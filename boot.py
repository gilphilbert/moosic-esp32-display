"""
This file is executed on every boot (including wake-boot from deepsleep)
"""
import network
import utime
 
WifiSSID = "Glibertvue"
WifiPassword = "InThePNW1234"
Ep32HostName = "esp32.local"
 
def connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WifiSSID, WifiPassword)
        sta_if.config(dhcp_hostname=Ep32HostName)
    print('network config:', sta_if.ifconfig())
 
def showip():
    import network
    sta_if = network.WLAN(network.STA_IF)
    print('network config:', sta_if.ifconfig())
    print('hostname:', sta_if.config('dhcp_hostname'))

def getip():
    import network
    sta_if = network.WLAN(network.STA_IF)
    return sta_if.ifconfig()
 
connect()
for i in range(10):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        utime.sleep(1)
        print('.', end=' ')
    else:
        break
 
showip()
