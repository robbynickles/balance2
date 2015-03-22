from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color, Rectangle, Line

from kivy.lang import Builder
Builder.load_file( 'libs/game/success_screen/success_screen.kv' )

class SuccessScreen(BoxLayout):

    def __init__(self, gamelayout, *args, **kwargs):
        super(SuccessScreen, self).__init__( *args, **kwargs )
        self.gamelayout = gamelayout

    def add_screen( self ):
        with self.gamelayout.canvas:
            self.screen_color = Color( 0,0,0,.8 )
            self.screen_rect  = Rectangle( pos=self.pos, size=self.size )

    def remove_screen( self ):
        self.gamelayout.canvas.remove( self.screen_color )
        self.gamelayout.canvas.remove( self.screen_rect )

        self.gamelayout.unlock_next_level()
        self.gamelayout.need_to_remove_success_screen = True
        self.gamelayout.reset()

    def retry_callback( self ):
        self.remove_screen()

    def next_callback( self ):
        self.remove_screen()
        self.gamelayout.level_index += 1
        self.gamelayout.build_level()


