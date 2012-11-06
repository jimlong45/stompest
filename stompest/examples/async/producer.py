"""
Copyright 2011 Mozes, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging
import json

from twisted.internet import defer, reactor

from stompest.async import Stomp
from stompest.protocol import StompConfig

class Producer(object):
    QUEUE = '/queue/testIn'

    def __init__(self, config=None):
        if config is None:
            config = StompConfig('tcp://localhost:61613')
        self.config = config
        
    @defer.inlineCallbacks
    def run(self):
        stomp = yield Stomp(self.config).connect()
        for j in range(10):
            stomp.send(self.QUEUE, json.dumps({'count': j}), receipt='message-%d' % j)
        yield stomp.disconnect() # graceful disconnect: waits until all receipts have arrived
        reactor.stop()
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Producer().run()
    reactor.run()