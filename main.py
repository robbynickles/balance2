from kivy.app import App

from libs.swipebook import SwipeBook
from libs.menu.menu import Menu
from libs.game.gamelayout import GameLayout
from libs.level_selector.level_selector import LevelSelector

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
        swipe_book     = SwipeBook()
        root_menu      = Menu()
        game_page      = GameLayout( swipe_book ) 
        level_selector = LevelSelector( game_page, swipe_book.swipe_right )

        swipe_book.add_page( root_menu )
        swipe_book.add_page( level_selector )
        swipe_book.add_page( game_page )

        root_menu.play_game  = swipe_book.swipe_right
        level_selector.back  = swipe_book.swipe_left
        game_page.go_to_menu = swipe_book.swipe_left

        return swipe_book

if __name__ == '__main__':
    from kivy.core.window import Window

    from plyer import utils
    if utils._determine_platform() == 'macosx':
        # Manually set the window size to emulate the iphone screen.
        #Window.size = int(640/1.5), int(960/1.5)
        Window.size = 640, 960


    try:
        DrawTiltApp().run()
    except:

        # If there's a crash, write the traceback to stdout as well as to the file named 'error_log/error_log.txt'.
        from traceback import format_exc
        from error_log import error_log

        print format_exc()

        # Logging the error to a file is for the benefit of
        # debugging on iOS, where there isn't really a stdout.
        error_log.append_log( format_exc() )

