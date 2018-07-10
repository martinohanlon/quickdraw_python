from quickdraw import QuickDrawDataGroup

qdg = QuickDrawDataGroup("anvil", cache_dir="C:\\path\\to\\cache")
print(qdg.drawing_count)
print(qdg.get_drawing())