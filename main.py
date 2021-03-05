# IMPORT USER CALLBACKS
ucb = __import__(SDC_MOUNTPOINT+"/"+CB_FILE)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# SUBSCRIPTIONS

def mqtt_scb(topic, msg):
    # TODO : TRY EXCEPTION
    if hasattr(ucb, "subscribe_callbacks"):
        ucb.subscribe_callbacks[topic](msg)
    
def connect_and_subscribe():
    global mqtt_client_id, mqtt_server
    print("Connecting to MQTT Broker : {}".format(mqtt_server))
    mqtt_client = umqtt.simple.MQTTClient(mqtt_client_id, mqtt_server)
    mqtt_client.set_callback(mqtt_scb)
    mqtt_client.connect()
    if hasattr(ucb, "subscribe_callbacks"):
      for _sub_topic in ucb.subscribe_callbacks.keys():
          print("Subscribing : {}".format(_sub_topic))
          mqtt_client.subscribe(_sub_topic)
    else:
        print('[Warning] No subscription topics found. Variable "subscribe_callbacks" undefined.')

    return mqtt_client

def restart_and_reconnect():
  print('Resetting device ...')
  time.sleep(10)
  machine.reset()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MAIN PROGRAM RUN
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
    mqtt_client = connect_and_subscribe()
    print("[Success]")
except OSError as e:
    print("[Fail]")
    restart_and_reconnect()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if not(hasattr(ucb, "userloop")):
    print('[Warning] No publishing topics found. Variable "userloop" undefined.')

while True:
  try:
    mqtt_client.check_msg() # checkout subscriptions
    
    if hasattr(ucb, "userloop"):
        ucb.userloop()  # update publish queue
        
    # publish if available
    while len(ucb.publish_queue) > 0:
        pub = ucb.publish_queue.pop(0)
        mqtt_client.publish(pub[0], pub[1])
  except OSError as e:
    restart_and_reconnect()
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
