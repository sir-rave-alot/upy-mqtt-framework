# upy-mqtt-framework
Simlpe MQTT framework for using a ESP32 with Micropython.  

## Requirements
- Basic understanding/experience with microcontroller boards.
- Basic understanding/experience with python/micropython.
- Basic understanding/experience with MQTT.
- ESP32 Device with
  - micropython installation
  - connected MicroSD slot
- MicroSD card (tested with FAT32 formatting)
- running MQTT broker

## Usage
1. Write `boot.py` and `main.py` to your IoT device's internal flash.
2. Put your network configuration file `config.js` on the MicroSD card (see section "Configuration File")
3. Put your callback file `callbacks.py` on the MicroSD card (see section "Callback File")
4. Populate the ESP32 board with the MicroSD card

Now you can power the device. Error log is available via serial port.

### Configuration File

To connect your IoT device to the local WiFi, populate the MicroSD card with a valid configuration file.
This file has to be named `config.js` and has to reside in the top directory of the MicroSD card.

Complete the following template with your credentials.  
`<..>` are placeholders, waiting to be filled.

```
{
   "device":{
      "id":"<future-use>",
      "type":"<future-use>"
   },
   "ssid":"<NETWORK NAME>",
   "key":"<NETWORK PASSPHRASE>",
   "interface":{
      "hostname":"<unused>",
      "addr":"dynamic",
      "port":"<unused>",
      "nm":"255.255.255.0",
      "dgw":"192.168.<N>.<N>",
      "dns":"192.168.<N>.<N>"
   },
   "mqtt":{
   	"broker-addr":"192.168.<N>.<N>"
   }
}
```
### Callback File
Write your micropython code in a file named `callbacks.py` and place it in the top directory of the MicroSD card.

You have to provide certain variables for the framework for proper functionality:
- `subscribe_callbacks` : dictionary containing topic and it's callback function object. Of course you have to first define a callback function.
- `userloop` : function object to be called in the infinite mainloop.

Use the example file in this repo as a starting point.

## Basic Principle
The following is some pseudo-code to depict the functionality:
```
Run boot.py:
   1. Mount MicroSD card
   2. Read network configuration and broker address
   3. Connect to network

Run main.py:
   1. Import custom callbacks.py
   2. Connect to MQTT broker
   3. Subscribe topics according to callbacks file
   4. Enter infinite loop:
      a. Check broker for incoming messages (subscription topics)
      b. If provided: run user loop
      c. If available: publish queuing topics
```
