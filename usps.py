import requests
import inspect

USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/57.0.2987.110 '
              'Safari/537.36')


class UspsApi(object):
    zipcode_api = 'https://tools.usps.com/tools/app/ziplookup/%s'
    zipcode_ref = 'https://tools.usps.com/zip-code-lookup.htm?%s'
    referers = {
        'cityByZip':        zipcode_ref % ('citybyzipcode'),
        'zipByCityState':   zipcode_ref % ('bycitystate'),
        'zipByAddress':     zipcode_ref % ('byaddress')
    }

    def __init__(self):
        super().__init__()

    def _zipcode_session(self, func_name, **kwargs):
        params = kwargs.get('params')
        params.pop('self')
        params = {k: '' if v is None else str(v) for k, v in params.items()}

        session = requests.Session()
        session.headers.update({
            'Referer': self.referers.get(func_name),
            'User-Agent': USER_AGENT
        })
        response = session.post(
            self.zipcode_api % (func_name),
            data=params,
            allow_redirects=False
        )
        session.close()
        return(response.json())

    def zipByAddress(self, address1=None, city=None, state=None, zip=None, companyName=None, address2=None):
        """
        Looks up address and returns whether the address is valid
        or invalid according to the USPS.
        """
        results = self._zipcode_session(
            func_name=inspect.stack()[0][3],
            params=locals()
        )
        return(results)

    def zipByCityState(self, city=None, state=None):
        """
        Looks up city and state returns valid zip-codes in that city
        along with the type according to the USPS.
        """
        results = self._zipcode_session(
            func_name=inspect.stack()[0][3],
            params=locals()
        )
        return(results)

    def cityByZip(self, zip=None):
        """
        Looks up zip-code and returns what cities reside within it
        according to the USPS.
        """
        results = self._zipcode_session(
            func_name=inspect.stack()[0][3],
            params=locals()
        )
        return(results)
