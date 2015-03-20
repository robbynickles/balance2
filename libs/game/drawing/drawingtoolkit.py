from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

from os.path import dirname, join
from kivy.core.image import Image

from kivy.lang import Builder
Builder.load_file( 'libs/game/drawing/drawingtoolkit.kv' )

from libs.game.physics_interface.game_objects.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT, COLLTYPE_USERCURVE

class DrawingToolkit( GridLayout ):
        
        ##### Initialization
        def __init__(self, gamelayout, *args, **kwargs):
            super( DrawingToolkit, self).__init__( *args, **kwargs )

            # Populate gamelayout.switches so that gamelayout can dispatch to the active_mode's drawing function.
            #modes = set(['brush', 'line', 'eraser'])
            modes = set(['line', 'curve', 'eraser'])
            for w in [ self.ids.line, self.ids.curve, self.ids.eraser ]:
                gamelayout.switches[ w.name ] = w

            assert modes == set(gamelayout.switches.keys())

            self.gamelayout = gamelayout
            self.dragging = False

        def magnetize( self ):
            if self.ids.magnet.state == 'down':
                return True
            else:
                return False

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
            # Exit 'edit line' mode.  
            self.gamelayout.active_mode = None
            self.gamelayout.exit_edit_line_mode()

        def bomb_pressed( self ):
            # Exit 'edit line' mode.  
            self.gamelayout.active_mode = None
            self.gamelayout.exit_edit_line_mode()

            # Remove all user-drawn platforms.
            for shape, obj in self.gamelayout.physics_interface.smap.items():
                if shape.collision_type == COLLTYPE_USERPLAT or shape.collision_type == COLLTYPE_USERCURVE:
                        obj.remove()


