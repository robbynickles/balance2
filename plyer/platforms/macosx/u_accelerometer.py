'''
MacOSX accelerometer
---------------------

Start a UDP server expecting UDP packets with acceleration data. 
_get_acceleration() passes the acceleration data on as if it came from the macbook.
'''
from plyer.facades import Accelerometer

from libs.deviceHandler import DeviceHandler, parse_message
from libs.serverThread import ServerThread

DEVICE_CACHE = []

class AccHandler( DeviceHandler ):
    device_name  = 'U_Accel'
    device_cache = DEVICE_CACHE
    parser       = lambda self, msg: parse_message( msg )

class OSXAccelerometer(Accelerometer):
    def _enable(self):
        # Run the UDP server in the background.
        self.device_cache = DEVICE_CACHE
        self.thread = ServerThread( AccHandler )
        self.thread.start()

    def _disable(self):
        # Shutdown the server.
        self.thread.shutdown()

    def _get_acceleration(self):
        """ Return a 3-tuple of the accelerations due to user motion on each axis measured in g-forces. """
        try:
            # Access the latest data from the device cache.
            x_acc, y_acc, z_acc = self.device_cache[-1]
            return x_acc, y_acc, z_acc 
        except IndexError:
            # self.device_cache is empty
            return 0,0,0
        except ValueError:
            # data isn't a 3-tuple.
            return 0,0,0

def instance():
    return OSXAccelerometer()
