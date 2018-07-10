from quickdraw import QuickDrawDataGroup

qdg = QuickDrawDataGroup("anvil")
for drawing in qdg.drawings:
    print(drawing.recognized)