import numpy as np
import os
import csv


def exemple():
    dir1 = 'D:\\python\\neitrin\\work'
    data1 = np.loadtxt(os.path.join(dir1, 'data_calibrate.csv'), delimiter='\t')
    # print(data1, data1.shape)

    Y1 = []
    for i in data1:
        Y1.append(sum(np.array(i) ** 2))

    Y1 = np.array(Y1)
    num_ones = np.ones(data1.shape[0])
    X1 = np.c_[data1, num_ones]
    # print(Y1, X1)

    betta = np.dot(np.dot(np.linalg.inv(np.dot(X1.T, X1)), X1.T), Y1)
    print(betta)


def calibrate_from_file(path):
    # потом написать циклический перебор всех фалов
    file1 = '6.3.2.txt'

    try:  # если чтение цифр будет с ошибками, то сначала переписываем все "," в "." через исключение
        with open(os.path.join(path, file1), 'r') as file_r:
            reader = csv.reader(file_r, delimiter='\t')
            next(reader)  # Skip the headers
            c_mx = []
            for row in reader:
                c_mx.append(list(map(float, row[1:])))
    except ValueError:
        # заменяю все запяты на точки, чтобы переводить текст во float
        with open(os.path.join(path, file1), 'r') as f:
            filedata = f.read()
        filedata = filedata.replace(',', '.')
        with open(os.path.join(path, file1), 'w') as f:
            f.write(filedata)

        with open(os.path.join(path, file1), 'r') as file_r:
            reader = csv.reader(file_r, delimiter='\t')
            next(reader)  # Skip the headers
            c_mx = []
            for row in reader:
                c_mx.append(list(map(float, row[1:])))

    print(len(c_mx)//6, '\n', c_mx[2], '___', c_mx[2][3:])
    betta = []
    for i in range(len(c_mx)//6):
        data = [c_mx[i][:3], c_mx[i+1][:3], c_mx[i+2][:3], c_mx[i+3][:3], c_mx[i+4][:3], c_mx[i+5][:3]]
        betta.append(make_calib_matrix(data))
    print(betta)
    return 'Ok'


def make_calib_matrix(data):
    Y1 = []
    for i in data:
        Y1.append(sum(np.array(i) ** 2))
    Y1 = np.array(Y1)
    num_ones = np.ones(len(data))
    X1 = np.c_[data, num_ones]
    # print('Y1= ', Y1, '\n', 'X1= ', X1)
    betta = np.dot(np.dot(np.linalg.inv(np.dot(X1.T, X1)), X1.T), Y1)
    return betta

if __name__ == '__main__':
    directory = os.path.join('D:/', 'teleskop_data', '218_str6sec3')
    print(directory)
    exemple()
    calibrate_from_file(directory)
