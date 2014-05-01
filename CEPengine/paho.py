#!/usr/bin/env jython

# This module wraps the paho library (mqtt client)
# Adapted from org.eclipse.paho.sample.mqttv3app

# Marc de Lignie, Politie IV-organisatie
# April 7, 2014

import sys, threading
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken as IMqttDeliveryToken 
import org.eclipse.paho.client.mqttv3.MqttCallback as MqttCallback 
import org.eclipse.paho.client.mqttv3.MqttClient as MqttClient
import org.eclipse.paho.client.mqttv3.MqttConnectOptions as MqttConnectOptions
import org.eclipse.paho.client.mqttv3.MqttException as MqttException
import org.eclipse.paho.client.mqttv3.MqttMessage as MqttMessage
import org.eclipse.paho.client.mqttv3.persist.MqttDefaultFilePersistence \
                                              as MqttDefaultFilePersistence

class MqttClient(MqttCallback, threading.Threading): 

    def __init__(self, brokerUrl, clientId, cleanSession, userName, password)
    """*
     * Constructs an instance of the sample client wrapper
     * @param brokerUrl the url of the server to connect to
     * @param clientId the client id to connect with
     * @param cleanSession clear state at end of connection or not 
     * (durable or non-durable subscriptions)
     * @param userName the username to connect with
     * @param password the password for the user
     * @throws MqttException
     """
        self.brokerUrl = brokerUrl
        self.clean     = cleanSession
        self.password  = password
        self.userName  = userName
        # This client stores messages in a temporary directory
        dataStore = MqttDefaultFilePersistence('/tmp')
        try: 
            # Construct the connection options object that contains connection parameters
            # such as cleanSession and LWT
            conOpt = MqttConnectOptions()
            conOpt.setCleanSession(clean)
            if(password != null ) 
              conOpt.setPassword(self.password.toCharArray())
            
            if(userName != null) 
              conOpt.setUserName(self.userName)
            

            # Construct an MQTT blocking mode client
            client = MqttClient(self.brokerUrl,clientId, dataStore)

            # Set this wrapper as the callback handler
            client.setCallback(this)

         except MqttException, e:
            print str(e)
            sys.exit(1)
            
    def subscribe(self, topicName, qos):
        """
         * Subscribe to a topic on an MQTT server
         * Once subscribed this method waits for the messages to arrive from the server
         * that match the subscription. It continues listening for messages.
         * @param topicName to subscribe to (can be wild carded)
         * @param qos the maximum quality of service to receive messages at for this subscription
        """
        # Connect to the MQTT server
        self._client.connect(conOpt)
        # Subscribe to the requested topic
        # The QoS specified is the maximum level that messages will be sent to the client at.
        # For instance if QoS 1 is specified, any messages originally published at QoS 2 will
        # be downgraded to 1 when delivering to the client but messages published at 1 and 0
        # will be received at the same level they were published at.
        self._client.subscribe(topicName, qos)
        # Continue waiting for messages
        sys.stdin.readline()
 		self._client.disconnect();
       
    def publish(self, topicName, qos, payload):
        """
         * Publish / send a message to an MQTT server
         * @param topicName the name of the topic to publish to
         * @param qos the quality of service to delivery the message at (0,1,2)
         * @param payload the set of bytes to send to the MQTT server
        """
    	# Connect to the MQTT server
    	self._client.connect(conOpt);
    	# Create and configure a message
   		message = MqttMessage(payload);
    	message.setQos(qos);
    	# Send the message to the server, control is not returned until
    	# it has been delivered to the server meeting the specified
    	# quality of service.
    	self._client.publish(topicName, message);
    	# Disconnect the client
    	self._client.disconnect();

    """**************************************************************"""
    """ Methods to implement the MqttCallback interface              """
    """**************************************************************"""
    def connectionLost(self, cause) :
        print "Connection to " + self.brokerUrl + " lost!" + cause
        raise NotImplementedError(cause) # Abstract method
    
    def deliveryComplete(self, token):
        raise NotImplementedError  # Abstract method
    
    def messageArrived(self, topic, message):
        # Called when a message arrives from the server that matches any
        # subscription made by the client
        print ("Time:\t" +time +
               "  Topic:\t" + topic +
               "  Message:\t" + str(message.getPayload()) +
               "  QoS:\t" + message.getQos())
        raise NotImplementedError  # Abstract method
    

