import threading
from plyer.platforms.macosx.libs.serverThread import ServerThread

# Management of ServerThread at the application level, specifically meant to 
# be used in  App.on_stop. Bengin to use even if ServerThread is not being used 

def find_server_thread():
    # Find out if there is an instance of ServerThread running within the global list of threads.
    existing_server_thread = None
    for thrd in threading.enumerate():
        if thrd.name == 'ServerThread':
            existing_server_thread = thrd
    return existing_server_thread

# This handles the case when the application is quitting but not all of the devices have called disable().

def shutdown_server_thread():
    existing_server_thread = find_server_thread()

    if existing_server_thread:

        # Under normal circumstances, ServerThread.population would be automatically adjusted as each device
        # enables or disables. The server dies only when the population reaches one and that last device disables.
        # So to force the server thread to die, even if all devices haven't called disable(), manually set ServerThread.population to 1.
        ServerThread.population = 1

        existing_server_thread.shutdown()
