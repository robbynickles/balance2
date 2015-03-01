from kivy.app import App

from libs.swipebook import SwipeBook
from libs.menu.menu import Menu
from libs.game.gamelayout import GameLayout

from plyer.libs.server_utils import shutdown_server_thread

class DrawTiltApp(App):

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_start(self):
        pass
        
    def on_stop(self):
        shutdown_server_thread()

    def build(self):
        swipe_book = SwipeBook()
        root_menu  = Menu()
        game_page  = GameLayout( swipe_book ) 

        swipe_book.add_page( root_menu )
        swipe_book.add_page( game_page )

        def play_game_callback():
            swipe_book.swipe_right()
            game_page.build_level()
            
        root_menu.play_game  = play_game_callback
        game_page.go_to_menu = swipe_book.swipe_left

        return swipe_book

if __name__ == '__main__':
    from kivy.core.window import Window

    # Manually set the window size to emulate the iphone screen.
    Window.size = 640, 960 # Note: 960 is too long for the monitor.


    try:
        DrawTiltApp().run()
    except:

        # If there's a crash, record the traceback to the file named 'error_log'.
        from traceback import format_exc
        from error_log import write_error_to_log

        write_error_to_log( format_exc() )

