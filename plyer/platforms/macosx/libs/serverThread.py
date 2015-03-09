# A UDP server that relays incoming messages to server-side programs as
# if it were a sensor, supplying device data in a specified way at specified intervals.
# The server listens at port 10552.

# A server-side application importing ServerThread needs to do four things:
# 1. import the module.
# 2. Define a handler class H that knows what to do with received data.
# 3. Instantiate a serverThread submitting H as an argument to __init__.
# 4. Call the serverThread's start() method.

import threading, SocketServer

PORTNO = 10552

class ServerThread (threading.Thread):
    """
    Thread that runs a UDP server.
    """

    # The number of times __init__() is called minus the number of times shutdown() is called.
    population = 0

    # Track which classes of handler exist in the server.
    handler_classes = []

    # All instances of serverThread have this name. 
    # Assumption: only instances of serverThread have this name within the global list of all threads.
    name = 'ServerThread'

    def __init__(self, handler):
        threading.Thread.__init__(self)
        
        ServerThread.population += 1

        # If this handler class has already been encounted, don't do anything more.
        # (This is the case of a device enabling, disabling, and then enabling.) The handler
        # is already present in the server. The device just needs to tap back in to the incoming data.
        if ServerThread.handler_classes.count( handler ) > 0:
            # Nullify the run statement so the thread just dies.
            self.run = lambda : None
            return

        else:

            # Otherwise, store that class to the class-wide ServerThread.handler_classes
            ServerThread.handler_classes.append( handler )

            # Find out if there is already an instance of this class of thread running within the global list of threads.
            existing_server_thread = None
            for thrd in threading.enumerate():
                if thrd.name == self.name:
                    existing_server_thread = thrd

            # If there is not an existing ServerThread instance, create a new server configured with the caller-supplied handler.
            # Otherwise, aggregate the existing server's handler with the caller-supplied handler, kill the existing server 
            # thread (thereby freeing up PORTNO), and finally create a new server configured with the aggregate handler
            # to be run on this thread.

            if existing_server_thread == None:
                # Configure a UDP server at PORTNO with handler for each received datagram.
                self.server = SocketServer.UDPServer(('',PORTNO), handler)
                self.handler = handler

            else:
                # Kill the current server thread, but not before storing the old handler class.
                old_handler = existing_server_thread.handler

                # Tell the existing thread to die, but without calling shutdown(). Because that would compromise 
                # the intended meaning of ServerThread.population.
                existing_server_thread.server.shutdown()
                existing_server_thread.server.server_close()
                
                # Aggregate the handlers: instantiate an old handler and a new handler for each received datagram.
                def aggregate_handler(request, client_address, obj):
                    old_handler(request, client_address, obj)
                    handler(request, client_address, obj)

                # Configure a UDP server with the aggregate handler.
                self.server = SocketServer.UDPServer(('',PORTNO), aggregate_handler)
                self.handler = aggregate_handler
            
    def run(self):
        # Start server.
        self.server.serve_forever()

    def shutdown( self ):
        # If all __init__ callers but one have called shutdown(),
        # shutdown the server and empty ServerThread.handler_classes.
        if ServerThread.population == 1:
            # Shutdown the UDP server.
            self.server.shutdown()
            # Free up socket address.
            self.server.server_close()
            
            ServerThread.handler_classes = []
        
        # Decrement ServerThread.population
        ServerThread.population -= 1
