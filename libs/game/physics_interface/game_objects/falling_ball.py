from _env import *

class Ball( GameObject ):
    _hue = 0

    def __init__( self, physics_interface, x, y, radius ):
        GameObject.__init__( self )
        self.pos            = x, y
        self.radius         = radius
        self.circle_texture = Image(join(dirname(__file__), 'Resources/circle.png'), mipmap=True).texture
        self.before         = True

        self.load_into_physics_interface( physics_interface )

    def build_phys_obj( self, space ):
        body          = cy.Body(100, 1e9)
        body.position = self.pos

        circle                = cy.Circle(body, self.radius)
        circle.elasticity     = 0.6
        #circle.friction       = 1.0
        circle.collision_type = COLLTYPE_BALL

        self.body             = body
        self.shapes          += [ circle ]
            
    def build_render_obj( self ):
        Ball._hue = (Ball._hue + 0.01) % 1
        color     = Color(Ball._hue, 1, 1, mode='hsv')
        rect      = Rectangle(
            texture=self.circle_texture,
            size=(self.radius * 2, self.radius * 2))
        
        self.render_obj = color, rect

    def update( self ):
        # Retrieve the physics body's postion.
        p = self.body.position

        # Make sure the ball is still in the dimensions of the gamelayout, which is the parent of physics_interface.
        # If not, game over and remove the ball.
        if not self.physics_interface.parent.collide_point( *p ):
            self.physics_interface.add_notification( self, 'Game Over' )
            self.physics_interface.add_notification( self, 'Remove' )
            return 
            
        # Update the renderable object.
        color, rect = self.render_obj
        rect.pos    = p.x - self.radius, p.y - self.radius
        rect.size   = self.radius * 2, self.radius * 2

        # Force the ball to stay awake.
        self.body.activate()

    # This is the method called when the ball hits a lava platform.
    def explode( self ):
        self.physics_interface.add_notification( self, 'Remove' )
