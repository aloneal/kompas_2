import os
import time
import numpy as np
from datetime import datetime as dt
import math
import csv


def read_file_txt(name, path='D:\\'):
    """
    Читает указнный файл в таблицу. Испраавляет перенос строки ответа у параметров 129 и 130.
    Фильтрует таблицу по параметрам запроса 129, 130 и 199.
    На выходе фильтроанная таблица.
    :param name: имя файла
    :param path: полный путь до директории с файлами данных датчиков
    :return: На выходе фильтроанная таблица по запросам 129, 130 и 199.
    """
    name1 = ['time', 'adr1', 'adr2', 'param', 't_call', 'len', 'ans']

    res = []  # массив строк для записи результата
    with open(os.path.join(path, name), 'r') as file_r:  # открыли файл по пути для чтения
        s = file_r.readline()
        if s == 0:
            return ''
        while s.count('\t') != 6:  # поиск строки с 6 табуляциями (если файл пуст - вечность!!!)
            s = file_r.readline().rstrip('\n')  # читаем следующую строку из файла без символа окончания строки

        while s and s != '\n':  # пока есть строки и строка не последняя
            col = s.split('\t')  # разбиваем строку через табуляцию
            if (col[3] == '129') or (col[3] == '130'):  # добавлю две следующие строки как два столбца
                col.append(file_r.readline().rstrip('\n'))
                col.append(file_r.readline().rstrip('\n'))
                res.append(col)
            if col[3] == '199':  # если "199", то надо разбить столбец с 6 числами на 6 столбцов по одному числу
                temp1 = col[6].split(',')
                col = col[:6]  # убираю лишний столбец для замены
                for num, t in enumerate(temp1):  # по очереди добавлю все значения в конец вектора
                    col.append(t)
                res.append(col)
            s = file_r.readline().rstrip('\n')  # читаем следующую строку из файла без символа окончания строки

    # собрать 129 и 130 вместе по адресам
    # res_np = np.asarray(res)

    format_t = '%d.%m.%Y %H:%M:%S'
    print(dt.strptime(res[20][0], format_t) - dt.strptime(res[0][0], format_t))
    return res


def mask(df, key, value):  # реализация фильтра для pandas
    return df[df.key == value]


# def read_file_bin(name, path=''):
#     dt = np.dtype([('a', 'i4'), ('b', 'i4'), ('c', 'i4'), ('d', 'f4'), ('e', 'i4', (256,))])
#     data = np.fromfile(name, dtype=dt)
#     df = pd.DataFrame(data.tolist(), columns=data.dtype.names)
#     return df


def find_new_file(path1='C:\\'):
    """
    Опрос указанной дериктории по наличию всех файлов по паттерну: data*.txt
    :param path1: полный путь до директории с файлами данных датчиков
    :return: возвращает имя последнего по времени подходящего файла
    """
    date_files = []
    sleep = 10  # задержа перед повторным опросом
    while not date_files:
        for fn in os.listdir(path=path1):
            full_path = os.path.join(path1, fn)
            if fn.lower().startswith('data') and fn.lower().endswith('.txt'):  # file: 'data' + '...' + '.txt'
                date_files = [(time.localtime(os.path.getmtime(full_path))[:5], os.path.basename(fn))]
        print(date_files)
        if not date_files:  # если файла нет, то ждем 10 секунд и проверяем снова
            time.sleep(sleep)
            print('wait file next {} second'.format(sleep))
    date_files.sort()
    date_files.reverse()
    return date_files[-1][1]


def pitch_roll_h(table):
    """
    по чистому файлу вычисляет углы и дописывает в таблицу
    :param table:
    :return:
    """
    table_end = []
    for i in table:
        if i[3] == '199':
            i[6:] = list(map(float, i[6:]))
            pitch = math.degrees(math.asin(-i[6]))
            roll = math.degrees(math.asin(i[7]/math.cos(pitch)))
            mx2 = i[9]*math.cos(pitch) + i[11]*math.sin(pitch)
            my2 = i[9]*math.sin(pitch)*math.sin(roll) + i[10]*math.cos(roll) - i[11]*math.sin(roll)*math.cos(pitch)
            mz2 = -i[9]*math.sin(pitch)*math.cos(roll) + i[10]*math.sin(roll) + i[11]*math.cos(roll)*math.cos(pitch)
            if mx2 > 0 and my2 >= 0:
                heading = math.atan(my2/mx2)
            elif mx2 < 0:
                heading = 180 + math.atan(my2/mx2)
            elif mx2 > 0 and my2 < 0:
                heading = 360 + math.atan(my2/mx2)
            elif mx2 == 0 and my2 < 0:
                heading = 90
            elif mx2 == 0 and my2 > 0:
                heading = 270
            else:
                heading = 0
                print('heading = 0, не выполняются другие условия')
            print(pitch, roll, heading)
            print(math.sqrt(mx2**2 + my2**2 + mz2**2), ' должно быть близко к 1')
            table_end.append(i)
            table_end.append([pitch, roll, heading])
    return table_end


def plot_points(points):
    """
    берем таблицу и рисуем в трехмерке точки - смотрим на шарик (после калибровки) или элипсоид
    :param points: pandas таблица со столбцами Ax, Ay, Az, Mx, My, Mz
    :return:
    """
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    threedee = plt.figure()
    ax = threedee.add_subplot(111, projection='3d')
    ax.scatter(points.Ax, points.Ay, points.Az, c='r', marker='o')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


if __name__ == '__main__':
    directory = os.path.join('D:\\', 'teleskop_data')
    print(os.listdir(directory))
    while 1:  # This constructs an infinite loop
        file1 = find_new_file(directory)  # поиск необработанных файлов
        print(directory, file1)
        file1 = 'data0001.txt'
        table_clean = read_file_txt(file1, directory)  # очистка данных до таблицы с Axyz и Mxyz

        # with open(os.path.join(directory, 'clean_' + file1), "w", newline='\n') as f:
        #     writer = csv.writer(f, delimiter='\t')
        #     writer.writerows(table_clean)

        # np.savetxt(os.path.join(directory, file1), table_clean, delimiter='\t')
        # plot_points(table_clean)
        table_clean2 = pitch_roll_h(table_clean)
        print(table_clean2)
        break
        one = input('one more? => "y"')
        if one != 'y':
            break

        # os.renames(file1, 'ok_' + file1)
