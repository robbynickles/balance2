from _env import *

class Ball():
    def __init__( self, physics_interface, x, y, radius ):
        # Texture that will be used for any circles drawn.
        self.circle_texture = Image(join(dirname(__file__), 'Resources/circle.png'), mipmap=True).texture
        self._hue = 0

        # Add a circle body to the physics engine.
        body = cy.Body(100, 1e9)
        body.position = x, y
        circle = cy.Circle(body, radius)
        circle.elasticity = 0.6
        #circle.friction = 1.0
        circle.collision_type = COLLTYPE_BALL
        physics_interface.space.add(body, circle)
        

        self.body, self.shape = body, circle
            
        # Configure a canvas Rectangle with a texture to represent the circle body in the rendering environment.
        with physics_interface.canvas.before:
            self._hue = (self._hue + 0.01) % 1
            color = Color(self._hue, 1, 1, mode='hsv')
            rect = Rectangle(
                texture=self.circle_texture,
                pos=(physics_interface.x - radius, physics_interface.y + 2 * physics_interface.height - radius),
                size=(radius * 2, radius * 2))
        
        self.render_obj = radius, color, rect

    def update( self ):
        self.body.activate()
        p = self.body.position
        radius, color, rect = self.render_obj
        rect.pos = p.x - radius, p.y - radius
        rect.size = radius * 2, radius * 2

    def remove( self ):
        self.physics_interface.space.remove( self.body )
        self.physics_interface.space.remove( self.shape )
        
        radius, color, rect = self.render_obj
        self.physics_interface.canvas.before.remove( color ) 
        self.physics_interface.canvas.before.remove( rect ) 
