from os.path import dirname, join
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle, Line

def load_texture( fle ):
    return Image(join(dirname(__file__), fle), mipmap=True).texture

def texture_toggle( fl1, fl2 ):
    texture1 = load_texture( fl1 )
    texture2 = load_texture( fl2 )

    def toggle( button, state ):
        if state == 'normal':
            texture = texture1
        else: # state == 'down'
            texture = texture2
        with button.canvas:
            Rectangle(
                texture=texture,
                pos=(button.x+button.width/2.0-16, button.y+button.height/2.0-16),
                size=(32,32)
            )

    return toggle


def distance( a, b ):
    return sum ( [ (x1-x2)**2 for x1,x2 in zip( a, b ) ] ) ** .5
