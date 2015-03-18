#
## Warning: the types here should be a superset of the types in ../collision_handlers.py
#

### Physics collision types
COLLTYPE_DEFAULT   = 0
COLLTYPE_BALL      = 1
COLLTYPE_USERPLAT  = 2
COLLTYPE_USERCURVE = 3
COLLTYPE_LAVA      = 4
COLLTYPE_BUCKET    = 5


### List of all custom collision handlers
collision_handlers = []


### A handler is a 4-tuple containing both types and the callback function of the collsion, as well as the phase of collision detection that
# the callback should be applied.
def submit_collision_handler( type1, type2, func, phase='post' ): # Set post_solve as the default phase (after the 'normal' physics response).
    global collision_handlers
    collision_handlers += [ (type1, type2, func, phase) ]


### Setup any submitted collision handlers inside of the caller-supplied space.
def setup_collision_handlers( space ):
    for type1, type2, func, phase in collision_handlers:
        if phase == 'begin':
            space.add_collision_handler(type2, type1, None, begin=func )
        if phase == 'pre':
            space.add_collision_handler(type2, type1, None, pre_solve=func )
        if phase == 'post':
            space.add_collision_handler(type2, type1, None, post_solve=func )
        if phase == 'separate':
            space.add_collision_handler(type2, type1, None, separate=func )
