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

        def swipe_right():
            # Since no positions or dimensions are known until after build() completes, call build_level once everything is built
            # but before the player sees the game page.
            game_page.build_level()
            swipe_book.swipe_right()

        root_menu.play_game  = swipe_right
        game_page.go_to_menu = swipe_book.swipe_left

        return swipe_book

if __name__ == '__main__':
    DrawTiltApp().run()

