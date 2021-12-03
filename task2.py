def inputs(file):
    file_open = open(file, 'r')
    data = [int(i) for i in file_open.read().split()]
    del data[0]
    return data


def traceroute(current_index, data, count_depth):
    current_index_original = current_index
    counter = 0
    step = 0

    while count_depth[current_index] == 0 or count_depth[current_index] < 0:
        step += 1
        counter += 1
        # data[current_index] - нынешний элемент, а data[parent_element_index] - родитель
        parent_element_index = data[current_index]
        # если родительским элементом указано -1 - то выходим
        if parent_element_index == -1:
            break
        # если для родительского элемента глубина уже посчитана - то просто добавляем к счётчику её и выходим
        if count_depth[parent_element_index] != 0:
            counter += count_depth[parent_element_index]
            break
        else:
            # иначе переходим к следующему элементу
            # а также стоит отнять от родительского элемента step, чтобы потом по всему пути добавить ответ
            count_depth[parent_element_index] = -1 * step
            current_index = parent_element_index

    # если мы тут, то ответ для запрашиваемого числа готов, но мы также запишем ответ для всех чисел, что стояли на пути
    for i in range(step):
        count_depth[current_index_original] += counter
        current_index_original = data[current_index_original]


def main():
    data = inputs('input.txt')
    file_out = open('output.txt', 'w')
    count_depth = [0] * len(data)

    # проходимся по всем узлам
    for i in range(len(data)):
        # если значение для этого элемента ещё не было подсчитано
        if count_depth[i] == 0:
            # рассчитываем на маршруте от этого элемента к корню глубину элемента на каждом шаге, записываем её в массив
            traceroute(i, data, count_depth)

    file_out.write(str(max(count_depth)))


main()
