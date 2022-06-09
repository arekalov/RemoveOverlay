import os
from pprint import pprint

import numpy
from PIL import Image

# Синтетически иметирует работу камеры микроскопа, создавая изображения со сдвигом
from numpy import array


def image_cutter(path, n_x, n_y, bias_x, bias_y,  # Симулирует фотографии микроскопа
                 is_digit=True):  # Путь, кол-во кусков по х, кол-во кусков по у, смещение по х, смещение по у, формат выведения результата
    try:
        img = Image.open(path)
        img_x, img_y = img.size
        img = img.crop((0, 0, img_x // n_x * n_x, img_y // n_y * n_y))
        if is_digit:
            images = []
        else:
            os.mkdir(path.split('/')[-1])
        count_x, count_y = 0, 0
        for i in range(0, img.size[1], img_y // n_y):
            if is_digit:
                images.append([])
            for j in range(0, img.size[0], img_x // n_x):
                new_image = img.crop((j, i, j + img_x // n_x + bias_x, i + img_y // n_y + bias_y))
                if is_digit:
                    images[-1].append(img_to_pixels(new_image))
                else:
                    new_image.save(f'{path.split("/")[-1]}/{count_x} {count_y}.jpeg')
                count_x += 1
            count_x = 0
            count_y += 1
        if is_digit:
            return images
        else:
            return f'Photo directory "{path.split("/")[-1]}" created'
    except Exception as ex:
        print('EXCEPTION!')
        print(ex)


def rgb_to_grid(images):  # Преобразует массив фотографий из RGB в L
    grid_imgs = images.copy()
    for i in range(len(images)):
        # print('i')
        for j in range(len(images[i])):
            # print('j')
            for y in range(len(images[i][j])):
                # print('y')
                for x in range(len(images[i][j][y])):
                    r, g, b = grid_imgs[i][j][y][x]
                    grid_imgs[i][j][y][x] = round(r * 299 / 1000 + g * 587 / 1000 + b * 114 / 1000)
    return grid_imgs


def img_to_pixels(img):  # Преобразует фотографию в цифру
    pixels_arr = []
    pixels = img.load()
    for a in range(img.size[1]):
        pixels_arr.append([])
        for b in range(img.size[0]):
            pixels_arr[-1].append(pixels[b, a])
    return pixels_arr


def photos_to_digits(directory):  # Преобразует фотографии из директории в цифру
    images = []
    # for i in range(len(os.listdir(directory))):
    for i in range(0, 3):
        line_images = []
        if i % 2 == 0:
            for j in range(len(os.listdir(f'{directory}/{i}'))):
                print(j)
                file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
                img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
                line_images.append(img_to_pixels(img))
            print('dir', i)
            images.append(line_images)
        else:
            for j in range(12, -1, -1):
                print(j)
                file_extention = os.listdir(f'{directory}/{i}')[0].split('.')[1]
                img = Image.open(f'{directory}/{i}/{i}_{j}.{file_extention}')
                # img.show()
                line_images.append(img_to_pixels(img))
            print('dir', i)
            images.append(line_images)
    print(numpy.array(images).shape)
    return images

