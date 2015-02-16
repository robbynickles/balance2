import cymunk as cy
from cymunk import Vec2d

from game_objects.collision_handlers import setup_collision_handlers

def init_physics(obj):
    # create the space for physics simulation
    obj.space = space = cy.Space()
    space.iterations = 30
    obj.world_gravity = 700
    space.gravity = (0, -obj.world_gravity)
    space.sleep_time_threshold = 0.5
    space.collision_slop = 0.5

    # Add all the necessary collision handlers to the physics world.
    setup_collision_handlers( space )

    # Create 4 static-body segments that will act as a bounds, initializing them with coordinates that 
    # will change based on the dimensions of the window.
    if obj.bounded:
        for x in xrange(4):
            seg = cy.Segment(space.static_body,
                             cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
            seg.elasticity = 0.6
            #seg.friction = 1.0
            obj.cbounds.append(seg)
            space.add_static(seg)


def update_bounds(obj, *largs):
    # obj needs to have cbounds, a boolean named bounded and it needs to have a space (cymunk physics world).
    if obj.bounded:
        assert(len(obj.cbounds) == 4)
        a, b, c, d = obj.cbounds
        x0, y0 = obj.pos
        x1 = obj.right
        y1 = obj.top
        
        obj.space.remove_static(a)
        obj.space.remove_static(b)
        obj.space.remove_static(c)
        obj.space.remove_static(d)
        a.a = (x0, y0)
        a.b = (x1, y0)
        b.a = (x1, y0)
        b.b = (x1, y1)
        c.a = (x1, y1)
        c.b = (x0, y1)
        d.a = (x0, y1)
        d.b = (x0, y0)
        obj.space.add_static(a)
        obj.space.add_static(b)
        obj.space.add_static(c)
        obj.space.add_static(d)
