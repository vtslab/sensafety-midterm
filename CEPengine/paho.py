#!/usr/bin/env jython

# This module wraps the paho library (mqtt client)
# Adapted from org.eclipse.paho.sample.mqttv3app

# Marc de Lignie, Politie IV-organisatie
# August 29, 2014

import java.lang
import sys, time, re
import org.eclipse.paho.client.mqttv3.MqttCallback as MqttCallback 
import org.eclipse.paho.client.mqttv3.MqttClient as MqttClient
import org.eclipse.paho.client.mqttv3.MqttConnectOptions as MqttConnectOptions
import org.eclipse.paho.client.mqttv3.MqttException as MqttException
import org.eclipse.paho.client.mqttv3.MqttMessage as MqttMessage
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence \
                                              as MemoryPersistence

USERNAME = 'cs08' # for tcp://vps38114.public.cloudvps.com:1883
PASSWORD = 'cs08_2014' # for tcp://vps38114.public.cloudvps.com:1883
CLIENTID = 'Commit_829'

class PahoClient(MqttCallback): 

    def __init__(self, brokerUrl):
        try: 
            self._client = MqttClient(brokerUrl, CLIENTID,
                                                 MemoryPersistence())
            # Set this instance as the callback handler
            self._client.setCallback(self)
            # Leave client connected
            conopts = MqttConnectOptions()
            conopts.setUserName(USERNAME)
            conopts.setPassword(PASSWORD)
            self._client.connect(conopts)
        except MqttException, e:
            print str(e)
            sys.exit(1)
        self._destinations = {}

    def close(self):
        # Required to have jython exit
        if self._client.isConnected():
            self._client.disconnect()
            
    def subscribe(self, topicName, qos, callback = None):
        """
         * Subscribe to a topic on an MQTT server
         * Once subscribed this method waits for the messages to arrive from 
         * the server that match the subscription. 
         * @param topicName to subscribe to (can be wild carded)
         * @param qos the maximum quality of service to receive messages at for 
           this subscription
        """
        if topicName.find('#') < (len(topicName) - 1) and \
           topicName.find('#') > -1:
            raise ValueError('# wildcard only supported as final character')
        self._client.subscribe(topicName, qos)
        topicName = topicName.replace('//','/+/').replace('//','/+/')
        regex = '^' + topicName.replace('+', '[^/\s]+'
                                ).replace('#', '[^\s]+') + '$'
        self._destinations[regex] = callback
       
    def publish(self, topicName, qos, payload):
        """
         * Publish / send a message to an MQTT server
         * @param topicName the name of the topic to publish to
         * @param qos the quality of service to delivery the message at (0,1,2)
         * @param payload the set of bytes to send to the MQTT server
        """
    	# Create and configure a message
        message = MqttMessage(java.lang.String(payload).getBytes())
        message.setQos(qos)
        # Send the message to the server, control is not returned until
        # it has been delivered to the server meeting the specified
        # quality of service.
        try:
            self._client.publish(topicName, message)
        except:
            print "Trying mqtt publish after client disconnect

    def _topicmatch(self, topic):
        for regex in self._destinations:
            if re.search(regex, topic):
                return self._destinations[regex]
    	return None
    	
    """**************************************************************"""
    """ Default methods to implement the MqttCallback interface      """
    """**************************************************************"""

    def connectionLost(self, cause):
        print "Connection lost!" + str(cause)
    
    def deliveryComplete(self, token):
        pass
        #print "Delivery complete: " + str(token)
    
    def messageArrived(self, topic, message):
        # Called when a message arrives from the server that matches any
        # subscription made by the client
        #print topic, message.toString()
        destination = self._topicmatch(topic)
        if destination:
            destination(topic, message)
        else:
            print ("Time: " + str(time.time()) +
                   "  Topic: " + topic +
                   "  Message: " + str(message.toString()) +
                   "  QoS: " + str(message.getQos()))
    

# Only for testing; run with ./paho.sh    
if __name__ == "__main__": 
    paho = PahoClient("tcp://m2m.eclipse.org:1883")
#    paho = PahoClient("tcp://test.mosquitto.org:1883")  # too many messages?
#    paho = PahoClient("tcp://localhost:1883") # Assumes local mosquitto broker
    paho.subscribe("SenSafety/test", 1)
    time.sleep(1)
    paho.publish("SenSafety/test", 1, "Test")
    time.sleep(5)  # Increase to also publish with mosquitto_pub in shell
    paho.close()  # Otherwise python does not exit
