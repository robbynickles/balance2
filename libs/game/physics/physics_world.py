import cymunk as cy
from cymunk import Vec2d

from os.path import dirname, join
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.core.image import Image
from random import random
from kivy.lang import Builder

import utils

Builder.load_string('''
<Playground>:
    Label:
        text: ''
''')

class PhysicsWorld(Widget):

    # List of static-body segments that define the world's boundaries.
    cbounds = []
    
    # Correspondence table
    cmap    = {}
    
    ##### Initialization 
    def __init__(self, accelerometer, bounded=False, **kwargs):
        self.bounded = bounded

        # self._hue needs to be set before the Widget __init__ is called?
        self._hue = 0
        super( PhysicsWorld, self ).__init__(**kwargs)
        
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
        
        # Texture that will be used for any circles drawn.
        self.circle_texture = Image(join(dirname(__file__), 'circle.png'), mipmap=True).texture


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
        # of this method update the rendered object with any changes that have occurred to its pair in the physics world.
        #for obj in self.game_objects:
        #    obj.update()

        for body, obj in self.cmap.iteritems():
            body.activate()
            p = body.position
            radius, color, rect = obj
            rect.pos = p.x - radius, p.y - radius
            rect.size = radius * 2, radius * 2


    ##### Add
    # place a new object in the physics world, couple it with a rendered object. Make it available for update().
    def add_circle(self, x, y, radius):
        # Add a circle body to the physics engine.
        body = cy.Body(100, 1e9)
        body.position = x, y
        circle = cy.Circle(body, radius)
        circle.elasticity = 0.6
        #circle.friction = 1.0
        self.space.add(body, circle)
            
        # Configure a canvas Rectangle with a texture. This will represent the circle body in the rendering environment.
        with self.canvas.before:
            self._hue = (self._hue + 0.01) % 1
            color = Color(self._hue, 1, 1, mode='hsv')
            rect = Rectangle(
                texture=self.circle_texture,
                pos=(self.x - radius, self.y + 2 * self.height - radius),
                size=(radius * 2, radius * 2))

        # Correspondence table between circle bodies and how they appear.
        self.cmap[body] = (radius, color, rect)
        
    def add_static_line( self, (x1,y1), (x2,y2) ):
        #if self.collide_point(x1,y1) and self.collide_point(x2,y2):
        # 1) Create the physics object.
        print (x1,y1), (x2,y2) 
        seg = cy.Segment(self.space.static_body, Vec2d(x1,y1), Vec2d(x2,y2), 0.0)
        #seg.friction = 0.99
        seg.elasticity = 0.7
        self.space.add_static( seg )
        
        # 2) Create the renderable object.
        with self.canvas:
            Color(1, 0, 0, 1)
            Line( points=[ x1,y1,x2,y2 ] )
