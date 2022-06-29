import os
import random
import statistics
import numpy
from PIL import Image


class RemoveOverlay:
    """Класс RemoveOverlay находит наложение 'кусков фотографий', при работе микроскопа"""

    def __init__(self, directory_name, image_width=1650, image_height=1075, iters=20, areas_iters=5):
        """
        Инициализатор класса

        Принимает: ширина фотографии, высота фотогографии, имя директории с фотографиями, количество проверок (по умолчанию 10) в стандартном режиме,
        количество проеерок в режиме разбития на области
        Возвращает: None
        """
        self.image_width = image_width
        self.image_height = image_height
        self.directory_name = directory_name
        self.iters = iters
        self.areas_iters = areas_iters

    def set_iters(self, new_iters):
        """
        Изменяет количество проверок

        Принимает: новое количество проверок
        Возвращает: None
        """
        self.iters = new_iters

    def get_iters(self):
        """
        Возвращает количество проверок

        Принимает: None
        Возвращает: количество проверок
        """
        return self.iters

    def set_size(self, width, height):
        """
        Изменяет размер

        Принимает: ширина, высота
        Возвращает: None
        """
        self.image_width = width
        self.image_height = height

    def get_sze(self):
        """
        Возвращает размер картинки

        Принимает: None
        Возвращает: ширину и высоту картинки
        """
        return self.image_width, self.image_height

    def areas_splitter(self):
        SEP_Y = 5  # Количество фоторгафий в одной области по у
        SEP_X = 6  # Количество фотографий во одной области по х
        y_areas = len(os.listdir(self.directory_name)) // SEP_Y
        x_areas = len(os.listdir(f'{self.directory_name}/{os.listdir(self.directory_name)[0]}')) // SEP_X
        x_flag, y_flag = False, False
        if len(os.listdir(self.directory_name)) % SEP_Y != 0:
            y_flag = True
            y_areas -= 1
        if len(os.listdir(f'{self.directory_name}/{os.listdir(self.directory_name)[0]}')) % SEP_X != 0:
            x_areas -= 1
            x_flag = True
        border_x = []
        border_y = []
        counter = 0
        for i in range(len(os.listdir(self.directory_name))):
            if (i + 1) % SEP_Y == 0 and counter < y_areas:
                border_y.append(i)
                counter += 1
        counter = 0
        for i in range(len(os.listdir(f'{self.directory_name}/{os.listdir(self.directory_name)[0]}'))):
            if (i + 1) % SEP_X == 0 and counter < x_areas:
                border_x.append(i)
                counter += 1
        if x_flag:
            border_x.append(len(os.listdir(f'{self.directory_name}/{os.listdir(self.directory_name)[0]}')) - 1)
        if y_flag:
            border_y.append(len(os.listdir(self.directory_name)) - 1)
        areas = []
        pred_y = 0
        for i in range(len(border_y)):
            pred_x = 0
            line = []
            for j in range(len(border_x)):
                line.append(((pred_x, pred_y), (border_x[j], border_y[i])))
                pred_x = border_x[0] + 1
            pred_y = border_y[i] + 1
            areas.append(line)
        return areas

    def x_y_areas_finder(self, areas):
        print(len(areas))
        biases = []
        for i in range(len(areas)):
            line = []
            for j in range(len(areas[0])):
                line.append(self.x_y_finder(areas[i][j]))
            biases.append(line)
        return biases

    def random_index_generator_areas(self, lt, rb, mode):
        random_indexes = []
        if mode == 'x':
            print(mode)
            for i in range(self.areas_iters):
                first = (random.randint(lt[1], rb[1]), random.randint(lt[0], rb[0] - 1))
                second = (first[0] + 1, first[1])
                random_indexes.append((first, second))
        elif mode == 'y':
            for i in range(self.areas_iters):
                first = (random.randint(lt[0], rb[0]), random.randint(lt[1], rb[1] - 1))
                second = (first[0], first[1] + 1)
                random_indexes.append((first, second))
        print(lt, rb)
        print(random_indexes)
        return random_indexes

    def random_indexes_generator(self, mode):
        """
        Генерирует массив изображений, на которых будет происходить поиск смещений

        Принимает: количеслво элементов в массиве, ось ('x' или 'y')
        Возвращает: массив кортежей вида ('координата по х', 'координата по у')
        """
        random_indexes = []
        for i in range(self.iters):
            if mode == 'x':
                dirs = len(os.listdir(self.directory_name))
                selected_dir = random.randint(2, dirs - 5)
                images_in_dir = len(os.listdir(f'{self.directory_name}/{selected_dir}'))
                if selected_dir % 2 == 0:
                    ind1 = (selected_dir, random.randint(3, images_in_dir - 5))
                    ind2 = (ind1[0], ind1[1] + 1)
                else:
                    ind1 = (selected_dir, random.randint(3, images_in_dir - 4))
                    ind2 = (ind1[0], ind1[1] - 1)
                random_indexes.append((ind1, ind2))
            elif mode == 'y':
                dirs = len(os.listdir(self.directory_name))
                selected_dir = random.randint(2, dirs - 5)
                images_in_dir = len(os.listdir(f'{self.directory_name}/{selected_dir}'))
                ind1 = (selected_dir, random.randint(3, images_in_dir - 4))
                ind2 = (selected_dir + 1, abs(images_in_dir - 1 - ind1[1]))
                random_indexes.append((ind1, ind2))
        return random_indexes

    def x_y_finder(self, lprb=()):
        """Находит смещение по данным, заданным в конструкторе

        Принимает: None
        Возвращает: кортеж из 2 целых чисел, смещений по x и y"""
        xs = []
        ys = []
        if not lprb:
            for im1, im2 in self.random_indexes_generator('x'):
                probabilities = self.probability_finder(im1, im2, 'x')
                xs.append(probabilities.index(min(probabilities)) + 1)
            for im1, im2 in self.random_indexes_generator('y'):
                probabilities = self.probability_finder(im1, im2, 'y')
                ys.append(probabilities.index(min(probabilities)) + 1)
        else:
            for im1, im2 in self.random_index_generator_areas(lprb[0], lprb[1], 'x'):
                print(im1, im2)
                probabilities = self.probability_finder(im1, im2, 'x')
                xs.append(probabilities.index(min(probabilities)) + 1)
            for im1, im2 in self.random_index_generator_areas(lprb[0], lprb[1], 'y'):
                probabilities = self.probability_finder(im1, im2, 'y')
                ys.append(probabilities.index(min(probabilities)) + 1)
        # new_xs = (list(filter(lambda x: x in range(round(statistics.mean(xs) - statistics.stdev(xs) / 2),
        #                                            round(statistics.mean(xs) + statistics.stdev(xs) / 2)),
        #                       xs)))
        # new_ys = (list(filter(lambda x: x in range(round(statistics.mean(ys) - statistics.stdev(ys) / 2),
        #                                            round(statistics.mean(ys) + statistics.stdev(ys) / 2)),
        #                       ys)))
        new_xs = xs
        new_ys = ys
        if not new_ys:
            new_ys = (list(filter(lambda x: x in range(round(statistics.mean(ys) - statistics.stdev(ys) / 1.5),
                                                       round(statistics.mean(ys) + statistics.stdev(ys) / 1.5)),
                                  ys)))
        if not new_xs:
            new_xs = (list(filter(lambda x: x in range(round(statistics.mean(xs) - statistics.stdev(xs) / 1.5),
                                                       round(statistics.mean(xs) + statistics.stdev(xs) / 1.5)),
                                  xs)))
        return round((statistics.mode(new_xs) + statistics.median(new_xs)) / 2), round(
            (statistics.mode(new_ys) + statistics.median(new_ys)) / 2)

    def probability_finder(self, ind1, ind2, mode):
        """
        Оценвиает вероятность наложения фото 1 на фото2

        Принимает: индекс первой фотографии, из находящихся в self.images, индекс второй фотографии, из находящихся в self.images, ось ('x' 'y')
        Возвращает: массив вероятностей смещений по пикселям
        """
        img1 = Image.open(f'{self.directory_name}/{ind1[0]}/{ind1[0]}_{ind1[1]}.jpg').convert('L')
        img2 = Image.open(f'{self.directory_name}/{ind2[0]}/{ind2[0]}_{ind2[1]}.jpg').convert('L')
        img1 = numpy.array(img1)
        img2 = numpy.array(img2)
        probabilities = []
        if mode == 'x':
            for over in range(self.image_width):
                probabilities.append(self.deviation(img1[:, -1], img2[:, over]))
        elif mode == 'y':
            for over in range(self.image_height):
                probabilities.append(self.deviation(img1[-1, :], img2[over, :]))
        return probabilities

    @staticmethod
    def deviation(a, b):
        """
        Поиск отклонения массива b от a

        Принимает: два массива numpy.array
        Возвращает: отклонение
        """
        mean = (a + b) / 2
        res = (a - mean) ** 2
        return numpy.sum(res)

    def cut_and_sew(self, output_path, biases):
        """
        Обрезает куски фотографий и склеивает в одну

        Принимает: путь для сохранения результата, смещения, которые будут обрезаны
        Возвращает: None
        """
        n_dirs = len(os.listdir(self.directory_name))
        n_imgs = len(os.listdir(f"{self.directory_name}/{os.listdir(self.directory_name)[0]}"))
        expansion = os.listdir(f"{self.directory_name}/{os.listdir(self.directory_name)[0]}")[0].split('.')[1]
        final_image = Image.new('RGB', (n_imgs * self.image_width - n_imgs * biases[0],
                                        n_dirs * self.image_height - n_dirs * biases[1]))
        new_w = self.image_width - biases[0]
        new_h = self.image_height - biases[1]
        for y in range(0, n_dirs):
            if y % 2 == 0:
                for x in range(0, n_imgs):
                    img_to_paste = Image.open(f'{self.directory_name}/{y}/{y}_{x}.{expansion}').crop(
                        (0, 0, new_w, new_h))
                    final_image.paste(img_to_paste, (new_w * x, new_h * y))
            else:
                counter = 0
                for x in range(n_imgs - 1, -1, -1):
                    img_to_paste = Image.open(f'{self.directory_name}/{y}/{y}_{x}.{expansion}').crop(
                        (0, 0, new_w, new_h))
                    final_image.paste(img_to_paste, (new_w * counter, new_h * y))
                    counter += 1
        final_image.save(output_path)
