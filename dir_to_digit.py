import os
import datetime
import statistics

import numpy as np
from PIL import Image
from conversion_functions import rgb_to_grid, photos_to_digits
from main import RemoveOverlay


# def dir_to_digit(directory):  # Преобразует фотографии из директории в цифру
#     images = []
#     start_flag_i = True
#     for i in range(len(os.listdir(directory))):
#         line_images = []
#         start_flag_j = True
#         if i % 2 == 0:
#             for j in range(len(os.listdir(f'{directory}/{i}'))):
#                 file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
#                 img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
#                 img = img.convert('L')
#                 if start_flag_j:
#                     line_images = [np.array(img)]
#                     print(line_images)
#                     start_flag_j = False
#                 else:
#                     line_images = np.append(images, [np.array(img)])
#             print('dir', i)
#             if start_flag_i:
#                 images = np.array([line_images])
#                 start_flag_i = False
#             else:
#                 images = np.append(images, [line_images])
#         else:
#             for j in range(12, -1, -1):
#                 file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
#                 img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
#                 img = img.convert('L')
#                 if start_flag_j:
#                     line_images = [np.array(img)]
#                     start_flag_j = False
#                 else:
#                     line_images = np.append(images, [np.array(img)])
#             print('dir', i)
#             images = np.append(images, [line_images])
#     print(np.array(images).shape)
#     return images


def dir_to_digit(directory):  # Преобразует фотографии из директории в цифру
    images = []
    for i in range(len(os.listdir(directory))):
        line_images = []
        if i % 2 == 0:
            for j in range(len(os.listdir(f'{directory}/{i}'))):
                file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
                img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
                img = img.convert('L')
                line_images.append(np.array(img))
            print('dir', i)

            images.append(line_images)
        else:
            for j in range(12, -1, -1):
                file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
                img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
                img = img.convert('L')
                line_images.append(np.array(img))
            print('dir', i)
            images.append(line_images)
    images = np.array(images)
    return images


imgs = dir_to_digit('images')
print(imgs.shape)
classsss = RemoveOverlay(imgs.shape[2], imgs.shape[3], imgs)
print(classsss.x_y_finder())