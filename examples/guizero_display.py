# This examples requires guizero
#  windows - pip install guizero
#  macos - pip3 install guizero
#  linux/raspberry pi - sudo pip3 install guizero

from guizero import App, Text, Combo, Picture
from quickdraw import QuickDrawData

def display_drawing():
    display.image = qd.get_drawing(drawing_name.value).image

qd = QuickDrawData()

app = App(title="Quick, Draw! Viewer")
Text(app, text="Pick a drawing")
drawing_name = Combo(app, options=qd.drawing_names, selected=qd.drawing_names[0], command=display_drawing)
display = Picture(app)
status = Text(app)
display_drawing()
display.repeat(1000, display_drawing)
app.display()