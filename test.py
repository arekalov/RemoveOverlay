from RemoveOverlay import RemoveOverlay
remover = RemoveOverlay('images2')
biases = remover.x_y_finder()
print(biases)
remover.cut_and_sew('new1.jpg', biases)
