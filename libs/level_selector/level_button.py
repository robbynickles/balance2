from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ObjectProperty
from utils import load_texture
from kivy.lang import Builder
Builder.load_file( 'libs/level_selector/level_button.kv' )

class LevelButton( Button ):
    
    custom_texture = ObjectProperty( None )

    def on_press( self ):
        super( LevelButton, self).on_press()

        if self.unlocked:
            self.gamelayout.level_index = self.index
            self.gamelayout.build_level()
            self.swipe_right()

    def __init__(self, gamelayout, swipe_right, index, *args, **kwargs):
        super( LevelButton, self).__init__(*args, **kwargs)

        self.gamelayout  = gamelayout
        self.swipe_right = swipe_right
        self.index       = index


        self.custom_texture = load_texture( "Resources/{}.png".format( index ) )

        self.lock_screen = Rectangle()
        self.lock_color  = Color( 0,0,0,0 )
        self.canvas.add( self.lock_color )
        self.canvas.add( self.lock_screen )
    
    def unlock( self, unlocked ):
        self.canvas.remove( self.lock_color )
        self.canvas.remove( self.lock_screen )
        self.lock_screen = Rectangle(pos=(self.x+(self.width/2.0)-(48+24), self.y+(self.height/2.0)-(48+24+12)),
                                     size=(96+48,96+48+24) )

        self.unlocked = unlocked

        if unlocked:
            self.lock_color = Color( 0,0,0,0 )
        else:
            self.lock_color = Color( .5,0,0,.9 )            

        self.canvas.add( self.lock_color )
        self.canvas.add( self.lock_screen )
        
