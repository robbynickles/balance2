import SocketServer

def parse_message( msg ):
    """ Tell the handler how to parse the message. """
    # Message format: 
    # "Device_Name, x, y, z" 
    try:
        device_name, x, y, z = msg.split(',')
        return device_name, x, y, z
    except ValueError:
        print "Recieved message ( {} ) couldn't be split into (device_name, x, y, z)".format( msg )
        return None, 0,0,0

class DeviceHandler(SocketServer.DatagramRequestHandler):
    device_name  = None
    device_cache = []
    parser       = lambda self, msg: (None, 0, 0, 0)

    def handle(self):
        newmsg = self.request[ 0 ]
        try:
            dev, x, y, z = self.parser( newmsg )
        except ValueError:
            print """Parser returns something of the wrong format.
            It should return a 4-tuple, preferably of the form (device_name, x, y, z)."""
            return
        # Only relay messages that are labeled self.device_name.
        if dev == self.device_name:
            try:
                x, y, z = map(float, [x, y, z] )
                self.device_cache.append( (x, y, z) )
            except ValueError:
                print "{} messsage wrong format: the last three values couldn't be converted floats.".format( self.device_name )
                return
