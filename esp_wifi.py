import binascii
import network
import time


def STA(ssid='', key='', txpower=None, wait=10, ip=None, subnet=None, gateway=None, dns=None):
    # Create a network interface,set IF to STA mode
    sta = network.WLAN(network.STA_IF)
    sta.active(True)  # activate interface
    mac = binascii.hexlify(sta.config('mac'), ':').decode()
    print("STA mac:", mac)
    print("dhcp_hostname:", sta.config('dhcp_hostname'))
    print("reconnects:", sta.config('reconnects'))
    if txpower != None:
        try:
            sta.config(txpower=txpower)  # set txpower(dBm)
        except Exception as e:
            print(e)
    try:
        txpower_dBm = sta.config("txpower")
        txpower_mW = 10 ** (txpower_dBm / 10)  # Unit conversion,(dBm) to (mW)
        print("txpower:{0}dBm,{1}mW".format(txpower_dBm, txpower_mW))
    except Exception as e:
        print(e)
    try:
        if not sta.isconnected():
            sta.connect(ssid, key)
            print('start to connect WiFi:', ssid)
            for i in range(wait):
                print('try to connect WiFi in {}s'.format((i + 1)))
                time.sleep(1)
                if sta.isconnected():
                    break
        if sta.isconnected():
            print('WiFi connection succeeded!')
            if ip == None:
                ip = sta.ifconfig()[0]
            if subnet == None:
                subnet = sta.ifconfig()[1]
            if gateway == None:
                gateway = sta.ifconfig()[2]
            if dns == None:
                dns = gateway
            net_interface = (ip, subnet, gateway, dns)
            sta.ifconfig(net_interface)
            _f = "{0:<15}|{1:<15}|{2:<15}|{3:<15}"
            print(_f.format("IP address", "subnet mask", "gateway", "DNS server"))
            print(_f.format(sta.ifconfig()[0], sta.ifconfig()[
                  1], sta.ifconfig()[2], sta.ifconfig()[3]))
            return sta.ifconfig()
        else:
            print('WiFi connection Failed!')
            sta.disconnect()
            sta.active(False)
            return 0
    except Exception as e:
        try:
            print(e)
            sta.disconnect()
            sta.active(False)
        except OSError:
            pass


def scan(ssid=None, loop=None, txpower=None):
    def _authmode(mode: int):
        try:
            return auth_mode[mode]
        except KeyError:
            # handle unknown modes
            return "mode-{}".format(mode)

    def _hidden(net: tuple):
        return net[5] if len(net) > 5 else "-"

    auth_mode = {0: "Open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK", 5: "WPA2-EAS", 6: "WPA3-PSK",
                 7: "WPA2/WPA3-PSK"}
    print('=====================================WiFi Scan======================================')
    _f = "{0:<32} {1:>12} {2:>8} {3:>6} {4:<13} {5:>8}"
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if txpower != None:
        try:
            sta.config(txpower=txpower)  # set txpower(dBm)
        except Exception as e:
            print(e)
    if loop == None:
        loop = 1
    for i in range(loop):
        _networks = sta.scan()
        _networks = sorted(_networks, key=lambda x: x[3], reverse=True)
        scaned = 0
        print(_f.format("SSID", "MAC address",
              "Channel", "Signal", "Authmode", "Hidden"))
        for _net in _networks:
            if ssid == None:
                print(_f.format(_net[0], binascii.hexlify(_net[1]), _net[2], _net[3], _authmode(_net[4]),
                                _hidden(_net)))
            else:
                if str(_net[0].decode()) == ssid:
                    scaned = 1
                    print(_f.format(_net[0], binascii.hexlify(_net[1]), _net[2], _net[3], _authmode(_net[4]),
                                    _hidden(_net)))
        if scaned == 0 and ssid != None:
            print(ssid, "isn't scaned")
        print('===================================================================================')


def AP(ssid='', key='', authmode=3, txpower=None, channel=11, hidden=False, ip=None, subnet=None, gateway=None,
       dns=None):
    # Create a network interface,set IF to AP mode
    ap = network.WLAN(network.AP_IF)
    ap.active(True)  # activate interface
    mac = binascii.hexlify(ap.config('mac'), ':').decode()
    print("AP mac:", mac)
    if txpower != None:
        try:
            ap.config(txpower=txpower)  # set txpower(dBm)
        except Exception as e:
            print(e)
    try:
        txpower_dBm = ap.config("txpower")
        txpower_mW = 10 ** (txpower_dBm / 10)  # Unit conversion,(dBm) to (mW)
        print("txpower:{0}dBm,{1}mW".format(txpower_dBm, txpower_mW))
    except Exception as e:
        print(e)
    try:
        ap.config(ssid=ssid, key=key, authmode=authmode,
                  channel=channel, hidden=hidden)
        print("ssid:", ap.config('ssid'))
        print("channel:", ap.config('channel'))
        print("hidden:", ap.config('hidden'))
        print("authmode:", ap.config('authmode'))
        if ip == None:
            ip = ap.ifconfig()[0]
        if subnet == None:
            subnet = ap.ifconfig()[1]
        if gateway == None:
            gateway = ip
        if dns == None:
            dns = ip
        net_interface = (ip, subnet, gateway, dns)
        ap.ifconfig(net_interface)
        _f = "{0:<15}|{1:<15}|{2:<15}|{3:<15}"
        print(_f.format("IP address", "subnet mask", "gateway", "DNS server"))
        print(_f.format(ap.ifconfig()[0], ap.ifconfig()[
              1], ap.ifconfig()[2], ap.ifconfig()[3]))
        return ap.ifconfig()
    except Exception as e:
        print(e)
        ap.active(False)
        return 0
# scan()
