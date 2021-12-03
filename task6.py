import math


class QueueElement:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class QueueElementWithIndex(QueueElement):
    def __init__(self, key, value, index):
        self.index = index
        QueueElement.__init__(self, key, value)


# наименьший аргумент вверху
# этот класс всё делает по индексам
# Также нельзя использовать в swap отрицательные индексы, так как в подклассе для 6 задачи штука может сломаться
# (но это не точно)
class QueuePriority:
    def __init__(self, is_binary_tree=False, array_given=None):
        self.array = []
        if array_given is not None:
            for i in range(len(array_given)):
                self.array.append(QueueElement(array_given[i][0], array_given[i][1]))

        if not is_binary_tree and array_given is not None:
            self.make_sorting_tree()

    def pop(self, pop_key=False):
        self.swap(self.length() - 1, 0)
        if pop_key:
            to_return = self.array.pop().key
        else:
            to_return = self.array.pop().value
        self.min_heapify(0)
        return to_return

    def length(self):
        return len(self.array)

    def swap(self, index1, index2):
        q = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = q

    def min_heapify(self, index):
        left_child_id = index * 2 + 1
        right_child_id = index * 2 + 2

        # если существует левый ребёнок
        if left_child_id < self.length():
            if right_child_id < self.length():
                # если существуют левый и правый
                if self.array[index].key > min(self.array[right_child_id].key, self.array[left_child_id].key):
                    # если правый максимальный - то меняем с правым, иначе с левым
                    if self.array[right_child_id].key < self.array[left_child_id].key:
                        self.swap(index, right_child_id)
                        self.min_heapify(right_child_id)
                    else:
                        self.swap(index, left_child_id)
                        self.min_heapify(left_child_id)
            else:
                # если существует только левый
                if self.array[left_child_id].key < self.array[index].key:
                    self.swap(left_child_id, index)

    # получаем индекс элемента, индекс которого понижается, а затем его надо(вероятно) отправить вверх на новое место
    def decrease_key(self, index, key):
        self.array[index].key = key
        # если мы не на вершине а родительский элемент больше нашего - меняем
        while index > 0 and self.array[(index - 1) // 2].key > self.array[index].key:
            self.swap(index, (index - 1) // 2)
            index = (index - 1) // 2

    def push(self, key, value):
        self.array.append(QueueElement(key, value))
        self.decrease_key(self.length() - 1, key)

    def make_sorting_tree(self):
        for i in range(self.length() - 1 // 2, -1, - 1):
            self.min_heapify(i)


# наименьший аргумент вверху
# этот класс decrease_key_by_link делает по ссылкам на объекты
# и здесь пушить будем заранее созданный объект класса
class QueuePriorityWithIndexes(QueuePriority):
    def __init__(self, is_binary_tree=False, array_given=None):
        self.array = []
        if array_given is not None:
            for i in range(len(array_given)):
                self.array.append(QueueElementWithIndex(array_given[i][0], array_given[i][1], i))

        if not is_binary_tree:
            self.make_sorting_tree()

    def push(self, object_link):
        # сначала новый элемент становится на последнее место
        self.array.append(object_link)
        self.decrease_key(self.length() - 1, object_link.key)

    # метод находит объект по заданной ссылке и выполняет для него decrease_key
    def decrease_key_by_link(self, object_link, key):
        self.decrease_key(object_link.index, key)

    # метод свап теперь должен и переставлять занимаемые индексы в массиве между собой
    def swap(self, index1, index2):
        QueuePriority.swap(self, index1, index2)
        self.array[index1].index = index1
        self.array[index2].index = index2


def test():
    a = [(7, 7), (2, 2), (1, 1), (4, 4), (3, 3), (5, 5), (6, 6)]
    queue = QueuePriorityWithIndexes(False, a)


def execute(queue, commands, current_index, file_out):
    if commands[current_index][0] == 'X':
        if queue.length() == 0:
            file_out.write('*')
        else:
            file_out.write(str(queue.pop(True)) + '\n')
    # договоримся, что key - число, а value в данной задаче - строка(чтоб не переводить туда-обратно)
    elif commands[current_index][0] == 'A':
        # создадим новый объект и запушим ссылку на него
        new_el = QueueElementWithIndex(int(commands[current_index][1]), commands[current_index][1], queue.length())
        queue.push(new_el)
        # и теперь в commands[current_index] запишем ссылку на этот эбъект, чтобы потом по ней можно было обратиться
        commands[current_index] = new_el
    else:
        # если задано изменить значение -
        # то тогда обращаемся к ранее созданной ссылке в ячейке массива commands на месте commands[current_index][1]
        queue.decrease_key_by_link(commands[int(commands[current_index][1]) - 1], int(commands[current_index][2]))


def inputs(file_name):
    file_open = open(file_name, 'r')
    data = []
    while True:
        # считываем строку
        line = file_open.readline()
        # прерываем цикл, если строка пустая
        if not line:
            break
        data.append([i for i in line.split()])
    del data[0]
    file_open.close()
    return data


# идея задачи - после того, как мы добавляем элемент в очередь, в этой ячейке массива со всеми командами будем хранить
# уже не эту команду, а ссылку на добавленный только что элемент. Потом мы обратимся по номеру это ячейки,
# получим ссылку, а наш новый подкласс по ссылке даст нам получить номер элемента в самом массиве,
# а уже имея номер элемента в массиве, мы легко сделаем привычную операцию подъёма вверх
def main():
    commands = inputs('input.txt')
    file_out = open('output.txt', 'a')

    queue = QueuePriorityWithIndexes()

    for i in range(len(commands)):
        execute(queue, commands, i, file_out)

    file_out.close()


main()
