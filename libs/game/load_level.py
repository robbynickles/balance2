import pickle 

from physics_interface.game_objects.level_build.collision_handlers import setup_collision_handlers            

def remove_current_level( physics_interface ):
    for obj in physics_interface.get_game_objects():
        obj.remove()

def load_level( level_name, physics_interface ):
    try:
        with open( level_name, 'r' ) as f:
            game_objects = pickle.load( f )
    except IOError:
        # No such file.
        return
    
    # Load each gameobject into the physics_interface.
    for obj in game_objects:
        obj.load_into_physics_interface( physics_interface )

    # Setup any collision handlers that the gameobjects have submitted.
    setup_collision_handlers( physics_interface.space )

def remove_current_load_next( index, physics_interface ):
    remove_current_level( physics_interface )

    # Level files are found in the root directory in a directory called levels. 
    # The naming convention is levelX where X is the level number.
    level_name = 'levels/level{}'.format( index )

    load_level( level_name, physics_interface )
    
    
