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
            # Populate gamelayout.switches so that gamelayout can dispatch to the active_mode's drawing functions.
            #modes = set(['brush', 'line', 'eraser'])
            modes = set(['line', 'eraser'])
            for w in self.children:
                if type(w) == ToggleButton and w.name in modes:
                    gamelayout.switches[ w.name ] = w

            assert modes == set(gamelayout.switches.keys())

            self.gamelayout = gamelayout
            self.dragging = False


        ##### Texture loaders for panel buttons
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
            
        ##### Implementation of draggable panel behavior
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
            for shape, obj in self.gamelayout.physics_world.smap.items():
                obj.remove()
            self.gamelayout.physics_world.smap = {}

