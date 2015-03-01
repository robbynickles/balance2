The gamelayout is part of the next immediate generation underneath the root widget. It contains the physics interface, buttons for pausing/playing the animation, a button for navigation back to the menu screen, and the drawing toolkit, which allows paint-style platform drawing. 

It's in charge of 
     1)  Asking for and releasing device data.

     2)  Hosting the drawing toolkit.
     
     3)  Recieving touch input which result in additions to the physics world.

     4)  Keeping a level index which is what level number the player is currently on.

     5)  Loading the current level.

     5)  Scheduling and unscheduling the physics step.
     
     6)  Responding to notifications from the physics_interface in between physics steps.


