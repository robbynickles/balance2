A drawing behavior consists of 3 things:

1. Button on the drawing toolkit - it activates the drawing mode, 

2. Drawing mode - the dispatcher dispatches to the mode's 3-stage drawing function whenever the drawingtoolkit is in that mode.

3. 3-stage drawing function - does three different things depending on which touch stage it is (touch_down, touch_move, touch_up).
   Usually results in a game_object being installed to or altered in the physics interface.
