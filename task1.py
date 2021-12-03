def inputs(file):
    file_open = open(file, 'r')
    data = [int(i) for i in file_open.read().split()]
    del data[0]
    return data


def outputs(file, flag):
    file_open = open(file, 'w')
    if flag:
        file_open.write('YES')
    else:
        file_open.write('NO')


def is_valid(data, index_given):
    if 2 * index_given + 1 < len(data):
        if data[2 * index_given + 1] < data[index_given]:
            return False
    if 2 * index_given + 2 < len(data):
        if data[2 * index_given + 2] < data[index_given]:
            return False
    return True


def main():
    data = inputs('input.txt')
    flag = True
    for i in range(len(data)):
        if not is_valid(data, i):
            flag = False
            break

    outputs('output.txt', flag)


main()
