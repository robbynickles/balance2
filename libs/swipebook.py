from kivy.uix.scatter import ScatterPlane
from kivy.graphics.transformation import Matrix 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window 

from plyer import utils
if utils._determine_platform() == 'macosx':
    # Manually set the window size to emulate the iphone screen.
    #Window.size = int(640/1.5), int(960/1.5)
    Window.size = 640, 960
    pass

# Simple data structure for storing the positon and dimensions of a page.
class Page():
    def __init__(self, pos, size):
        self.x, self.y  = pos
        self.size = size

class SwipeBook( ScatterPlane ):
    """ Upgrades: 
    1. Deactivate un-viewed widgets.
    2. Don't press buttons when swiped.
    """
    PAGE_W, PAGE_H = Window.size
    SPACING = .2 * Window.width

    ##### Initialization
    def __init__(self, *args, **kwargs):
        """ScatterPlane that supports navigation between pages."""
        # Don't allow any touch navigation.
        self.do_rotation, self.do_scale, self.do_translation = False, False, False

        super( SwipeBook, self).__init__(*args, **kwargs)
        
        #from kivy.uix.label import Label
        #self.add_widget( Label( text="***** WINDOW DIMENSIONS:  {} x {} *****".format( self.PAGE_W, self.PAGE_H ) ) )  

        self.pages = []

        # Only allow one animation loop at a time.
        self.animating = False

        # Sliding velocity.
        self.xvel = 0

        # Rendering layers: widgets in self.top are rendered on top of widgets in self.bottom.
        self.top_layer    = FloatLayout()
        self.bottom_layer = FloatLayout()

        # The widget (and the widget tree there rooted) added first is rendered first (meaning underneath any widgets added later).
        self.add_widget( self.bottom_layer ) 
        self.add_widget( self.top_layer )

    ##### Widget adding/removing with layer control
    # Any widget added to a layer 'above' another layer is rendered on top of all widgets in the 'lower' layer.
    def add_widget_to_layer( self, widg, layer ):
        if layer == 'top':
            self.top_layer.add_widget( widg )
        if layer == 'bottom':
            self.bottom_layer.add_widget( widg )

    def remove_widget_from_layer( self, widg, layer):
        if layer == 'top':
            self.top_layer.remove_widget( widg )
        if layer == 'bottom':
            self.bottom_layer.remove_widget( widg )

    # Create a new page and place the widget in it.
    # A page is a PAGE_W x PAGE_H box that is used for collision detection.
    def add_page( self, widget ):
        x, y = len(self.pages) * ( self.PAGE_W + self.SPACING ), 0
        page = Page( (x,y), (self.PAGE_W, self.PAGE_H) )
        self.pages += [page]

        # Wrap widget in a BoxLayout before placing in the swipebook.
        page_wrapper = BoxLayout( pos=(x,y), size=(self.PAGE_W, self.PAGE_H) )
        page_wrapper.add_widget( widget )
        self.add_widget_to_layer( page_wrapper, 'bottom' )

    def current_page(self): 
        """Return the current page we're looking at."""
        return int(-self.x / self.PAGE_W)


    ##### Navigation methods
    # Swipe right to the next page.
    def swipe_right( self ):
        self.start_page_i = self.current_page()
        self.start_page = self.pages[ self.start_page_i ]
        self.start_inertia( -50 )

    # Swipe left to the previous page.
    def swipe_left( self ):
        self.start_page_i = self.current_page()
        self.start_page = self.pages[ self.start_page_i ]
        self.start_inertia( 50 )


    ##### Animation control
    # Start the animation
    def start_inertia(self, xvel):
        global SWIPING
        SWIPING = True
        self.animating, self.xvel = True, xvel
        Clock.schedule_interval(self.animate, 1/120.0)

    # Stop the animation
    def stop_inertia(self):
        self.animating, self.xvel = False, 0
        Clock.unschedule(self.animate)
    
    # Check if self is colliding with a new page.
    def collide_page( self, page ):
        return page != self.start_page and \
                page.x - abs(self.xvel) <= -self.x <= page.x + abs(self.xvel)

    # Translate self (the viewport) horizontally.
    def x_shift(self, x):
        self.apply_transform( 
            self.transform.inverse().translate( x, 0, 0 )
        )


    ##### Animation
    def animate( self, dt ):
        for p in self.pages:
            if self.collide_page(p):
                self.stop_inertia()
                self.x_shift( -p.x )
                return 
        self.x += self.xvel
        self.x_shift( self.x )

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window 
    
    swipe_plane = SwipePlane()

    for i in range(5):
        # Give swipe plane a widget whose pos is within the desired page.
        swipe_plane.add_page( Label( text=str(i), pos=(i*Window.width, 0) ) )

    runTouchApp( swipe_plane )
