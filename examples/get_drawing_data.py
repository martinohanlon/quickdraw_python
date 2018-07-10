from quickdraw import QuickDrawData

qd = QuickDrawData()

anvil = qd.get_drawing("anvil")
stroke_no = 0
for stroke in anvil.strokes:
    for x, y in stroke:
        # x = xy[0]
        # y = xy[1]
        print("stroke={} x={} y={}".format(stroke_no, x, y))
    stroke_no += 1