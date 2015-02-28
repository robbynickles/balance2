from _env import *

from level_build.static_line import PreStaticLine

class UserStaticLine( PreStaticLine ):

    def build_phys_obj( self, space ):
        PreStaticLine.build_phys_obj( self, space )
        for sh in self.shapes:
            sh.collision_type = COLLTYPE_USERPLAT

    def build_render_obj( self ):
        self.color = (0,1,0,1)
        PreStaticLine.build_render_obj( self )
