import brush, line, eraser

def dispatch( self, touch, touch_stage ):
    if self.active_mode != None:
        if self.active_mode == 'brush':
            brush.freehand( self, touch, touch_stage )
    
        if self.active_mode == 'line':
            line.straightline( self, touch, touch_stage )
            
        if self.active_mode == 'eraser':
            eraser.erase( self, touch, touch_stage )
