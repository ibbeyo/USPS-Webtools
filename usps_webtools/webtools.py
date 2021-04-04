import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, re, element as bs4types
from typing import Tuple


def lookup(func):
    def wrapper(*args, **kwargs):

        response = requests.post(
            f'https://tools.usps.com/tools/app/ziplookup/{func.__name__}',
            data=func(*args, **kwargs),
            allow_redirects=False,
            headers={'User-Agent': UserAgent().random}
        )

        return response.json()
    return wrapper


@lookup
def cityByZip(zip) -> dict: 
    """
    Looks up zip-code and returns what cities reside within it
    according to the USPS."""

    return locals()
    

@lookup
def zipByAddress(address1, city, state, zip, companyName='', address2='') -> dict:
    """
    Looks up address and returns whether the address is valid 
    or invalid according to the USPS."""

    return locals()


@lookup
def zipByCityState(city, state) -> dict:
    """
    Looks up city and state returns valid zip-codes in that city
    along with the type according to the USPS."""

    return locals()


class PackageTracking(object):
    def __init__(self, tracking_number) -> None:
        "Track a package using the tracking number provided by USPS"

        super().__init__()
        response = requests.get(
            f'https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_number}',
            allow_redirects=False,
            headers={'User-Agent': UserAgent().random}
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        self._html = soup.find('div', id='tracked-numbers')
        self._expected_delivery = self._html.find('div', attrs={'class': 'expected_delivery'})
        self._delivery_status   = self._html.find('div', attrs={'class': 'delivery_status'})
        
        self._status = None
        self._status_last_updated = self._delivery_status.find('div', attrs={'class': 'status_feed'})
        self._eta = None
        self._eta_status = None


    @property
    def status(self) -> Tuple[str, None]:
        "Get the status of a package."
        
        if self._status: return self._status

        self._status = self._delivery_status.find('h2').get_text().strip()
        return self._status
    

    @property
    def status_last_updated(self) -> Tuple[str, None]:
        "Get the date of the most recent status update"

        if isinstance(self._status_last_updated, bs4types.Tag):
            element = self._status_last_updated.find('p')
            child = list(element.children)[0]
            text = ' '.join(re.sub(r'[\t\r\n]*', '', child).split()).strip()
            self._status_last_updated = text if text else None

        return self._status_last_updated
            

    @property
    def eta(self) -> Tuple[str, None]:
        "Get the expected delivery DATE for the package."

        if self._eta: return self._eta

        snippet = self._expected_delivery.find('span', attrs={'class': 'eta_snip'})

        if snippet: self._eta = snippet.get_text()
        
        return self._eta


    @property
    def eta_status(self) -> Tuple[str, None]:
        "Get the expected delivery STATUS for the package"

        if self._eta_status: return self._eta_status

        self._eta_status = self._expected_delivery.find('p').get_text().strip()
        return self._eta_status

    
    def as_dict(self) -> dict:
        "Returns all package tracking information as a dictionary."

        return {
            'package_status'        : self.status,
            'package_status_updated': self.status_last_updated,
            'package_eta'           : self.eta,
            'package_eta_status'    : self.eta_status
        }
