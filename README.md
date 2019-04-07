# UspsApi
Simple USPS API using request.

Sample Usage:

``` {.sourceCode .python}
>>> from UspsApi.usps import UspsApi
>>> usps = UspsApi()

#Get Address Verification
>>> usps.zipByAddress(address1="1745 Fairfield Road", city="Milwaukee", state="WI", zip=53202)

{'resultStatus': 'SUCCESS', 'addressList': [{'addressLine1': '1745 W FAIRFIELD CT', 'city': 'MILWAUKEE', 'state': 'WI', 'zip5': '53209',
'zip4': '', 'carrierRoute': 'C041', 'countyName': 'MILWAUKEE', 'cmar': 'N', 'recordType': 'S', 'dpvConfirmation': 'N', 'defaultFlag': '',
'defaultInd': 'E'}]}

#Get Zipcodes in by city and state
>>> usps.zipByCityState(city="Milwaukee", state="WI")

{'resultStatus': 'SUCCESS', 'city': 'MILWAUKEE', 'state': 'WI', 'zipList': [{'zip5': '53201', 'recordType': 'PO BOX'}, {'zip5': '53202'},.....

#Get City by Zipcode
>>> usps.cityByZip(zip="53202")

{'resultStatus': 'SUCCESS', 'zip5': '53202', 'defaultCity': 'MILWAUKEE', 'defaultState': 'WI',
'defaultRecordType': 'STANDARD', 'citiesList': [], 'nonAcceptList': []}

#Track a Package
>>> usps.trackPackage(tracking_number="000000000000")

'The tracking number may be incorrect or the status update is not yet available. Please verify your tracking number and try again later., , ,
