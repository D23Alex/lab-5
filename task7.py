# сортировать будем от больших к меньшим


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
                # если правый максимальный - то меняем с правым, иначе с левым
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


# заменяем рекурсивный вызовы на цикл
def min_heapify_cycle(array_given, index, actual_length):
    while True:
        left_child_id = index * 2 + 1
        right_child_id = index * 2 + 2
        if left_child_id >= actual_length:
            break
        if right_child_id < actual_length:
            # если существуют левый и правый
            if array_given[index] > min(array_given[right_child_id], array_given[left_child_id]):
                # если правый максимальный - то меняем с правым, иначе с левым
                if array_given[right_child_id] < array_given[left_child_id]:
                    swap(array_given, index, right_child_id)
                    index = right_child_id
                else:
                    swap(array_given, index, left_child_id)
                    index = left_child_id
            else:
                break
        else:
            # если существует только левый
            if array_given[left_child_id] < array_given[index]:
                swap(array_given, left_child_id, index)
            break


# процедура построения двоичного дерева из данного массива
def make_sorting_tree(array_given):
    # 2 половина элементов - листья, они уже отсортированы, мы их не трогаем.
    for i in range((len(array_given) - 1) // 2, -1, - 1):
        min_heapify_cycle(array_given, i, len(array_given))


# процедура построения отсортированного массива из нашей кучи
def heap(array_given):
    actual_length = len(array_given)
    for i in range(len(array_given), 0, -1):
        actual_length -= 1
        # на вершине точно находится самый большой элемент из оставшихся, его в конец, настоящую длину уменьшить,
        # а на место вершины пойдёт элемент с индексом actual_length, что может быть сломает кучу,
        # так что кучу придётся починить с помощью max_heapify
        swap(array_given, actual_length, 0)
        min_heapify_cycle(array_given, 0, actual_length)


# сортировка кучей
def heap_sort(array_given):
    # сначала сделаем двоичную кучу из нашего массива
    make_sorting_tree(array_given)
    # а теперь отсортируем кучу
    heap(array_given)


def inputs(file):
    file_open = open(file, 'r')
    data = [int(i) for i in file_open.read().split()]
    del data[0]
    file_open.close()
    return data


def outputs(file, data):
    file_out = open(file, 'w')
    for value in data:
        file_out.write(str(value) + ' ')


# в задании говорится сделать max heapify, но тут надо min heapify
def main():
    data = inputs('input.txt')
    heap_sort(data)
    outputs('output.txt',data)


main()
