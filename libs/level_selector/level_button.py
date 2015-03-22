from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ObjectProperty
from utils import load_texture
from kivy.lang import Builder
Builder.load_file( 'libs/level_selector/level_button.kv' )

class LevelButton( Button ):
    
    custom_texture = ObjectProperty( None )
    unlocked       = False

    def on_press( self ):
        super( LevelButton, self).on_press()
        if self.unlocked:
            self.gamelayout.level_index = self.index
            self.gamelayout.build_level()
            self.swipe_right()

    def __init__(self, gamelayout, swipe_right, index, *args, **kwargs):
        super( LevelButton, self).__init__(*args, **kwargs)

        self.gamelayout     = gamelayout
        self.swipe_right    = swipe_right
        self.index          = index
        self.custom_texture = load_texture( "Resources/{}.png".format( index ) )

        self.lock_screen    = Rectangle()
        self.lock_color     = Color( 0,0,0,0 )
        self.canvas.add( self.lock_color )
        self.canvas.add( self.lock_screen )

    def unlock( self, unlocked, score ):
        self.canvas.remove( self.lock_color )
        self.canvas.remove( self.lock_screen )

        if unlocked:
            self.lock_color      = Color( 0,0,0,0 )
            self.ids.score.text  = "Score: {}".format( round(score,2) )
        else:
            self.lock_color = Color( .5,0,0,.9 )            

        self.lock_screen = Rectangle(pos=(self.x+(self.width/2.0)-(48+24), self.y+(self.height/2.0)-(48+24+12)),
                                     size=(96+48,96+48+24) )
        self.canvas.add( self.lock_color )
        self.canvas.add( self.lock_screen )

        self.unlocked = unlocked
        
