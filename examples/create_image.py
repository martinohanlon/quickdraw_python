from quickdraw import QuickDrawData
from PIL import Image, ImageDraw

qd = QuickDrawData()
anvil = qd.get_drawing("anvil")

anvil_image = Image.new("RGB", (255,255), color=(255,255,255))
anvil_drawing = ImageDraw.Draw(anvil_image)

for stroke in anvil.strokes:
    # anvil_drawing.line(stroke, fill=(0,0,0), width=2)

    for coordinate in range(len(stroke)-1):
        x1 = stroke[coordinate][0]
        y1 = stroke[coordinate][1]
        x2 = stroke[coordinate+1][0]
        y2 = stroke[coordinate+1][1]
        anvil_drawing.line((x1,y1,x2,y2), fill=(0,0,0), width=2)

anvil_image.show()