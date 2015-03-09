'''
MacOSX compass
---------------------

Start a UDP server expecting UDP packets with orientation data. 
_get_orientation() passes the orientation data on as if it came from the macbook.
'''
from plyer.facades import Compass

from libs.deviceHandler import DeviceHandler, parse_message
from libs.serverThread import ServerThread

DEVICE_CACHE = []

class CompassHandler( DeviceHandler ):
    device_name  = 'Compass'
    device_cache = DEVICE_CACHE
    parser       = lambda self, msg: parse_message( msg )

class OSXCompass(Compass):
    def _enable(self):
        # Run the UDP server in the background.
        self.device_cache = DEVICE_CACHE
        self.thread = ServerThread( CompassHandler )
        self.thread.start()

    def _disable(self):
        # Shutdown the server.
        self.thread.shutdown()

    def _get_orientation(self):
        """ Return a 3-tuple of the 3  orientations on each axis measured in g-forces. """
        try:
            # Access the latest data from the device cache.
            x, y, z = self.device_cache[-1]
            return x, y, z 
        except IndexError:
            # self.device_cache is empty
            return 0,0,0
        except ValueError:
            # data isn't a 3-tuple.
            return 0,0,0

def instance():
    return OSXCompass()
