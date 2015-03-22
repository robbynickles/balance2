from _env import *

def distance( a, b ):
    return sum ( [ (x1-x2)**2 for x1,x2 in zip( a, b ) ] ) ** .5

def normalize( (x,y), (ox,oy), (xdim, ydim) ):
    return (x-ox)/xdim, (y-oy)/ydim

def absolute( (x,y), (ox,oy), (xdim,ydim) ):
    return x*xdim + ox, y*ydim + oy 

MAX_DIST = 40

class Editable( GameObject ):
    end_points = ()
    width      = 3

    color      = (1,1,1,1)
    colltype   = COLLTYPE_DEFAULT
    curve      = False

    def __init__( self, physics_interface, start, end ):
        GameObject.__init__( self )

        origin      = physics_interface.pos
        dim         = physics_interface.size

        self.set_start(origin, dim, start)
        self.set_end(origin, dim, end)

        # the thirdpt starts as the line midpoint.
        (x1,y1), (x2,y2) = start, end
        self.set_thirdpt( origin, dim, ( x1 + (x2-x1)/2., y1 + (y2-y1)/2.) ) 

        # self.points is a list of points that defines the segmentation. In the future, it's set by adjust_coordinates().
        self.points = [ start, end ]
        
        # Represent the object on the level-builder screen.
        self.load_into_physics_interface( physics_interface )


    ##### Implementation of GameObject methods
    def build_phys_obj( self, space ):
        for i in range( len(self.points) - 1 ):
            start, end = self.points[i], self.points[i+1]
            seg = cy.Segment(space.static_body, Vec2d( *start ), Vec2d( *end ), self.width)
            #seg.friction = 0.99
            seg.elasticity = 0.7
            seg.collision_type   = self.colltype
            self.shapes   += [ seg ]

    def build_render_obj( self ):
        color = Color( *self.color )
        line  = Line( points=reduce( lambda x,y: x+y, self.points ), width=self.width )
        self.render_obj = color, line

    ##### Necessary for Editable objects
    ##### Setters
    def set_start( self, origin, dim, pos ):   self.start = normalize( pos, origin, dim )
    def set_end( self, origin, dim, pos ):     self.end = normalize( pos, origin, dim )
    def set_thirdpt( self, origin, dim, pos ): self.thirdpt  = normalize( pos, origin, dim )

    ##### Getters
    def get_start( self ): 
        try:
            origin, dim = self.physics_interface.pos, self.physics_interface.size
            return absolute( self.start, origin, dim )
        except:# The gameobject isn't loaded. Return the normalized coordinates.
            return self.start

    def get_end( self ): 
        try:
            origin, dim = self.physics_interface.pos, self.physics_interface.size
            return absolute( self.end, origin, dim )
        except:
            return self.end

    def get_thirdpt( self ): 
        try:
            origin, dim = self.physics_interface.pos, self.physics_interface.size
            return absolute( self.thirdpt, origin, dim )
        except:
            return self.thirdpt


    ##### Helpers
    def near_start( self, pos ):  return distance( pos, self.get_start() ) <= MAX_DIST
    def near_end( self, pos ):    return distance( pos, self.get_end() ) <= MAX_DIST


    def length( self ):
        """ Return the length of the segmentation representing the line. """
        total = 0
        for i in range( len(self.points) - 1 ):
            start, end = self.points[i], self.points[i+1]
            total += distance( start, end )
        return total

    def update_render_obj( self ):
        self.remove_render_obj()
        self.build_render_obj()
        for instr in self.render_obj:
            self.physics_interface.canvas.add( instr )

    def remove_render_obj( self ):
        for instr in self.render_obj:
            self.physics_interface.canvas.remove( instr )

    def draw_endpoints( self ):
        start       = self.get_start()
        end         = self.get_end()
        radius      = 20
        with self.physics_interface.canvas:
            color   = Color( 1,1,1,1 )
            circle1 = Line( circle=(start[0], start[1], radius) )
            circle2 = Line( circle=(end[0], end[1], radius) )
        self.end_points = color, circle1, circle2

    def update_endpoints( self ):
        self.remove_endpoints()
        start  = self.get_start()
        end    = self.get_end()
        radius = 20
        with self.physics_interface.canvas:
            color   = Color( 1,1,1,1 )
            circle1 = Line( circle=(start[0], start[1], radius) )
            circle2 = Line( circle=(end[0], end[1], radius) )
        self.end_points = color, circle1, circle2

    def remove_endpoints( self ):
        for instr in self.end_points:
            self.physics_interface.canvas.remove( instr )
        self.end_points = ()

    def setup_for_editing( self, physics_interface ):
        self.remove()

        # Load back only the renderable.
        self.physics_interface = physics_interface
        self.build_render_obj()
        for instr in self.render_obj:
            self.physics_interface.canvas.add( instr )
            
        # Add endpoint circles to the render_obj.
        self.draw_endpoints()

    def tear_down_from_editing( self ):
        # Destroy the renderable object. (Now it's ready for loading.)
        self.remove_render_obj()
        # Destroy the endpoint circles.
        self.remove_endpoints()
        self.physics_interface = None

    def remove( self ):
        self.remove_endpoints()
        GameObject.remove( self )

