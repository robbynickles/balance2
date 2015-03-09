'''
MacOSX gyroscope
---------------------

Start a UDP server expecting UDP packets with gyroscope data. 
_get_orientation() passes the gyroscope data on as if it emanated from this machine.
'''
from plyer.facades import Gyroscope

from libs.deviceHandler import DeviceHandler, parse_message
from libs.serverThread import ServerThread 

DEVICE_CACHE = []

class GyroHandler( DeviceHandler ):
    device_name  = 'Gyro'
    device_cache = DEVICE_CACHE
    parser       = lambda self, msg: parse_message( msg )

class OSXGyroscope(Gyroscope):
    def _enable(self):
        try:
            self.device_cache = DEVICE_CACHE
            # Run the UDP server in the background.
            self.thread = ServerThread( GyroHandler )
            self.thread.start()
        except:
            raise Exception('Could not enable gyroscope on this macbook!')

    def _disable(self):
        # Shutdown the server.
        self.thread.shutdown()

    def _get_orientation(self):
        """ Return a 3-tuple of 3 angles in the form of roll, pitch, yaw measured in radians. """
        try:
            # Access the latest data from the device cache.
            x_rot, y_rot, z_rot = self.device_cache[-1]
            return x_rot, y_rot, z_rot 
        except IndexError:
            # self.device_cache is empty
            return 0,0,0
        except ValueError:
            # data isn't a 3-tuple.
            return 0,0,0

def instance():
    return OSXGyroscope()
