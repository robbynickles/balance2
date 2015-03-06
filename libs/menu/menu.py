from kivy.uix.gridlayout import GridLayout

from kivy.lang import Builder
Builder.load_file( 'libs/menu/menu.kv' )

class Menu(GridLayout):
    play_game = lambda : None

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__( *args, **kwargs )

    def play_callback( self ):
        self.play_game()
