# GameObject Class

class GameObject():
    def __init__( self ):
        self.reset()

    def reset( self ):
        self.body              = None
        self.shapes            = []
        self.space             = None
        
        self.render_obj        = ()    # A render_obj is a tuple of canvas instructions.
        self.before            = False # If before is turned on, render to context.before instead of context.
        self.context           = None
        
        self.smap              = {}

        self.physics_interface = None

    # These are called when the object is being loaded. Either they contain lines that need to be executed in the running environment,
    # or build nonpickle-able objects.
    def load_into_space_and_context( self, space, context, pos, size ):
        # Adjust coordinates based on pos and size.
        self.adjust_coordinates( pos, size )

        # Construct the physics body and shape(s).
        self.build_phys_obj( space )

        # Add the body to the space.
        if self.body != None:
            space.add( self.body )
            
        # Add any associated shapes.
        for sh in self.shapes:
            space.add( sh )

        # Construct the renderable object.
        self.build_render_obj()
        
        # Add the renderable object to the context.
        for canvas_instruction in self.render_obj:
            # A canvas instruction is sent to canvas.before when that object needs 
            # to be dynamically positioned in the animation loop.
            if self.before:
                context.before.add( canvas_instruction )
            else:
                context.add( canvas_instruction )

        # Store references for later use.
        self.space, self.context = space, context

    def remove_from_space_and_context( self ):
        # Remove the physics body from self.space.
        if self.space != None:
            if self.body != None:
                self.space.remove( self.body )
            for sh in self.shapes:
                self.space.remove( sh )

        # Remove the render obj from self.context
        if self.context != None:
            for canvas_instruction in self.render_obj:
                if self.before:
                    self.context.before.remove( canvas_instruction ) 
                else:
                    self.context.remove( canvas_instruction ) 

    def create_shape_mapping( self, smap ):
        # A shape mapping maps a shape to its enclosing game_object.
        # Since a body might have multiple shapes associated with it, they're
        # maybe multiple keys in the shape mapping that refer to a game_object.
        self.smap = smap
        for sh in self.shapes:
            self.smap[ sh ] = self

    def remove_shape_mapping( self ):
        for sh in self.shapes:
            if self.smap.has_key( sh ):
                del self.smap[ sh ]

    def load_into_physics_interface( self, physics_interface ):
        self.physics_interface = physics_interface

        self.load_into_space_and_context( physics_interface.space, 
                                          physics_interface.canvas,
                                          physics_interface.pos, 
                                          physics_interface.size )

        self.create_shape_mapping( physics_interface.smap )


    def remove_from_physics_interface( self ):
        self.remove_from_space_and_context()
        self.remove_shape_mapping()
        self.reset()

    # This method achieves the effect of deleting a game_object completely from the game. It also makes it
    # ready for pickling.
    def remove( self ):
        self.remove_from_physics_interface()


    ##### Empty methods that subclasses need to implement

    # As the window of the running environment may be different size and position than the build window,
    # GameObjects must adjust the coordinates of their objects accordingly.
    def adjust_coordinates( self, pos, size ):
        """ Should be implemented by a subclass """
        pass

    def build_phys_obj( self, space ):
        """ Should be implemented by a subclass """
        pass

    def build_render_obj( self ):
        """ Should be implemented by a subclass """
        pass

    def update( self ):
        """ Should be implemented by a subclass (if it needs to be, i.e. if the physics body is moved by the physics engine)"""
        pass
    
        

