from cymunk import Vec2d

from kivy.uix.widget import Widget
from kivy.lang import Builder

import utils
from game_objects.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT
from game_objects.static_line import StaticLine
from game_objects.falling_ball import Ball

Builder.load_string('''
<Playground>:
    Label:
        text: ''
''')

class PhysicsInterface(Widget):

    # List of static-body segments that define the world's boundaries.
    cbounds = []
    
    ##### Initialization 
    def __init__(self, accelerometer, bounded=False, **kwargs):
        super( PhysicsInterface, self ).__init__(**kwargs)
        self.bounded = bounded
        
        # Accelerometer is passed in by the parent. self.parent (game_layout) is responsible for managing the device.
        # In this class, you only have to ask for the current acceleration data.
        self.accelerometer = accelerometer

        # Setup the running environment of the physics engine.
        # Create the physics world and set variables that determine how the engine runs. Calling self.space.step(dt) after this
        # will move the simulation forward a dt amount of time, applying velocities to objects, responding to collisions between objects, etc.
        utils.init_physics( self )

        # Update the bounds (which exist in the physics world) dynamically to fit the dimensions 
        # of the current window (which exists in the rendering environment).
        self.bind( size=lambda *args: utils.update_bounds(self, *args), pos= lambda *args: utils.update_bounds(self, *args) )
        
        # List of game objects that need updating.
        self.game_objects = []

        # Mapping from shape to game_object - sometimes the physics engine needs to talk to game objects.
        # So self.smap is a set of back references such that if a game object G is initialized with 
        # a shape S, self.smap[ S ] == G.
        self.smap = {}

        # Notifications that need responding to.
        # A notification consists of a (k,v) pair where k is the gameobject from which the notification emanated,
        # and v is list of unique notifications (meaning only the first submission of a notification N is accepted).
        self.notifications = {}

        
    ##### Notification system
    # The notifications system is used when a gameobject needs to create a game-level event. For example, 'game overs', 'game wins', 'object 
    # removals' are all triggered by collisions, but collision handlers can't complete those actions. 
    # For example, pausing the simulation, loading the next level, or even just removing a body from the physics engine, are all things that
    # collision handlers can't do. 
    # So all the collision handler needs to do is create a notification, and the gamelayout will deal with it at the end of the physics step.

    # The notifications system has three methods: 
    # 1) add_notification
    # 2) get_notifications
    # 3) clear_notifications
    # The first is generally used from inside collision handler callbacks, while the latter two are used by the gamelayout
    # when checking if any notifications need responding to between physics steps.
    def add_notification( self, gameobject, msg ):
        if self.notifications.has_key( gameobject ):
            submitted_messages = self.notifications[ gameobject ]
            if submitted_messages.count( msg ) == 0:
                self.notifications[ gameobject ] += [ msg ]
        else:
            self.notifications[ gameobject ] = [ msg ]

    def get_notifications( self ):
        return self.notifications.iteritems()

    def clear_notifications( self ):
        self.notifications = {}


    ##### Step
    # The main physics step. Forward the physics world one unit of time dt.
    def step(self, dt):
        # Update the gravity vector (change its angle) with accelerometer data.
        x_acc, y_acc, z_acc = self.accelerometer.acceleration[:3]
        self.space.gravity = ( x_acc * self.world_gravity, y_acc * self.world_gravity )

        self.space.step(dt)#1 / 60.) # Why not make this dt?
        # Canvas_before will have already setup the canvas objects up with their appearances. So update_objects will now move those 
        # canvas objects to their current location within the physics world. Later, kivy will automatically render all canvas objects.
        self.update_objects()


    ##### Update
    # Retrieve from the physics world the coordinates of objects and update the corresponding rendered objects that represent them
    # with the new information.
    def update_objects(self):
        # Once an object has been placed in the world, the physics will interact with it, potentially moving it or changing it. It's the job 
        # of this method to update the rendered object with any changes that have occurred to its pair in the physics world.
        for obj in self.game_objects:
            obj.update()

    ##### Methods that add objects
    # place a new object in the physics world, couple it with a rendered object. Make it available for update_objects() if it needs to.
    def add_circle(self, x, y, radius):
        self.game_objects += [ Ball( self, x, y, radius ) ]

    # For use in creating user-drawn lines.
    def add_user_static_line( self, (x1,y1), (x2,y2) ):
        StaticLine( self, (x1, y1), (x2, y2), COLLTYPE_USERPLAT, smap=self.smap)

    def add_user_freehand_line( self, line_points ):
        # line_points = smooth( line_points )
        for i in range( 0, len(line_points) - 3, 2 ):
            a,b,c,d = line_points[i:i+4]
            self.add_user_static_line( (a,b), (c,d) )

