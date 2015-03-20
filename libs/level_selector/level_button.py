from kivy.uix.button import Button

class LevelButton( Button ):
    
    def __init__(self, gamelayout, swipe_right, index, *args, **kwargs):
        self.size_hint_y = None

        super( LevelButton, self).__init__(*args, **kwargs)

        self.gamelayout  = gamelayout
        self.swipe_right = swipe_right
        self.index       = index

        # Load the textures at index to be backgrounds (normal and down).
        self.text = str( index )
        

    def on_press( self ):
        super( LevelButton, self).on_press()

        self.gamelayout.level_index = self.index
        self.gamelayout.build_level()
        self.swipe_right()



