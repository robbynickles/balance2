The gamelayout is part of the next immediate generation underneath the root widget. It contains the physics interface, buttons for pausing/playing the animation and navigation back to the menu screen and the drawing toolkit, which allows paint-style platform drawing. 

1)  It's in charge of asking for and releasing device data.

2)  It hosts the drawing toolkit and recieves touch input which result in drawings.

3)  It keeps a level_index which is what level-number the player is currently on, and knows how to load the current level.

4)  It schedules and unschedules the physics engine, responding to notifications from the physics_interface in between physics steps.


