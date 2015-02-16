from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

from os.path import dirname, join
from kivy.core.image import Image

from kivy.lang import Builder
Builder.load_file( 'libs/game/drawing/drawingtoolkit.kv' )

class DrawingToolkit( GridLayout ):
        
        ##### Initialization
        def __init__(self, gamelayout, *args, **kwargs):
            super( DrawingToolkit, self).__init__( *args, **kwargs )
            # Since gamelayout is in charge of managing the rendering/physics environment,
            # DrawingToolkit needs to communicate which drawing mode it's in. This will determine
            # gamelayout's interpretation of user touches.
            modes = set(['brush','line','curve','eraser'])
            for w in self.children:
                if type(w) == ToggleButton and w.name in modes:
                    gamelayout.switches[ w.name ] = w

            assert modes == set(gamelayout.switches.keys())
                    
            self.dragging = False

        ##### Load textures for panel buttons:
        def load_texture( self, fle ):
                return Image(join(dirname(__file__), fle), mipmap=True).texture
        def get_brush_texture( self ):
                return self.load_texture( 'Resources/brush.png' )
        def get_line_texture( self ):
                return self.load_texture( 'Resources/line.png' )
        def get_curve_texture( self ):
                return self.load_texture( 'Resources/curve.png' )
        def get_eraser_texture( self ):
                return self.load_texture( 'Resources/eraser.png' )
        def get_bomb_texture( self ):
                return self.load_texture( 'Resources/bomb.png' )
            
        ##### Implementation of draggable panel behavior:
        def on_touch_down(self, touch):
            super(type(self), self).on_touch_down( touch )
            if self.collide_point( *touch.pos ):
                # Don't move panel if using slider.
                #if not self.ids.grain_slider.collide_point( *touch.pos ):
                self.dragging = True

        def on_touch_move(self, touch):
            super(type(self), self).on_touch_move( touch )
            if self.dragging:
                self.x += touch.dx
                self.y += touch.dy

        def on_touch_up(self, touch):
            super(type(self), self).on_touch_up( touch )
            if self.dragging:
                self.dragging = False
            
        ##### Callbacks for panel buttons:
        def brush_pressed( self ):
            pass

        def line_pressed( self ):
            pass

        def curve_pressed( self ):
            pass

        def eraser_pressed( self ):
            pass

        def bomb_pressed( self ):
            pass

