import brush, line, eraser

import transformation

def dispatch( self, touch, touch_stage, acc ):
    if self.active_mode != None:
        tilt = 0.,0.,0. #transformation.to_tilt( acc )

        if self.active_mode == 'brush':
            brush.freehand( self, touch, touch_stage )
    
        if self.active_mode == 'line':
            line.straightline( self, touch, touch_stage, tilt )

        if self.active_mode == 'edit line':
            line.editline( self, touch, touch_stage, tilt )

        if self.active_mode == 'eraser':
            eraser.erase( self, touch, touch_stage )
