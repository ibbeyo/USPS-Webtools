import inspect
from bs4 import BeautifulSoup, re
from urllib.parse import quote
import requests


class UspsApi(object):
    ua = ('Mozilla/5.0 (X11; Linux x86_64) '
          'AppleWebKit/537.36 (KHTML, like Gecko) '
          'Chrome/57.0.2987.110 '
          'Safari/537.36')

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': self.ua
        })

    def _ziplookup(self, data):
        data.pop('self')
        data = {k: '' if v is None else str(v) for k, v in data.items()}
        response = self._session.post(
            url=f'https://tools.usps.com/tools/app/ziplookup/{inspect.stack()[1][3]}',
            data=data,
            allow_redirects=False
        )
        self._session.close()
        return(response.json())

    def zipByAddress(self, address1, city, state, zip, companyName=None, address2=None):
        """
        Looks up address and returns whether the address is valid
        or invalid according to the USPS.
        """
        results = self._ziplookup(data=locals())
        return(results)

    def zipByCityState(self, city, state):
        """
        Looks up city and state returns valid zip-codes in that city
        along with the type according to the USPS.
        """
        results = self._ziplookup(data=locals())
        return(results)

    def cityByZip(self, zip):
        """
        Looks up zip-code and returns what cities reside within it
        according to the USPS.
        """
        results = self._ziplookup(data=locals())
        return(results)

    def trackPackage(self, tracking_number):
        def _etaFilter(string):
            string = string.strip().replace('\xa0', ' ').replace('\t', '').replace('\r', '')
            return([x for x in string.split('\n') if x != ''])

        def _getDeliveryStatus(html):
            sf = ', '.join([x.get_text() for x in html.find_all('p')])
            sf = ' '.join([x.strip() for x in _etaFilter(sf)])
            return(sf)

        tracking_api = 'https://tools.usps.com/go/TrackConfirmAction?tLabels={}'
        response = self._session.get(
            tracking_api.format(tracking_number),
            allow_redirects=False
        )

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get All Tracking Information
        tracking_info = soup.find('div', id='tracked-numbers')

        # Expected Delivery Data
        eta_delivery = tracking_info.find('div', attrs={'class': 'expected_delivery'})

        # Delivery Status Data
        delivery_status = tracking_info.find('div', attrs={'class': 'delivery_status'})

        try:
            eta = eta_delivery.find('span', attrs={'class': 'eta_snip'}).get_text()
        except AttributeError:
            return(_getDeliveryStatus(html=delivery_status))
        else:
            status_feed = _getDeliveryStatus(html=delivery_status)

        eta = _etaFilter(eta)
        month, year = eta[2].split(' ')

        eta_time = eta_delivery.find('strong', attrs={'class': 'time'}).get_text()
        eta_time = _etaFilter(eta_time)

        # Tracking History Data
        hist_data = soup.find('div', attrs={'class': 'panel-actions-content thPanalAction'})

        val = 0
        row = list()
        tracking_history = dict()
        for elem in hist_data.find_all(['span', 'hr']):
            if elem.text == '':
                val += 1
                tracking_history[val] = list(row)
                row.clear()
                continue
            row.extend([' '.join(_etaFilter(x)) for x in elem.stripped_strings])

        status = {
            'tracking_number': tracking_number,
            'expected_delivery': {
                'status': eta_delivery.find('h3').get_text().strip(),
                'on': {
                    'day': eta[0],
                    'date': eta[1],
                    'month': month,
                    'year': year
                },
                'by': eta_time[0],
            },
            'delivery_status': {
                'status': delivery_status.find('h2').get_text().strip(),
                'status_feed': status_feed
            },
            'tracking_history': tracking_history
        }

        self._session.close()
        return(status)


usps = UspsApi()
