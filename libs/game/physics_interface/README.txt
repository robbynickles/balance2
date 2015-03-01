The physics interface is the widget that contains the cymunk space. It sits between gameobjects and the gamelayout. 

Its jobs are to
    1.    Retrieve the current gravity vector and update the space's gravity with it.

    2.	  Host a notifications system through which gameobjects communicate with the gamelayout.

    3.    Maintain a mapping between physics shapes and the gameobjects that contain those shapes.

    4.    Update a gameobject's renderable objects to match that gameobject's physics body.

    5. 	  Start/Stop a level (for example drop a ball on start, and remove that ball on stop).


