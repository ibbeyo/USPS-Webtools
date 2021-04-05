import requests
from typing import Tuple
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, re, element as bs4types
 

class PackageTracking(object):
    def __init__(self, tracking_number) -> None:
        super().__init__()
        "Track a package using the tracking number provided by USPS"

        self.tracking_number        = tracking_number
        self._expected_delivery     = None
        self._delivery_status       = None
        self._status                = None
        self._status_last_updated   = None
        self._eta                   = None
        self._eta_status            = None

        self.refresh()


    @property
    def status(self) -> Tuple[str, None]:
        "Gets the status of a package."
        
        if isinstance(self._status, bs4types.Tag):
            self._status = self._status.get_text().strip()

        return self._status
    

    @property
    def status_last_updated(self) -> Tuple[str, None]:
        "Gets the date of the most recent status update"

        if isinstance(self._status_last_updated, bs4types.Tag):
            element = self._status_last_updated.find('p')
            child = list(element.children)[0]
            text = ' '.join(re.sub(r'[\t\r\n]*', '', child).split()).strip()
            self._status_last_updated = text if text else None

        return self._status_last_updated
            

    @property
    def expected_delivery_date(self) -> Tuple[str, None]:
        "Gets the expected delivery DATE for the package."

        if isinstance(self._expected_delivery_date, bs4types.Tag):
             self._expected_delivery_date =  self._expected_delivery_date.get_text()
        
        return  self._expected_delivery_date


    @property
    def expected_delivery_status(self) -> Tuple[str, None]:
        "Gets the expected delivery STATUS for the package"

        if isinstance(self._expected_delivery_status, bs4types.Tag):
            self._expected_delivery_status = self._expected_delivery_status.get_text().strip()

        return self._expected_delivery_status

    
    @property
    def history(self) -> Tuple[list, None]:
        "Gets the package tracking history."
        
        if isinstance(self._history, bs4types.Tag):
            history = self._history.contents.copy()
            string = []; self._history = []
            for x in history:
                if isinstance(x, bs4types.Tag):
                    if x.name == 'hr':
                        event = re.sub(r'[\t\n\r]*', '', ' '.join(string))
                        event = event.strip().split('  ')
                        self._history.append({
                            'date': event[0],
                            'status': event[1],
                            'location': event[2] if len(event) >= 3 else None
                        })
                        string.clear()
                    else:
                        string.append(x.get_text().replace('\xa0', ' '))
        return self._history


    def refresh(self):
        "Gets most recent package tracking data from USPS."

        response = requests.get(
            f'https://tools.usps.com/go/TrackConfirmAction?tLabels={self.tracking_number}',
            allow_redirects=False,
            headers={'User-Agent': UserAgent().random}
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        html = soup.find('div', id='tracked-numbers')

        delivery_status = html.find('div', attrs={'class': 'delivery_status'})
        self._status = delivery_status.find('h2')
        self._status_last_updated = delivery_status.find('div', attrs={'class': 'status_feed'})

        expected_delivery = html.find('div', attrs={'class': 'expected_delivery'})
        self._expected_delivery_date = expected_delivery.find('span', attrs={'class': 'eta_snip'})
        self._expected_delivery_status = expected_delivery.find('p')

        self._history = html.find('div', attrs={'class': 'panel-actions-content thPanalAction'})
    

    def as_dict(self) -> dict:
        "Returns all package tracking information as a dictionary."

        return {
            'status': self.status,
            'status_last_updated': self.status_last_updated,
            'expected_delivery': {
                'date': self.expected_delivery_date,
                'status': self.expected_delivery_status
            },
            'history': {
                'events': self.history
            },
            'product_info': {
                'postal_product': '',
                'features': ''
            }
        }
