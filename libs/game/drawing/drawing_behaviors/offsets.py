import transformation

def build_offsets( self, (x, y) ):
    self.x_off = 0
    if self.y + y < self.y + (self.height/2.):
        self.y_off = -200
    else:
        self.y_off = 100

def destroy_offsets( self ):
    self.x_off, self.y_off = None, None

def offset_pos( self, (x,y), tilt ):
    # The idea is that the offset puts the touch either above or below the touch.
    # Whether it's below or above depends on where in the screen is the touch.
    # If the offset is below, change it to above when the touch is passed 3/4 of the screen.
    # If the offset is above, change it to below when the touch is passed 1/4 of the screen.
    # That there is an overlap (i.e. sections of the screen reachable with either the above offset of below offset),
    # ensures all points on the screen are reachable.

    mid_line = transformation.horizontal_line( tilt, self.x + self.width/2.0 )

    if self.y_off < 0: # below-finger (negative) offset
        if y > mid_line( x ) + self.y + (.75*self.height):
            self.y_off = 200
        elif self.y_off > -200:
            self.y_off = -200
    else: # above-finger (positive) offset
        if y < mid_line( x ) + self.y + (.25*self.height):
            self.y_off = -200
        elif self.y_off < 200:
            self.y_off = 200

    # Don't allow an offset to put an endpoint offscreen.
    if y + self.y_off > self.y + self.height:
        self.y_off = self.y + self.height - y
    elif y + self.y_off < self.y:
        self.y_off = -( y - (self.y) ) 

    # Shift the offset based on the tilt of the phone.
    if tilt != (0.,0.):
        self.x_off, self.y_off = self.y_off * tilt[0], self.y_off * -tilt[1]

    return x + self.x_off, y + self.y_off
