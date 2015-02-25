from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from kivy.lang import Builder
Builder.load_file( 'libs/game/gamelayout.kv' )

from plyer import accelerometer
import pickle 

from drawing.drawingtoolkit import DrawingToolkit
from drawing.drawing_behaviors import dispatcher
from physics_interface.physics_interface import PhysicsInterface
import utils

class GameLayout(GridLayout):
    ##### Initialization
    def __init__(self, swipebook, *args, **kwargs):
        super( GameLayout, self ).__init__( *args, **kwargs )
        self.go_to_menu = lambda : None
        self.engine_running = False

        # Toggle methods for play and pause that toggle custom textures. 
        # Changing button.background_normal and button.background_down might be easier but didn't seem to work.
        self.play_toggle  = utils.texture_toggle( 'Resources/play_normal.png', 'Resources/play_down.png' )
        self.pause_toggle = utils.texture_toggle( 'Resources/pause_normal.png', 'Resources/pause_down.png' )
        
        # Create the physics interface.
        self.physics_interface = PhysicsInterface( accelerometer )
        self.add_widget( self.physics_interface )

        # Boolean used to allow build_level() to build the level only once.
        self.level_built = False

        # switches is populated by drawing_toolkit at runtime with various mode switches that can be checked to 
        # see what drawing mode is active (if any).
        self.switches = {} 
        self.drawing_toolkit = DrawingToolkit( self )
        self.active_mode = None

        # Make swipebook the parent of drawing_toolkit so that it's out of the gridlayout's automatic coordination.
        swipebook.add_widget_to_layer( self.drawing_toolkit, 'top' )
        self.swipebook = swipebook


    ##### Load the level
    def build_level( self ):
        # Build level.
        if not self.level_built:
            self.level_built = True # Build the level only one time.

            with open( 'level1', 'r' ) as f:
                game_objects = pickle.load( f )
                
            for obj in game_objects:
                obj.load_into_physics_interface( self.physics_interface )

            from physics_interface.game_objects.level_build.collision_handlers import setup_collision_handlers            
            setup_collision_handlers( self.physics_interface.space )

            # self.physcs_interface.game_objects are updated each timestep.
            self.physics_interface.game_objects += game_objects

    ##### Touch drawing
    def do_drawpt( self, pos ):
        # Boolean used to determine if a point is good to draw.
        # Return True if the position occurs not in the drawing panel, else False.
        return not self.drawing_toolkit.collide_point( *pos )

    # Subclass the on_touch methods to implement paint-like drawing interaction.
    # Look to self.switches to set the value of self.active_mode. Then dispatch to the mode's drawing functions.
    def on_touch_down(self, touch):
        super(type(self), self).on_touch_down( touch )
        if self.do_drawpt( touch.pos ):
            if self.engine_running: #play
                # Don't respond to any touches once 'play' has been pressed.
                pass
            else: #pause
                # self.switches contains entries like ( 'mode_name', mode_button ).
                # If a mode_button B is toggled, then B.state == 'down'.
                # Search self.switches for any 'down' buttons. 
                # Set self.active_mode to the first encounterd 'down' button.
                self.active_mode = None
                for mode_name, mode_button in self.switches.items():
                    if mode_button.state == 'down':
                        self.active_mode = mode_name
                        break

                # Initiate mode behavior based on which mode (if any) is active.
                self.mode_behavior( touch, 'touch_down' )

    def on_touch_move(self, touch):
        super(type(self), self).on_touch_move( touch )
        if self.engine_running: #play
            # Don't respond to any touches once 'play' has been pressed.
            pass
        else: #pause
            self.mode_behavior( touch, 'touch_move' )

    def on_touch_up(self, touch):
        super(type(self), self).on_touch_up( touch )
        if self.engine_running: #play
            # Don't respond to any touches once 'play' has been pressed.
            pass
        else: #pause
            self.mode_behavior( touch, 'touch_up' )
            self.active_mode = None

    def mode_behavior( self, touch, touch_stage ):
        """Dispatch function: call the right drawing function for the current mode."""
        dispatcher.dispatch( self, touch, touch_stage )

    ##### Animation Step
    # This method is scheduled or unscheduled for playing or pausing, respectively.
    def Step( self, dt ):
        # Step the physics interface forward one unit of time dt.
        self.physics_interface.step( dt )

        # Respond to any notifications from self.physics_interface
        for gameobject, notifications in self.physics_interface.get_notifications():
            for notice in notifications:

                if notice == 'Game Over':
                    self.reset()

                if notice == 'Remove':
                    gameobject.remove()

        self.physics_interface.clear_notifications()


    ##### Callbacks and helpers for the top-of-the-screen buttons ('menu', 'play', 'pause') (which are defined in gamelayout.kv).
    def reset( self ):
        """Reset the gamelayout to its default state."""
        # Unschedule self.Step().
        Clock.unschedule( self.Step )
        self.engine_running = False
        # Disable the accelerometer.
        accelerometer.disable()
        # Show the drawing toolkit.
        self.swipebook.add_widget_to_layer( self.drawing_toolkit, 'top' )

        # Reset pause and play to default states.
        self.play_toggle( self.ids.play_button, 'normal' )
        self.pause_toggle( self.ids.pause_button, 'down' )

    def start_animation( self ):
        """Start the gamelayout into its running state."""
        # Set pause and play to playing states.
        self.play_toggle( self.ids.play_button, 'down' )
        self.pause_toggle( self.ids.pause_button, 'normal' )

        # Hide the drawing toolkit.
        self.swipebook.remove_widget_from_layer( self.drawing_toolkit, 'top' )
        # Enable the accelerometer.
        accelerometer.enable()
        # Schedule self.Step()
        Clock.schedule_interval( self.Step, 1 / 60. )
        self.engine_running = True

        # Place a ball at the top of the level.
        self.physics_interface.add_circle(self.x+50, self.y+self.height, 15)


    # Texture loaders. 
    def get_menu_texture( self ):
        return utils.load_texture( 'Resources/menu.png' )
    def get_play_normal_texture( self ):
        return utils.load_texture( 'Resources/play_normal.png' )
    def get_pause_down_texture( self ):
        return utils.load_texture( 'Resources/pause_down.png' )

    def not_in_a_mode(self):
        return not any( [ b.state == 'down' for b in self.switches.values() ] )

    def menu_callback(self, button):
        if self.not_in_a_mode():
            self.go_to_menu()
            if self.engine_running:
                self.reset()

    def pause_callback(self, button):
        if self.not_in_a_mode() and self.engine_running:
            self.reset()
        else:
            # Kivy toggles, even though a response is unwanted. Force 'down' state.
            button.state = 'down'

    def play_callback(self, button):
        if self.not_in_a_mode() and not self.engine_running:
            self.start_animation()
        else:
            # Kivy toggles, even though a response is unwanted. Force 'down' state.
            button.state = 'down'



