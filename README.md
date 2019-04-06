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

{'resultStatus': 'SUCCESS', 'city': 'MILWAUKEE', 'state': 'WI', 'zipList': [{'zip5': '53201', 'recordType': 'PO BOX'}, {'zip5': '53202'}, 
{'zip5': '53203'}, {'zip5': '53204'}, {'zip5': '53205'}, {'zip5': '53206'}, {'zip5': '53207'}, {'zip5': '53208'}, 
{'zip5': '53209'}, {'zip5': '53210'}, {'zip5': '53211'}, {'zip5': '53212'}, {'zip5': '53213'}, {'zip5': '53214'}, 
{'zip5': '53215'}, {'zip5': '53216'}, {'zip5': '53217'}, {'zip5': '53218'}, {'zip5': '53219'}, {'zip5': '53220'},
{'zip5': '53221'}, {'zip5': '53222'}, {'zip5': '53223'}, {'zip5': '53224'}, {'zip5': '53225'}, {'zip5': '53226'}, 
{'zip5': '53227'}, {'zip5': '53228'}, {'zip5': '53233'}, {'zip5': '53234', 'recordType': 'PO BOX'}, {'zip5': '53235'}, 
{'zip5': '53237', 'recordType': 'PO BOX'}, {'zip5': '53259', 'recordType': 'UNIQUE'}, {'zip5': '53263', 'recordType': 'UNIQUE'}, 
{'zip5': '53274', 'recordType': 'UNIQUE'}, {'zip5': '53278', 'recordType': 'UNIQUE'}, {'zip5': '53288', 'recordType': 'UNIQUE'}, 
{'zip5': '53290', 'recordType': 'UNIQUE'}, {'zip5': '53293', 'recordType': 'UNIQUE'}, {'zip5': '53295', 'recordType': 'UNIQUE'}]}

#Get City by Zipcode
>>> usps.cityByZip(zip="53202")

{'resultStatus': 'SUCCESS', 'zip5': '53202', 'defaultCity': 'MILWAUKEE', 'defaultState': 'WI', 
'defaultRecordType': 'STANDARD', 'citiesList': [], 'nonAcceptList': []}

#Track a Package
>>> usps.trackPackage(tracking_number="000000000000")

'The tracking number may be incorrect or the status update is not yet available. Please verify your tracking number and try again later., , ,'
