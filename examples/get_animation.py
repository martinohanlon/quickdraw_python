from quickdraw import QuickDrawData

qd = QuickDrawData()

anvil = qd.get_drawing("anvil",0)
anvil.animation.save("my_anvil_animation.gif")