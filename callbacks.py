# callbacks.py
#
# Usage:
#  (1) You have to provide the mandatory variables
#      a. "subscribe_callbacks"
#         dictionary containing topic and it's callback function object
#      b. "userloop"
#         function object to be called in the infinite mainloop 
#
#  (2) To publish on the mqtt server, use the functions
#      a. "publish(_topic, _msg)"
#         for normal priority topics
#      b. "publish_prio(_topic, _msg)"
#         for high priority topics

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# BEGIN SECTION 1
# DO NOT CHANGE THIS SECTION (SECTION 1)
import time
import machine
import uos
import micropython

publish_queue = []

# USE THIS FUNCTION TO PUBLISH A NORMAL MESSAGE
def publish(_topic, _msg):
    global publish_queue
    publish_queue.append((_topic, _msg))

# USE THIS FUNCTION TO PUBLISH A HIGH PRIORITY MESSAGE
def publish_prio(_topic, _msg):
    global publish_queue
    publish_queue.insert(0,(_topic, _msg))
# END SECTION 1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#########################
# USER CODE BEGINS HERE #
#########################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USER MODULES

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USER VARIABLES
lamppin = machine.Pin(33, machine.Pin.OUT)

topic_pub = b'lamp-001'
last_message = 0
message_interval = 0.2
counter = 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USER FUNCTIONS
def lampOn(_p):
    print('+++ lamp ON. +++')
    _p.value(1)

def lampOff(_p):
    print('+++ lamp OFF. +++')
    _p.value(0)

def getLampState(_p):
    if lamppin.value() == 1:
        return "ON"
    else:
        return "OFF"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# USER SUBSCRIPTION CALLBACKS (must take one string argument)
def toggleLamp(msg_str):
    if msg_str == b'ON': # TURN ON LED
        lampOn(lamppin)
    if msg_str == b'OFF': # TURN OFF LED
        lampOff(lamppin)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# WILL BE RUN ITERATIVELY (no arguments allowed)
# PUBLISH TOPICS HERE
def update_publications():
    global topic_pub
    global last_message
    global message_interval
    global counter
    
    # Publish to the server periodically
    if (time.time() - last_message) > message_interval:
        msg = getLampState(lamppin)
        publish(topic_pub,"{} - {}".format(msg, counter))
        last_message = time.time()
        counter += 1
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MANDATORY
# SUBSCRIPTION CALLBACK ASSIGNMENTS
subscribe_callbacks = {
    b'lamp-controls/lamp-001' : toggleLamp
    }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MANDATORY
# CHOOSE YOUR LOOP FUNCTION
userloop = update_publications

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#######################
# USER CODE ENDS HERE #
#######################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #