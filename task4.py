from random import randint


class Swaps:
    def __init__(self):
        self.swapList = []


def swap(array_given, index1, index2, swaps):
    swaps.swapList.append((index1, index2))
    array_given[index1], array_given[index2] = array_given[index2], array_given[index1]


# мы находимся в двоичном дереве, но данный элемент, возможно, стоит неверно
def min_heapify(array_given, index, actual_length, swaps):
    left_child_id = index * 2 + 1
    right_child_id = index * 2 + 2

    # если существует левый ребёнок
    if left_child_id < actual_length:
        if right_child_id < actual_length:
            # если существуют левый и правый
            if array_given[index] > min(array_given[right_child_id], array_given[left_child_id]):
                # если правый максимальный - то меняем с правым, иначе с левым
                if array_given[right_child_id] < array_given[left_child_id]:
                    swap(array_given, index, right_child_id, swaps)
                    min_heapify(array_given, right_child_id, actual_length, swaps)
                else:
                    swap(array_given, index, left_child_id, swaps)
                    min_heapify(array_given, left_child_id, actual_length, swaps)
        else:
            # если существует только левый
            if array_given[left_child_id] < array_given[index]:
                swap(array_given, left_child_id, index, swaps)


# процедура построения двоичного дерева из данного массива
def make_sorting_tree(array_given):
    swaps = Swaps()
    # 2 половина элементов - листья, они уже отсортированы, мы их не трогаем.
    for i in range((len(array_given) - 1) // 2, -1, - 1):
        min_heapify(array_given, i, len(array_given), swaps)
    return swaps.swapList


def inputs(file):
    file_open = open('input.txt', 'r')
    data = [int(i) for i in file_open.read().split()]
    del data[0]
    file_open.close()
    return data


def outputs(data, file):
    file_out = open(file, 'w')
    file_out.write(str(len(data)) + '\n')
    for current_swap in data:
        file_out.write(str(current_swap[0]) + ' ' + str(current_swap[1]) + '\n')


def main():
    data = inputs('input.txt')
    result = make_sorting_tree(data)
    outputs(result, 'output.txt')


main()
