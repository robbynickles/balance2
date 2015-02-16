### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_BALL = 1

types = [ COLLTYPE_DEFAULT, COLLTYPE_BALL ]

### List of all custom collision handlers
collision_handlers = []


### A handler is a 3-tuple containing both types and the callback function of the collsion.
def submit_collision_handler( type1, type2, func ):
    if type1 in types and type2 in types:
        global collision_handlers
        collision_handlers.append( (type1, type2, func ) )


### Populate collision_handlers with the game's custom collision handlers.
def ball_hit_platform( space, arbiter ):
    print "Ball contact with platform."

submit_collision_handler( COLLTYPE_DEFAULT, COLLTYPE_BALL, ball_hit_platform )


### Setup any collision handlers needed within the caller-supplied space.
def setup_collision_handlers( space ):
    for type1, type2, func in collision_handlers:
        # For now, there are no collisions that shouldn't be handled by physics.
        # So call the function in the post_solve phase.
        space.add_collision_handler(type2, type1, None, post_solve=func)

