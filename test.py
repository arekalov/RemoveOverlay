from RemoveOverlay import RemoveOverlay
remover = RemoveOverlay('images2')
biases = remover.x_y_finder()
remover.cut_and_sew('new2.jpg', biases)
