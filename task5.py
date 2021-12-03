from random import randint


def swap(array_given, index1, index2):
    array_given[index1], array_given[index2] = array_given[index2], array_given[index1]


# мы находимся в двоичном дереве, но данный элемент, возможно, стоит неверно
def min_heapify(array_given, index, actual_length):
    left_child_id = index * 2 + 1
    right_child_id = index * 2 + 2

    # если существует левый ребёнок
    if left_child_id < actual_length:
        if right_child_id < actual_length:
            # если существуют левый и правый
            if array_given[index] > min(array_given[right_child_id], array_given[left_child_id]):
                # если правый минимальный - то меняем с правым, иначе с левым
                if array_given[right_child_id] < array_given[left_child_id]:
                    swap(array_given, index, right_child_id)
                    min_heapify(array_given, right_child_id, actual_length)
                else:
                    swap(array_given, index, left_child_id)
                    min_heapify(array_given, left_child_id, actual_length)
        else:
            # если существует только левый
            if array_given[left_child_id] < array_given[index]:
                swap(array_given, left_child_id, index)


# процедура построения двоичного дерева из данного массива
def make_sorting_tree(array_given):
    # 2 половина элементов - листья, они уже отсортированы, мы их не трогаем.
    for i in range((len(array_given) - 1) // 2, -1, - 1):
        min_heapify(array_given, i, len(array_given))


# процедура построения отсортированного массива из нашей кучи
def heap(array_given):
    actual_length = len(array_given)
    for i in range(len(array_given), 0, -1):
        actual_length -= 1
        # на вершине точно находится самый большой элемент из оставшихся, его в конец, настоящую длину уменьшить,
        # а на место вершины пойдёт элемент с индексом actual_length, что может быть сломает кучу,
        # так что кучу придётся починить с помощью max_heapify
        swap(array_given, actual_length, 0)
        min_heapify(array_given, 0, actual_length)


# сортировка кучей
def heap_sort(array_given):
    # сначала сделаем двоичную кучу из нашего массива
    make_sorting_tree(array_given)
    # а теперь отсортируем кучу
    heap(array_given)


# опускает вершину пирамиды на место
def min_heapify_special(array_given, index):
    left_child_id = index * 2 + 1
    right_child_id = index * 2 + 2

    # если существует левый ребёнок
    if left_child_id < len(array_given):
        if right_child_id < len(array_given):
            # если существуют левый и правый
            if array_given[index][0] >= min(array_given[right_child_id][0], array_given[left_child_id][0]):
                # если правый минимальный - то меняем с правым, иначе с левым
                # тут мы используем хитрое сравнение кортежей в пайтоне
                if array_given[right_child_id] < array_given[left_child_id]:
                    if array_given[right_child_id][0] < array_given[index][0] \
                            or (array_given[right_child_id][0] == array_given[index][0]
                                and array_given[right_child_id][1] < array_given[index][1]):
                        swap(array_given, right_child_id, index)
                        min_heapify_special(array_given, right_child_id)
                else:
                    if array_given[left_child_id][0] < array_given[index][0] \
                            or (array_given[left_child_id][0] == array_given[index][0]
                                and array_given[left_child_id][1] < array_given[index][1]):
                        swap(array_given, left_child_id, index)
                        min_heapify_special(array_given, left_child_id)
        else:
            # если существует только левый
            if array_given[left_child_id][0] < array_given[index][0]\
                    or (array_given[left_child_id][0] == array_given[index][0]
                        and array_given[left_child_id][1] < array_given[index][1]):
                swap(array_given, left_child_id, index)


def inputs(file):
    file_open = open(file, 'r')
    processes = [int(i) for i in file_open.read().split()]

    data = []
    for i in range(processes[0]):
        data.append((0, i))

    del processes[0]
    del processes[0]
    return data, processes


def outputs(file, cortege):
    file_out = open(file, 'a')
    file_out.write(str(cortege[1]) + ' ' + str(cortege[0]) + '\n')


def main():
    data, processes = inputs('input.txt')
    # сделаем дерево data
    make_sorting_tree(data)

    for i in range(len(processes)):
        # мы знаем, что обработан он будет потоком, который на вершине. запишем в файл
        outputs('output.txt', data[0])
        # теперь добавим время к этой штуке и опустим в нужное место
        data[0] = (data[0][0] + processes[i], data[0][1])
        min_heapify_special(data, 0)


main()

# короче тут мы абьюзим то как в пайтоне сравниваются кортежи. Вторым элементом кортежа идёт приоритет.
# без всяких классов - легко(я бездарь)
