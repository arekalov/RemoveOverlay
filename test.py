from RemoveOverlay import RemoveOverlay
remover = RemoveOverlay('images')
areas = remover.areas_splitter()
# print(len(areas))
remover.x_y_areas_finder(areas)