#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The avahi module provides an avahi client to detect and monitor the presence
# of sensors and sensor gateways of specified servicetype.

# Marc de Lignie, Politie IV-organisatie
# April 10, 2014


import sys, time, hashlib

import java.io.IOException as IOException
import java.util.ArrayList as ArrayList

import avahi4j.Address as Address
import avahi4j.Avahi4JConstants as Avahi4JConstants
import avahi4j.Client as Client
import avahi4j.EntryGroup as EntryGroup
import avahi4j.IClientCallback as IClientCallback
import avahi4j.IEntryGroupCallback as IEntryGroupCallback
import avahi4j.IServiceBrowserCallback as IServiceBrowserCallback
import avahi4j.IServiceResolverCallback as IServiceResolverCallback
import avahi4j.ServiceBrowser as ServiceBrowser
import avahi4j.ServiceResolver as ServiceResolver
import avahi4j.Avahi4JConstants.BrowserEvent as BrowserEvent
import avahi4j.Avahi4JConstants.Protocol as Protocol
import avahi4j.Client.State as State
import avahi4j.EntryGroup.State as State
import avahi4j.ServiceResolver.ServiceResolverEvent as ServiceResolverEvent
import avahi4j.exceptions.Avahi4JException as Avahi4JException


class ServicePublisher(IClientCallback, IEntryGroupCallback):
    # Client maintains its own thread as daemon andd returns
    # One Client can only handle one servicetype reliably
    # Use separate instance for each service

    def __init__(self, servicename, servicetype, 
                 servicesubtype, port, txtlist=None):
        self._client = Client(self)
        self._client.start()
        self._group = self._client.createEntryGroup(self)
        try:
            self._group.addService(Avahi4JConstants.AnyInterface, Protocol.ANY,
                servicename, servicetype, None, None, port, txtlist)
            if servicesubtype:
                self._group.addServicesubType(Avahi4JConstants.AnyInterface, 
                  Protocol.ANY, servicename, servicetype, None, servicesubtype)
            self._group.commit() 
        except Avahi4JException, e:
            print "Error publishing service by avahi4j\n", e
		                
    def stop(self):
        self._group.release()
        self._client.stop()
        self._client.release()


class ServiceBrowser(IClientCallback, IServiceBrowserCallback,
		             IServiceResolverCallback):
    # Client maintains its own thread as daemon andd returns
    # One Client can only handle one servicetype reliably
    # Use separate instance for each service
    
    def __init__(self, servicetype):
        """ Matching services are delivered to the callback method 
            serviceCallback which then resolves the services.
        """
        self._services = {}
        self._resolvers = ArrayList()
        self._client = Client(self)
        self._browser = self._client.createServiceBrowser(self, 
            Avahi4JConstants.AnyInterface, Protocol.ANY, servicetype, None, 0)
        self._client.start()
    
    def stop(self):
        # release the browser first so no more ServiceResolver can be added
        # to the list
        self._browser.release()    
        # we can now safely release items in the list
        for s in self._resolvers:
            s.release()        
        # stop and release the client
        self._client.stop()
        self._client.release()
        
    def getServices(self):
        return self._services
    
    def serviceCallback(self, interfaceNum, proto, browserEvent, name, 
                                      jtype, domain, lookupResultFlag):
        if browserEvent==BrowserEvent.NEW or browserEvent==BrowserEvent.REMOVE:
            # store service details
            key = hashlib.md5(str(interfaceNum) + str(proto) + name + 
                              jtype + domain).hexdigest()
            self._services.update({key: {
                'interface': interfaceNum,
                'protocol': proto,
                'name': name,
                'type': jtype,
                'domain': domain
                }})
            # only if it's a new service, resolve it
            if browserEvent==BrowserEvent.NEW:
                try: 
                    # ServiceResolvers are kept open and a reference is stored
                    # in a list so they can be freed upon exit
                    self._resolvers.add(self._client.createServiceResolver(self, 
                            interfaceNum, proto, name, jtype, domain, 
                            Protocol.ANY, 0))
                except Avahi4JException, e:
                    print "error creating resolver"
                    print str(e)
            else:
                del self._services[key]
    
    def resolverCallback(self, resolver, interfaceNum, proto, resolverEvent, 
                         name, jtype, domain, hostname, address, port, 
                         txtRecords, lookupResultFlag):
        # print resolved name details
        if resolverEvent==ServiceResolverEvent.RESOLVER_FOUND:            
            if name==None and jtype==None and hostname==None:
                # if None, the service has disappeared, release the resolver
                # and remove it from the list
                resolver.release()
                self._resolvers.remove(resolver)
            else: 
                key = hashlib.md5(str(interfaceNum) + str(proto) + name + 
                                  jtype + domain).hexdigest()
                self._services[key].update({
                    'address': address,
                    'txtrecords': [s for s in txtRecords]
                    })
        else: 
            print "Unable to resolve name"
                    

# To do: write proper unit test        
if __name__ == "__main__":
    a1 = ServicePublisher("test2", "_http._tcp", None, 
                          12348, ['a=5', 'b=6'])
    a2 = ServicePublisher("test", "_http._tcp", "_cep._sub._http._tcp", 
                          12347, ['a=1', 'b=2'])
    b1=ServiceBrowser('_http._tcp')            # Published above
    b2=ServiceBrowser('_cep._sub._http._tcp')  # Published above
    b3=ServiceBrowser('_workstation._tcp')     # Present by default
    time.sleep(1)
    print "http services:\n", b1.getServices()
    print "cep services:\n", b2.getServices()
    print "workstation services:\n", b3.getServices()
    a1.stop()   # Probably unnecessary
    a2.stop()
    b1.stop()
    b2.stop()
    b3.stop()


