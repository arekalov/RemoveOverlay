import random
import statistics
import numpy


class RemoveOverlay:
    """Класс RemoveOverlay находит наложение 'кусков фотографий', при работе микроскопа"""

    def __init__(self, image_width, image_height, images):
        """
        Инициализатор класса

        Принимает: ширина фотографии, высота фотогографии, массив фотографий numpy.array с цифровым представлением изображений
        Возвращает: None
        """
        self.image_width = image_width
        self.image_height = image_height
        self.images = images
        self.n = 5  # Количество проверок смещений

    def random_indexes_generator(self, n, mode):
        """
        Генерирует массив изображений, на которых будет происходить поиск смещений

        Принимает: количеслво элементов в массиве, ось ('x' или 'y')
        Возвращает: массив кортежей вида ('координата по х', 'координата по у')
        """
        random_indexes = []
        for i in range(n):
            if mode == 'x':
                first = (random.randint(0, self.images.shape[0] - 1), random.randint(0, self.images.shape[0] - 2))
                second = (first[0], first[1] + 1)
                random_indexes.append((first, second))
            elif mode == 'y':
                first = (random.randint(0, self.images.shape[0] - 2), random.randint(0, self.images.shape[0] - 1))
                second = (first[0] + 1, first[1])
                random_indexes.append((first, second))
        return random_indexes

    def x_y_finder(self):
        """Метод конвеера находит смещение по данным, заданным в конструкторе

        Принимает: None
        Возвращает: кортеж из 2 целых чисел, смещений по x и y"""
        xs = []
        ys = []
        for im1, im2 in self.random_indexes_generator(self.n, 'x'):
            probabilities = self.probability_finder(im1, im2, 'x')
            xs.append(probabilities.index(min(probabilities)) + 1)
        for im1, im2 in self.random_indexes_generator(self.n, 'y'):
            probabilities = self.probability_finder(im1, im2, 'y')
            ys.append(probabilities.index(min(probabilities)) + 1)
        return statistics.mode(xs), statistics.mode(ys)

    def probability_finder(self, ind1, ind2, mode):
        """Оценвиает вероятность наложения фото 1 на фото2

        Принимает: индекс первой фотографии, из находящихся в self.images, индекс второй фотографии, из находящихся в self.images, ось ('x' 'y')
        Возвращает: массив вероятностей смещений по пикселям"""
        img1 = self.images[ind1]
        img2 = self.images[ind2]
        probabilities = []
        if mode == 'x':
            for over in range(self.image_height):
                probabilities.append(self.mse(img1[:, -1], img2[:, over]))
        elif mode == 'y':
            for over in range(self.image_width):
                probabilities.append(self.mse(img1[-1, :], img2[over, :]))
        return probabilities

    @staticmethod
    def deviation(a, b):
        """Поиск отклонения массива b от a

        Принимает: два массива numpy.array
        Возвращает: отклонение"""
        mean = (a + b) / 2
        mse = (a - mean) ** 2
        return numpy.sum(mse)


help(RemoveOverlay)
