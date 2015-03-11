from _env import *

from level_build.static_line import PreStaticLine

class UserStaticLine( PreStaticLine ):
    end_points = ()
    width      = 3.

    def build_phys_obj( self, space ):
        PreStaticLine.build_phys_obj( self, space )
        for sh in self.shapes:
            sh.collision_type = COLLTYPE_USERPLAT

    def build_render_obj( self ):
        self.color = (0,1,0,1)
        PreStaticLine.build_render_obj( self )

    def draw_endpoints( self ):
        start  = self.points[:2]
        end    = self.points[2:]
        radius = 20
        with self.physics_interface.canvas:
            color   = Color( 1,1,1,1 )
            circle1 = Line( circle=(start[0], start[1], radius) )
            circle2 = Line( circle=(end[0], end[1], radius) )
        self.end_points = color, circle1, circle2

    def setup_for_editing( self, physics_interface ):
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

    def update_render_obj( self ):
        self.remove_render_obj()
        self.build_render_obj()
        for instr in self.render_obj:
            self.physics_interface.canvas.add( instr )

    def update_endpoints( self ):
        self.remove_endpoints()
        start  = self.points[:2]
        end    = self.points[2:]
        radius = 20
        with self.physics_interface.canvas:
            color   = Color( 1,1,1,1 )
            circle1 = Line( circle=(start[0], start[1], radius) )
            circle2 = Line( circle=(end[0], end[1], radius) )
        self.end_points = color, circle1, circle2

    def remove_render_obj( self ):
        for instr in self.render_obj:
            self.physics_interface.canvas.remove( instr )

    def remove_endpoints( self ):
        for instr in self.end_points:
            self.physics_interface.canvas.remove( instr )
        self.end_points = ()

    def remove( self ):
        self.remove_endpoints()
        PreStaticLine.remove( self )
