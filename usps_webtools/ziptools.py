import requests
from fake_useragent import UserAgent


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
