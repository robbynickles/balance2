from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file( 'libs/level_selector/level_selector.kv' )

from level_button import LevelButton
import utils

LEVELS = 5

class LevelSelector(GridLayout):
    back = lambda : None

    def __init__(self, gamelayout, swipe_right, *args, **kwargs):
        super(LevelSelector, self).__init__( *args, **kwargs )

        # Populate a Gridlayout G with level-thumbnail buttons.
        G = GridLayout( cols=3, 
                        spacing=20, 
                        padding=70, 
                        col_default_width=96+48+10, 
                        row_default_height=96+48+24+10 )

        for i in range( LEVELS ):
            G.add_widget( LevelButton( gamelayout, swipe_right, i + 1 ) )

        self.add_widget( G )

        self.level_buttons = G
        self.get_unlocked_levels = gamelayout.get_unlocked_levels

    def load( self ):
        # Lock or Unlock all buttons so that their state reflects the current game completion state.
        current_state = self.get_unlocked_levels()
        for b in self.level_buttons.children:
            b.unlock( current_state[ b.index - 1 ]  )

    def back_callback( self ):
        self.back()

    def get_back_texture( self ):
        return utils.load_texture( 'Resources/back.png' )
    def get_levels_texture( self ):
        return utils.load_texture( 'Resources/levels.png' )

