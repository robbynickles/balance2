#import cymunk as cy
from cymunk import Vec2d

#from os.path import dirname, join
#from kivy.clock import Clock
#from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
#from kivy.core.image import Image
#from random import random
from kivy.lang import Builder

import utils
from game_objects.static_line import StaticLine
from game_objects.falling_ball import Ball

Builder.load_string('''
<Playground>:
    Label:
        text: ''
''')

class PhysicsWorld(Widget):

    # List of static-body segments that define the world's boundaries.
    cbounds = []
    
    ##### Initialization 
    def __init__(self, accelerometer, bounded=False, **kwargs):
        super( PhysicsWorld, self ).__init__(**kwargs)
        self.bounded = bounded
        
        # Accelerometer is passed in by the parent. self.parent (game_layout) is responsible for managing the device.
        # In this class, you only have to ask for the current acceleration data.
        self.accelerometer = accelerometer

        # Setup the running environment of the physics engine.
        # Create the physics world and set variables that determine how the engine runs. Calling self.space.step(dt) after this
        # will move the simulation forward a dt amount of time, applying velocities to objects, responding to collisions between objects.
        utils.init_physics( self )

        # Update the bounds (which exist in the physics world) dynamically to fit the dimensions 
        # of the current window (which exists in the rendering environment).
        self.bind( size=lambda *args: utils.update_bounds(self, *args), pos= lambda *args: utils.update_bounds(self, *args) )
        
        # List of game objects that need updating.
        self.game_objects = []


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

    ##### Add
    # place a new object in the physics world, couple it with a rendered object. Make it available for update_objects() if it needs to.
    def add_circle(self, x, y, radius):
        self.game_objects.append(  Ball( self, x, y, radius )  )
        
    def add_static_line( self, (x1,y1), (x2,y2) ):
        StaticLine( self, (x1, y1), (x2, y2) )
