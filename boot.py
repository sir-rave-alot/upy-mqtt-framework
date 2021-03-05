import time
import umqtt.simple
import ubinascii
import machine
import uos
import ujson
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
CFG_FILE="config.js"
CB_FILE="callbacks"
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
SDC_MOUNTPOINT   ="/sd"
SDC_SPI_SLOT     = 2
SDC_SPI_PIN_CLK  = 18
SDC_SPI_PIN_MISO = 19
SDC_SPI_PIN_MOSI = 23
SDC_SPI_PIN_CS   = 5
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
# MOUNT FLASH DEVICE
try:
    print("Mounting flash device ...")
    uos.mount(machine.SDCard(
        slot = SDC_SPI_SLOT,
        sck  = machine.Pin(SDC_SPI_PIN_CLK),
        miso = machine.Pin(SDC_SPI_PIN_MISO),
        mosi = machine.Pin(SDC_SPI_PIN_MOSI),
        cs   = machine.Pin(SDC_SPI_PIN_CS)
        ),SDC_MOUNTPOINT)
    print("[Success]")
except OSError:
    print("[Fail] Mount failed.")
# READ CONFIGURATION
try:
    print("Read configuration ...")
    with open(SDC_MOUNTPOINT + "/" + CFG_FILE) as _cfgfile:
        _cfg = ujson.load(_cfgfile)
        try:
            ssid            = _cfg["ssid"]
            password        = _cfg["key"]
            mqtt_server     = _cfg["mqtt"]["broker-addr"]
            print("[Success]")
        except KeyError:
            print("[Fail] Bad configuration.")
except OSError:
    print("[Fail] No such file. '{}'".format(SDC_MOUNTPOINT + "/" + CFG_FILE))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

mqtt_client_id = ubinascii.hexlify(machine.unique_id())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NETWORK CONNECTION
print("Connect to network ...")
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    time.sleep(1)
    print(".", end="")
print("\n[Success]")
_ifcfg = station.ifconfig()

print("Assigned IP = {}".format(_ifcfg[0]))
print("Subnet-mask = {}".format(_ifcfg[1]))
print("Default GW  = {}".format(_ifcfg[2]))
print("DNS         = {}".format(_ifcfg[3]))
#
print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
