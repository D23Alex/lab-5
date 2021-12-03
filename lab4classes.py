# Это библиотека классов 4 лабораторной работы

class StackElement:

    def __init__(self, key):
        self.key = key
        self.previous = None


# ограничение - значение key элемента стека не может быть None
class Stack:

    def create_node(self, node_class, key):
        new_element = node_class(key)
        new_element.previous = self.top
        self.top = new_element

    def push(self, object_given):
        if type(object_given) == list:
            for current_element in object_given:
                self.create_node(StackElement, current_element)
        else:
            self.create_node(StackElement, object_given)

    def __init__(self, data=None):
        self.bottom = StackElement(None)
        self.top = self.bottom
        if data is not None:
            self.push(data)

    def pop(self):
        to_return = self.top.key
        self.top = self.top.previous
        # только надо ещё поместить в мусор это всё
        return to_return

    def is_empty(self):
        return self.top.key is None

    # чем левее в массиве - тем ниже в стеке
    def elements(self):
        current_element = self.top
        all_elements = []
        while current_element.key is not None:
            all_elements.append(current_element.key)
            current_element = current_element.previous
        return all_elements


# этот класс - подкласс StackElement'а, который хранит в свойстве max максимальное значение всего что ниже его (TASK 5)
class StackElementWithMax(StackElement):
    def __init__(self, key):
        StackElement.__init__(self, key)
        self.maxim = None


class StackElementWithMin(StackElement):
    def __init__(self, key):
        StackElement.__init__(self, key)
        self.minim = None


# (TASK 5, 7)
class StackWithMax(Stack):
    def create_node(self, node_class, key):
        new_element = node_class(key)
        if self.top.key is None:
            new_element.maxim = new_element.key
        else:
            new_element.maxim = max(new_element.key, self.top.maxim)
        new_element.previous = self.top
        self.top = new_element

    def push(self, object_given):
        if type(object_given) == list:
            for current_element in object_given:
                self.create_node(StackElementWithMax, current_element)
        else:
            self.create_node(StackElementWithMax, object_given)

    def __init__(self, data=None):
        self.bottom = StackElementWithMax(None)
        self.top = self.bottom
        if data is not None:
            self.push(data)

    def maxim(self):
        return self.top.maxim


# (TASK 6)
class StackWithMin(Stack):
    def create_node(self, node_class, key):
        new_element = node_class(key)
        if self.top.key is None:
            new_element.minim = new_element.key
        else:
            new_element.minim = min(new_element.key, self.top.minim)
        new_element.previous = self.top
        self.top = new_element

    def push(self, object_given):
        if type(object_given) == list:
            for current_element in object_given:
                self.create_node(StackElementWithMin, current_element)
        else:
            self.create_node(StackElementWithMin, object_given)

    def __init__(self, data=None):
        self.bottom = StackElementWithMin(None)
        self.top = self.bottom
        if data is not None:
            self.push(data)

    def minim(self):
        return self.top.minim


# класс для обработки постфиксных выражений
# класс предполагает, что арифметическое выражение записано в постфиксном виде корректно, деления на 0 нет, только +-*/
class StackWithCalc(Stack):
    def push(self, object_given):
        if type(object_given) == list:
            for current_element in object_given:
                self.create_node(StackElement, current_element)
                if type(current_element) == str:
                    if self.top.key in '/+*-':
                        self.calc()
        else:
            self.create_node(StackElement, object_given)
            if type(self.top.key) == str:
                self.calc()

    def calc(self):
        # тут можно было бы кидать лишние 2 элемента в мусор
        action = self.top.key
        element_to_replace = self.top.previous.previous
        op1 = self.top.previous.key
        op2 = self.top.previous.previous.key
        if action == '+':
            element_to_replace.key = op2 + op1
        elif action == '-':
            element_to_replace.key = op2 - op1
        elif action == '*':
            element_to_replace.key = op2 * op1
        else:
            element_to_replace.key = op2 / op1
        # теперь на вершине элемент со значением element_to_replace
        self.top = element_to_replace


class QueueElement:
    def __init__(self, key, previous_el=None, next_el=None):
        self.key = key
        self.previous = previous_el
        self.next = next_el


class Queue:
    def __init__(self, data=None):
        self.first = QueueElement(None)
        self.last = self.first
        if data is not None:
            self.push(data)

    def create_node(self, node_class, key):
        new_node = node_class(key, self.last)
        self.last.next = new_node
        self.last = new_node

    def push(self, object_given):
        if type(object_given) == list:
            for current_element in object_given:
                self.create_node(QueueElement, current_element)
        else:
            self.create_node(QueueElement, object_given)

    # в очереди pop - достать элемент из начала
    def pop(self):
        # self.first - это не первый элемент очереди! Это элемент, key которого - None и
        # который содержит ссылку на настоящий первый элемент в свойстве next
        # тоже можно вызвать мусорку - но вообще python сам справляется с такими вещами
        to_return = self.first.next.key

        # если предыдущий элемент - это начало то есть если в очереди всего 1 элемент
        if self.last.previous.key is None:
            # тогда фактически повторяем действия инита
            self.first.next = None
            self.last = self.first
            return to_return

        self.first.next.next.previous = self.first
        self.first.next = self.first.next.next
        return to_return

    # если вызвать на на пустой очпереди - всё плохо
    def elements(self):
        if self.is_empty():
            return 0
        all_elements = []
        current_element = self.first.next
        while True:
            all_elements.append(current_element.key)
            if current_element.next is None:
                break
            current_element = current_element.next
        return all_elements

    def is_empty(self):
        return self.last.key is None


# наследник класса очередь, но хранящий в свойстве average ссылку на средний элемент
# (за которым, по условию №9 встанет новый элемент очереди)
# каждый если у нас было чётное кол-во элементов - при push или pop средний элемент сдвигается на 1,
# иначе ничего не проиходит.
class QueueWithAverage(Queue):
    def __init__(self, data=None):
        self.first = QueueElement(None)
        self.last = self.first
        self.average = self.first
        self.isEven = True
        if data is not None:
            self.push(data)

    def create_node(self, node_class, key):
        Queue.create_node(self, node_class, key)
        if self.isEven:
            self.average = self.average.next
            self.isEven = False
        else:
            self.isEven = True

    def pop(self):
        if self.last.previous.key is None:
            self.average = self.first
            self.isEven = True

        elif self.isEven:
            self.average = self.average.next
            self.isEven = False
        else:
            self.isEven = True
        return Queue.pop(self)

    def put_in_the_middle(self, value):
        if self.average.key is None:
            Queue.push(self, value)
        new_node = QueueElement(value, self.average, self.average.next)
        self.average.next = new_node
        self.average.next.previous = new_node


# этот класс - для задачи 10 и его единственное отличие - свойство length
class QueueWithLength(Queue):
    def __init__(self, data=None):
        self.length = 0
        Queue.__init__(self, data)

    def create_node(self, node_class, key):
        self.length += 1
        Queue.create_node(self, node_class, key)

    def pop(self):
        self.length -= 1
        return Queue.pop(self)

    # выпускает из очереди людей, которые к указанному времени должны её покинуть
    def let_people_out(self, current_time):
        current_element = self.first.next
        while current_element is not None:
            # если времени ещё меньше, чем время выхода чела - то прекращаем
            if current_time < current_element.key:
                break
            # иначе выгоняем первого чела
            self.pop()
            current_element = self.first.next


class QueueWithLengthAndSum(Queue):
    def __init__(self, data=None):
        self.length = 0
        self.sum = 0
        Queue.__init__(self, data)

    def create_node(self, node_class, key):
        self.length += 1
        self.sum += key
        Queue.create_node(self, node_class, key)

    def pop(self):
        self.length -= 1
        self.sum -= self.last.key
        return Queue.pop(self)


# Этот класс - для задачи 12. Он поддерживает методы встать в строй слева или справа а также назвать соседей
class QueueArmy(Queue):
    def __init__(self, data=None):
        self.formation = {}
        Queue.__init__(self, data)
        self.formation['1'] = self.last

    # ставим элемент со значением key слева от элемента со значением index
    def insert_left(self, node_class, key, index):
        current_element = self.formation[index]
        new_node = node_class(key, current_element.previous, current_element)

        current_element.previous.next = new_node
        current_element.previous = new_node
        # вставим в наш словарик ссылку на new_node
        self.formation[key] = new_node

    def insert_right(self, node_class, key, index):
        current_element = self.formation[index]
        new_node = node_class(key, current_element, current_element.next)

        if current_element.next is not None:
            current_element.next.previous = new_node
        current_element.next = new_node
        # вставим в наш словарик ссылку на new_node
        self.formation[key] = new_node

    def delete_element(self, key):
        element_to_delete = self.formation[key]
        element_to_delete.previous.next = element_to_delete.next
        if element_to_delete.next is not None:
            element_to_delete.next.previous = element_to_delete.previous
        del self.formation[key]

    def neighbors(self, key):
        current_element = self.formation[key]
        if current_element.previous.key is None:
            left = '0'
        else:
            left = current_element.previous.key
        if current_element.next is None:
            right = '0'
        else:
            right = current_element.next.key
        return left, right


# очередь сделанная на основе двух стэков - является решением заданий 6 и 7
class QueueWithStacks:
    def __init__(self, stack_class):
        self.stack1 = stack_class()
        self.stack2 = stack_class()

    def push(self, key):
        self.stack1.push(key)

    def pop(self):
        self.fake_pop()
        return self.stack2.pop()

    def fake_pop(self):
        # если в stack2 пусто - то перенести все элементы из первого стака во второй. иначе просто взять из первого
        if self.stack2.is_empty():
            while True:
                if self.stack1.is_empty():
                    break
                key = self.stack1.pop()
                self.stack2.push(key)

    def minim(self):
        s1_min = self.stack1.minim()
        s2_min = self.stack2.minim()
        if s1_min is None:
            s1_min = 999999999999999999
        elif s2_min is None:
            s2_min = 999999999999999999
        return min(s1_min, s2_min)

    def maxim(self):
        s1_max = self.stack1.maxim()
        s2_max = self.stack2.maxim()
        if s1_max is None:
            s1_max = -999999999999999999
        elif s2_max is None:
            s2_max = -999999999999999999
        return max(s1_max, s2_max)


def queue_test():
    queue = QueueWithStacks(StackWithMin)
    queue.push(1)
    print(queue.minim())
    queue.push(-22)
    print(queue.minim())
    queue.push(-3)
    print(queue.minim())
    queue.push(-4)
    print(queue.minim())
    queue.push(-5)
    print(queue.minim())
    queue.pop()
    queue.pop()
    print(queue.minim())

