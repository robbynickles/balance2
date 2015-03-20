import brush, line, eraser

import transformation

def dispatch( self, touch, touch_stage ):
    magnetize = self.drawing_toolkit.magnetize()

    if self.active_mode != None:

        if self.active_mode == 'brush':
            brush.freehand( self, touch, touch_stage )
    
        if self.active_mode == 'line':
            line.drawline( self, touch, touch_stage, magnetize )

        if self.active_mode == 'edit line':
            line.editline( self, touch, touch_stage, magnetize )

        if self.active_mode == 'curve':
            line.drawline( self, touch, touch_stage, magnetize, curve=True )

        if self.active_mode == 'eraser':
            eraser.erase( self, touch, touch_stage )
