import transformation

OFFSET = 200

def build_offsets( self, (x, y) ):
    self.x_off = 0
    if self.y + y < self.y + (self.height/2.):
        self.y_off = -OFFSET
    else:
        self.y_off = OFFSET

def destroy_offsets( self ):
    self.x_off, self.y_off = None, None

def offset_pos( self, (x,y) ):
    # The idea is that the offset puts the touch either above or below the touch.
    # Whether it's below or above depends on where in the screen is the touch.
    # If the offset is below, change it to above when the touch is above 85 percent screen height.
    # If the offset is above, change it to below when the touch is under 15 percent screen height.
    # That there is an overlap (i.e. sections of the screen reachable with either the above offset or below offset),
    # ensures all points on the screen are reachable.

    mid_line = lambda x: 0#transformation.horizontal_line( tilt, self.x + self.width/2.0 )

    if self.y_off < 0: # below-finger (negative) offset
        # Transistion point to above offset.
        if y > mid_line( x ) + self.y + (.85*self.height):
            self.y_off = OFFSET
        # If the below offset was shrunk last time, give it full magnitude.
        elif self.y_off > -OFFSET:
            self.y_off = -OFFSET
    else: # above-finger (positive) offset
        # Transistion point to below offset.
        if y < mid_line( x ) + self.y + (.15*self.height):
            self.y_off = -OFFSET
        # If the above offset was shrunk last time, give it full magnitude.
        elif self.y_off < OFFSET:
            self.y_off = OFFSET

    # Don't allow an offset to put an endpoint offscreen. Shrink it to fit.
    if y + self.y_off > self.y + self.height:
        self.y_off = self.y + self.height - y
    elif y + self.y_off < self.y:
        self.y_off = -( y - (self.y) ) 

    # Shift the offset based on the tilt of the phone.
    #if tilt != (0.,0.):
    #self.x_off, self.y_off = self.y_off * tilt[0], self.y_off * -tilt[1]

    return x + self.x_off, y + self.y_off
