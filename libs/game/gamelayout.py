from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from kivy.lang import Builder
Builder.load_file( 'libs/game/gamelayout.kv' )

from plyer import accelerometer, gyroscope

from success_screen.success_screen import SuccessScreen

from drawing.drawingtoolkit import DrawingToolkit
from drawing.drawing_behaviors import dispatcher
from physics_interface.physics_interface import PhysicsInterface

from physics_interface.game_objects.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT, COLLTYPE_USERCURVE
from cymunk import Vec2d

import utils, load_level

LEVELS = 5

class GameLayout(GridLayout):
    ##### Initialization
    def __init__(self, swipebook, *args, **kwargs):
        super( GameLayout, self ).__init__( *args, **kwargs )

        # Function called when the player hits the menu button.
        self.go_to_menu = lambda : None

        # self.engine_running is True whenever the self.Step is scheduled, and false otherwise.
        self.engine_running = False

        # Toggle methods for play and pause that toggle custom textures. 
        # Changing button.background_normal and button.background_down might be easier but didn't seem to work.
        self.play_toggle  = utils.texture_toggle( 'Resources/play_normal.png', 'Resources/play_down.png' )
        self.pause_toggle = utils.texture_toggle( 'Resources/pause_normal.png', 'Resources/pause_down.png' )
        
        # Create the physics interface.
        self.physics_interface = PhysicsInterface( accelerometer, gyroscope )
        self.add_widget( self.physics_interface )
        
        # self.switches contains entries like ( 'mode_name', mode_button ), 
        # where mode_button is one of DrawingToolkit's toggle buttons, 
        # and mode_name is its name as it's known to the dispatcher.
        # If a mode_button B is toggled, then B.state == 'down'.
        self.switches = {} 

        # DrawingToolkit populates self.switches with references to its toolkit panel toggle buttons. 
        # When the player toggles a button, its state is visible in self.switches. Then, the dispatcher will know
        # which drawing function to call when it recieves new touch data.
        self.drawing_toolkit = DrawingToolkit( self )
        self.active_mode = None

        # Make swipebook the parent of drawing_toolkit so that it's out of the gridlayout's automatic coordination.
        self.toolkit_loaded                = False
        self.success_screen_loaded         = False
        self.need_to_remove_success_screen = False
        self.in_success_screen             = False
        self.swipebook = swipebook

        # Reference to the line being edited in 'line edit' mode.
        self.target_line = None

        # self.build_level() builds the level stored in the file named "levels/level{self.level_index}".
        self.level_index  = 1

        # Keep track of which levels have been unlocked.
        # By default, only the first level is unlocked.
        self.levels_unlocked = [True] + [False for i in range( LEVELS - 1 )]

        # Variable used to store the level_index of the level currently built.
        self.level_loaded = 0

        # Enable the device.
        accelerometer.enable()

    def unlock_next_level( self ):
        self.levels_unlocked[ self.level_index ] = True

    def get_unlocked_levels( self ):
        return self.levels_unlocked

    ##### Load the current level
    def build_level( self ):
        # Load the drawing_toolkit
        if not self.toolkit_loaded:
            self.toolkit_loaded = True
            self.drawing_toolkit.pos = self.x+self.width/2., self.y+self.height/2.
            #self.drawing_toolkit.pos = self.x+self.width, self.y+self.height
            self.swipebook.add_widget_to_layer( self.drawing_toolkit, 'top' )

        # Load the success screen.
        if not self.success_screen_loaded:
            self.success_screen_loaded = True
            self.success_screen = SuccessScreen( self, pos=self.pos, size=self.size )

        # Only load the level when the level_index has changed.
        if self.level_loaded != self.level_index:
            load_level.remove_current_load_next( self.level_index, self.physics_interface )
            self.level_loaded = self.level_index

    ##### Touch drawing
    def do_drawpt( self, pos ):
        # Boolean used to determine if a point is good to draw.
        # Return True if the position occurs not in the drawing panel, else False.
        return not self.drawing_toolkit.collide_point( *pos )

    QUICK = .2
    SHORT = 10
    # This method is best used in on_release, that way everything is known about the touch.
    def quick_and_short( self, touch ):
        "True if a touch is a quick tap with little movement."
        return \
            touch.time_end - touch.time_start <= self.QUICK and utils.distance( touch.pos, touch.opos ) <= self.SHORT

    # Exit edit-line mode.
    def exit_edit_line_mode( self ):
        self.active_mode = None

        if self.target_line:
            # Prepare target_line to be loaded back into the game normally.
            self.target_line.tear_down_from_editing()

            # Load target_line normally.
            self.target_line.load_into_physics_interface( self.physics_interface )

            # Remove the reference to it.
            self.target_line = None

    # Subclass the on_touch methods to implement paint-like drawing interaction.
    # Look to self.switches to set the value of self.active_mode. Then dispatch to the mode's drawing functions.
    def on_touch_down(self, touch):
        super(type(self), self).on_touch_down( touch )
        if self.do_drawpt( touch.pos ):
            if self.engine_running: #play
                # Don't respond to any touches once 'play' has been pressed.
                pass
            else: #pause

                if touch.is_double_tap:
                    # A double-tap exits 'edit line' mode.
                    self.exit_edit_line_mode()
        
                if self.active_mode != 'edit line':
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

            # A quick tap on a user-platform enters into edit-line mode.
            if self.active_mode != 'eraser' and self.quick_and_short( touch ):
                MAX_DIST = 40

                # Query the space for the closest user-platform within a radius of MAX_DIST from the touch position.
                shape    = self.physics_interface.space.nearest_point_query_nearest( Vec2d( *touch.pos ), 
                                                                                     MAX_DIST, 
                                                                                     COLLTYPE_USERPLAT | COLLTYPE_USERCURVE )

                # If a user-platform is tapped, start 'edit line' mode targeted at the found platform.
                if shape and (shape.collision_type == COLLTYPE_USERPLAT or shape.collision_type == COLLTYPE_USERCURVE):
                    
                    # Exit edit line mode for the currently targeted line, if it exists.
                    self.exit_edit_line_mode()
                    self.active_mode = 'edit line'
                    self.target_line = self.physics_interface.smap[ shape ]
                    self.target_line.setup_for_editing( self.physics_interface )

            self.mode_behavior( touch, 'touch_up' )

    def mode_behavior( self, touch, touch_stage ):
        """Dispatch function: call the current mode's drawing function."""
        dispatcher.dispatch( self, touch, touch_stage )


    ##### Animation Step
    # This method is scheduled or unscheduled for playing or pausing, respectively.
    def Step( self, dt ):
        # Step the physics interface forward one unit of time dt.
        self.physics_interface.step( dt )

        # Respond to any notifications from self.physics_interface.
        for gameobject, notifications in self.physics_interface.get_notifications():
            for notice in notifications:

                if notice == 'Game Over':
                    self.reset()

                if notice == 'Level Complete':
                    try:
                        self.swipebook.add_widget_to_layer( self.success_screen, 'top' )
                        self.success_screen.set_score( self.physics_interface.length_of_user_lines() )
                        self.success_screen.add_screen()
                        self.in_success_screen = True
                    except:
                        # Under certain assumptions, an error here means self.success_screen is already a child of self.swipebook.
                        pass


                if notice == 'Remove':
                    try:
                        gameobject.remove()
                    except:
                        pass

        self.physics_interface.clear_notifications()


    ##### Callbacks and helpers for the top-of-the-screen buttons ('menu', 'play', 'pause') (which are defined in gamelayout.kv).
    def reset( self ):
        """Reset the gamelayout to its default state."""
        # Unschedule self.Step().
        Clock.unschedule( self.Step )
        self.engine_running = False

        if self.need_to_remove_success_screen:
            self.swipebook.remove_widget_from_layer( self.success_screen, 'top' )
            self.need_to_remove_success_screen = False

        # Show the drawing toolkit.
        self.swipebook.add_widget_to_layer( self.drawing_toolkit, 'top' )
        #self.swipebook.add_widget_to_layer( self.drawing_toolkit, 'top' )

        # Reset pause and play to default states.
        self.play_toggle( self.ids.play_button, 'normal' )
        self.pause_toggle( self.ids.pause_button, 'down' )

        # Stop Level
        self.physics_interface.stop_level()

    def start_animation( self ):
        """Start the gamelayout into its running state."""
        # Set pause and play to playing states.
        self.play_toggle( self.ids.play_button, 'down' )
        self.pause_toggle( self.ids.pause_button, 'normal' )

        # Exit edit-line mode.
        self.exit_edit_line_mode()

        # Hide the drawing toolkit.
        self.swipebook.remove_widget_from_layer( self.drawing_toolkit, 'top' )

        # Schedule self.Step()
        Clock.schedule_interval( self.Step, 1 / 60. )
        self.engine_running = True

        # Start Level
        self.physics_interface.start_level()

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
        if self.quick_and_short( button.last_touch ) and not self.in_success_screen:
            # Disable the devices.
            accelerometer.disable()

            self.go_to_menu()
            if self.engine_running:
                self.reset()

    def pause_callback(self, button):
        t = button.last_touch
        if self.quick_and_short( button.last_touch ) and not self.in_success_screen and \
           self.engine_running:
            self.reset()
        else:
            # Kivy toggles, even though a response is unwanted. Force 'down' state.
            button.state = 'down'

    def play_callback(self, button):
        t = button.last_touch
        if self.quick_and_short( button.last_touch ) and not self.in_success_screen and \
           not self.engine_running:
            self.start_animation()
        else:
            # Kivy toggles, even though a response is unwanted. Force 'down' state.
            button.state = 'down'



