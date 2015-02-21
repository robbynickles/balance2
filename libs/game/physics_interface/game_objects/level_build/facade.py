# Abstract GameObject Class

class GameObject():
    body       = None
    shape      = None

    # A render_obj is a tuple of canvas instructions.
    render_obj = ()

    space      = None
    before     = False # If before is turned on, render to context.before instead of context.
    context    = None

    smap       = None

    # These are called when the object is being loaded. Either they contain lines that need to be executed in the running environment,
    # or build nonpickle-able objects.

    # As the window of the running environment may be different size and position than the build window,
    # GameObjects must adjust the coordinates of their objects accordingly.
    def adjust_coordinates( self, pos, size ):
        return 

    def build_phys_obj( self, space ):
        return

    def build_render_obj( self, context ):
        return

    def load_into_space_and_context( self, space, context, pos, size ):
        self.adjust_coordinates( pos, size )
        self.build_phys_obj( space )
        self.build_render_obj( context )

        if self.body != None and self.shape != None:
            space.add( self.body, self.shape )
        if self.body != None:
            space.add( self.body )
        
        for canvas_instruction in self.render_obj:
            # A canvas instruction is sent to canvas.before when that object needs 
            # to be dynamically positioned in the animation loop.
            if self.before:
                context.before.add( canvas_instruction )
            else:
                context.add( canvas_instruction )

        self.space, self.context = space, context

    # This method is important for pickling. Objects these variables reference can't be pickled, and hence
    # those references need to be removed before pickling.
    def remove_from_space_and_context( self ):
        # Remove the physics body from self.space.
        if self.space != None:
            if self.body != None:
                self.space.remove( self.body )
                self.body = None
            if self.shape != None:
                self.space.remove( self.shape )
                self.shape = None
            self.space = None

        # Remove the render obj from self.context
        if self.context != None:
            for canvas_instruction in self.render_obj:
                if self.before:
                    self.context.before.remove( canvas_instruction ) 
                else:
                    self.context.remove( canvas_instruction ) 
            self.render_obj = None
            self.context = None
    
    def update( self ):
        pass
    
    def remove( self ):
        self.remove_from_space_and_context()
        if self.smap != None:
            try:
                del self.smap[ self.body ]
            except:
                pass
            self.smap = None
        

