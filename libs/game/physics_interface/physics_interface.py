from kivy.uix.widget import Widget

from kivy.lang import Builder
Builder.load_string('''
<Playground>:
    Label:
        text: ''
''')

import utils
from game_objects.static_line import UserStaticLine
from game_objects.static_curve import UserStaticCurve
from game_objects.falling_ball import Ball

from math import sin, cos

class PhysicsInterface(Widget):

    # List of static-body segments that define the world's boundaries.
    cbounds = []
    
    ##### Initialization 
    def __init__(self, accelerometer, gyroscope, bounded=False, **kwargs):
        super( PhysicsInterface, self ).__init__(**kwargs)
        self.bounded = bounded
        
        # Devices are passed in by the parent. self.parent (game_layout) is responsible for managing devices.
        # In this class, you only have to ask for the current device data.
        self.accelerometer = accelerometer
        self.gyroscope = gyroscope

        # Setup the running environment of the physics engine.
        # Create the physics world and set variables that determine how the engine runs. Calling self.space.step(dt) after this
        # will move the simulation forward a dt amount of time, applying velocities to objects, responding to collisions between objects, etc.
        utils.init_physics( self )

        # Update the bounds (which exist in the physics world) dynamically to fit the dimensions 
        # of the current window (which exists in the rendering environment).
        self.bind( size=lambda *args: utils.update_bounds(self, *args), 
                   pos= lambda *args: utils.update_bounds(self, *args) )
        
        # Mapping from shape to game_object - sometimes the physics engine needs to talk to game objects.
        # So self.smap is a set of back references such that if a game object G has a shape S, self.smap[ S ] == G.
        self.smap = {}

        self.user_lines = []

        # Notifications that need responding to.
        # A notification consists of a (k,v) pair where k is the gameobject from which the notification emanated,
        # and v is list of unique notifications (meaning only a gameobject's first submission of a notification N is accepted).
        self.notifications = {}


    # Getter method for the current set of game objects in this physics interface.
    def get_game_objects( self ):
        """Return a list of all the physics_interface's game_objects."""
        return set( self.smap.values() )

        
    ##### Notification system
    # When a gameobject needs to create a game-level event, for example, pause the simulation, load the next level, or remove a body 
    # from the physics engine, it creates a notification, which the gamelayout will respond to between physics steps.

    # The notifications system has three methods: 
    # 1) add_notification
    # 2) get_notifications
    # 3) clear_notifications
    # The first is used from inside collision handler callbacks, while the latter two are used by the gamelayout.

    def add_notification( self, gameobject, msg ):
        if self.notifications.has_key( gameobject ):
            submitted_messages = self.notifications[ gameobject ]
            if submitted_messages.count( msg ) == 0:
                self.notifications[ gameobject ] += [ msg ]
        else:
            self.notifications[ gameobject ] = [ msg ]

    def get_notifications( self ):
        return self.notifications.items()

    def clear_notifications( self ):
        self.notifications = {}

    ##### Acceleromter ---> Tilt mapping helpers.
    def normalize( self, x ):
        "Normalize x (get the direction of the vector)."
        return abs(x) / x

    def combine( self, a, b ):
        "Combine a and b to form a Pythagorean diagonal."
        return ( a**2 + b**2 ) ** .5
        
    def transfer_acceleration( self, z_acc ):
        "Return a function that adds z-axis acceleration to an axis."
        A = 1 - z_acc**2
        def add_z( acc ):
            return self.normalize( acc ) * self.combine( acc, (acc**2/A)*abs(z_acc) )
        return add_z

    ##### Step
    # The main physics step. 
    def step(self, dt):
        # Map the real-world gravity vector to the game's gravity vector.
        # The mathematical limitations are such that if x_acc and y_acc are close to zero,
        # it's not known how to tilt gravity. Probably want to pause the game and inform the player
        # that whenever the phone goes perfectly flat, the game will pause. (Modern take on the buzzer
        # when you shake the pinball machine.)
        x_acc, y_acc, z_acc = self.accelerometer.acceleration[:3]
        try:
            add_z              = self.transfer_acceleration( z_acc )
            self.space.gravity = ( add_z( x_acc ) * self.world_gravity, 
                                   add_z( y_acc ) * self.world_gravity )
        except:
            # Probably a ZeroDivision error because either the device-motion updates haven't started,
            # or the phone is flat (z^2 = 1 ====> A = 0 ====> x^2/A ====> undefined )
            pass

        # Forward the physics world one unit of time dt in sub_steps sub steps.
        sub_steps = 10
        for i in range( sub_steps ):
            self.space.step(dt / sub_steps)

        # Update the rendered world to match the physics world (which has just moved forward in time).
        self.update_objects()


    ##### Update
    def update_objects(self):
        # Once an object has been placed in the world, the physics will interact with it, potentially moving it or changing it. It's the job 
        # of this method to update the rendered object with any changes that have occurred to the physics object.
        for obj in self.get_game_objects():
            obj.update()

        
    ##### Start/Stop level
    # Drop a ball at the top-left corner.
    def start_level( self ):
        self.add_circle(self.parent.x+50, self.parent.y+self.parent.height-20, 15)

    # Destroy the ball.
    def stop_level( self ):
        for obj in self.get_game_objects():
            if isinstance( obj, Ball ):
                try:
                    obj.remove()
                except:
                    pass


    # Return the total length of line that the user has drawn.
    def length_of_user_lines( self ):

        # Adjust self.user_lines so that it reflects the current set of gameobjects.
        current_objects = self.get_game_objects()
        current_lines   = []
        for l in self.user_lines:
            if l in current_objects:
                current_lines += [ l ]

        self.user_lines = current_lines

        return sum( [ l.length() for l in self.user_lines ] )

    ##### Methods that add game objects
    def add_circle(self, x, y, radius):
        Ball( self, x, y, radius )

    def add_user_static_line( self, (x1,y1), (x2,y2) ):
        self.user_lines += [ UserStaticLine( self, (x1, y1), (x2, y2) ) ]

    def add_user_static_curve( self, (x1,y1), (x2,y2) ):
        self.user_lines += [ UserStaticCurve( self, (x1, y1), (x2, y2) ) ]


    # No good. Ball doesn't roll; raw vertices are too jagged.
    def add_user_freehand_line( self, line_points ):
        # line_points = smooth( line_points )
        for i in range( 0, len(line_points) - 3, 2 ):
            a,b,c,d = line_points[i:i+4]
            self.add_user_static_line( (a,b), (c,d) )

