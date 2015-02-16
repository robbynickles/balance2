from os.path import dirname, join
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle, Line

def load_texture( fle, w=32, h=32 ):
    return Image(join(dirname(__file__), fle), mipmap=True).texture

def texture_toggle( fl1, fl2, button, state ):
    if state == 'normal':
        texture =  load_texture( fl1 )
    else:
        texture =  load_texture( fl2 )
    with button.canvas:
        Rectangle(
            texture=texture,
            pos=(button.x+button.width/2.0-16, button.y+button.height/2.0-16),
            size=(32,32)
        )

