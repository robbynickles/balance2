from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.lang import Builder
Builder.load_file( 'libs/level_selector/level_selector.kv' )

from level_button import LevelButton

LEVELS = 5

class LevelSelector(GridLayout):
    back = lambda : None

    def __init__(self, gamelayout, swipe_right, *args, **kwargs):
        super(LevelSelector, self).__init__( *args, **kwargs )

        # Populate a Gridlayout G with level thumbnail buttons.
        G = GridLayout( cols=5, padding=20, spacing=20 )
        for i in range( LEVELS ):
            G.add_widget( LevelButton( gamelayout, swipe_right, i + 1 ) )

        self.add_widget( G )

    def back_callback( self ):
        self.back()
