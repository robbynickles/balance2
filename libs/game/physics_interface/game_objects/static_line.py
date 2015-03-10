from _env import *

from level_build.static_line import PreStaticLine

class UserStaticLine( PreStaticLine ):
    end_points = ()

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

    def remove_endpoints( self ):
        for instr in self.end_points:
            self.physics_interface.canvas.remove( instr )
        self.end_points = ()

    def remove( self ):
        self.remove_endpoints()
        PreStaticLine.remove( self )
