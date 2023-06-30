# micropython-esp-wifi
Easy way to do WiFi connection, WiFi scan, WiFi AP. Mainly used in ESP32S3, ESP32S2.

It can be installed from [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip) via:

```
>>> import mip
>>> mip.install("github:Wind-stormger/micropython-esp-wifi")
```

Or from mpremote via

```bash
mpremote mip install github:Wind-stormger/micropython-esp-wifi
```

# Use Cases

```py
import esp_wifi

# Simple
esp_wifi.scan()
esp_wifi.STA('SSID', 'PASSWORD')
esp_wifi.AP('SSID', 'PASSWORD')

# Full
esp_wifi.scan(ssid=None, loop=None, txpower=None)
esp_wifi.STA(ssid='SSID', key='PASSWORD', txpower=None, wait=10, ip=None, subnet=None, gateway=None, dns=None)
esp_wifi.AP(ssid='SSID', key='PASSWORD', authmode=3, txpower=None, channel=11, hidden=False, ip=None, subnet=None, gateway=None,
       dns=None)

```
