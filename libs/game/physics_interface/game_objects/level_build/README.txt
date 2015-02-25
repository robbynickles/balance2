A GameObject offers the following public API:

  load_object_into_physics_interface - (method) place a GameObject into a physics_interface. Specifically, add the physics body, renderable object, and shape mapping that belong to a GameObject to a physics_interface.
  
  update - (method) update a GameObject's renderable object with the current data of its physics body.

  remove - (method) remove a GameObject completely from (removing any references to) the physics_interface it was loaded into.




To add a new game object to the level_builder do two things:

1. Subclass GameObject, implementing the methods necessary for the subclass O.
2. Add a drawing behavior* to the drawingtoolkit that creates the game_object and installs it to the physics interface.

* A drawing behavior consists of 3 things:
1. Button on the drawing toolkit - it activates the drawing mode, 
2. Drawing mode - the dispatcher dispatches to the mode's 3-stage drawing function whenever the drawingtoolkit is in that mode.
3. 3-stage drawing function - does three different things depending on which touch stage it is (touch_down, touch_move, touch_up).
   Results in a game_object being installed to the physics interface.

