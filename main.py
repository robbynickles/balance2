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
        self.game_page  = GameLayout( swipe_book ) # make an instance var for later access in on_start.

        swipe_book.add_page( root_menu )
        swipe_book.add_page( self.game_page )

        root_menu.play_game  = swipe_book.swipe_right
        self.game_page.go_to_menu = swipe_book.swipe_left

        return swipe_book

if __name__ == '__main__':
    DrawTiltApp().run()

