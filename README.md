# USPS-Webtools
Simple API for the USPS Webtools. No Authentication Required.

## Usage

Package Tracking Example:

```python
from usps_webtools import PackageTracking

package = PackageTracking('YOUR_TRACKING_NUMBER')

package.status
package.status_last_updated
package.eta
package.eta_status
package.as_dict()

```

ZipTools Lookup Example:

```python
from usps_webtools import zipByCityState, zipByAddress, cityByZip

zipByAddress('376 Fairfield St', 'New Lenox', 'IL', '60451')

zipByCityState('New Lenox', 'IL')

cityByZip('60451')


```
