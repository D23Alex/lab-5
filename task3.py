# к нам посутпает файл с временной отметкой, затем мы отсчитываем , сколько времени прошло - соответственно
# обрабатываем в процессоре файл и по окончании обработки запрашиваем ещё файлы из буфера
# файл затем либо добавляется в буфер, либо исчезает
# у меня проблема будет - что процессор слишком умный и он успевает обработать файлы пришедшие в 1 время при пустом
# процесоре и 1 месте в буфере


from lab4classes import QueueWithLengthAndSum


# класс системы - имеет процессор, характеризующийся временем, что осталось на обработку 1 файла и буфер,
# имеющий размер хранилища и представляющий очередь
class System:
    def __init__(self, buffer_storage):
        self.buffer = QueueWithLengthAndSum()
        self.processor_time_to_finish = 0
        self.buffer_storage = buffer_storage
        self.current_time = 0

    # обработка файла пришедшего в определённое время и обрабатывающегося определённое время
    def process_the_file(self, arrival_time, time_to_process):
        is_taken = False
        # рассчитаем, сколько времени прошло с предыдущего файла
        time_left = arrival_time - self.current_time
        # обновим часы
        self.current_time = arrival_time

        while time_left > 0 and (self.buffer.sum + self.processor_time_to_finish > 0):
            # если времени прошло больше, чем требуется текущему файлу в обработке:
            if self.processor_time_to_finish <= time_left:
                time_left -= self.processor_time_to_finish
                self.processor_time_to_finish = 0
                if self.buffer.length != 0:
                    self.processor_time_to_finish = self.buffer.pop()
            else:
                # если мы тут, то значит прошло недостаточно времени, чтобы файл обработался
                self.processor_time_to_finish -= time_left
                time_left = 0
        # если мы уже здесь - то можем быть уверены, что всё время прошло и пора кидать файл в буфер

        # если ничего не обрабатывается - то можно закинуть файл из буфера на обработку
        # if self.processor_time_to_finish == 0 and self.buffer.length != 0:
            # self.processor_time_to_finish = self.buffer.pop()

        # надо рассчитать время, которое займёт обработка всех пакетов до того, который только что поступил
        time_required = self.buffer.sum + self.processor_time_to_finish

        # кинем файл в буфер(теперь буфер 100% не пуст) и снова проверим, вдруг сейчас ничего не обрабатывается
        if self.buffer.length < self.buffer_storage:
            is_taken = True
            self.buffer.push(time_to_process)
        # вот эту штуку возможно придётся убрать
        # if self.processor_time_to_finish == 0:
            # self.processor_time_to_finish = self.buffer.pop()

        # всё на данном шаге всё сделано, осталось вывести либо время поступления на обработку, либо -1
        if is_taken:
            return time_required + self.current_time
        return -1


def inputs(file_name):
    file_open = open(file_name, 'r')
    data = [int(i) for i in file_open.read().split()]
    return data


def main():
    data = inputs('input.txt')
    file_out = open('output.txt', 'a')

    system = System(data[0])
    for i in range(2, len(data) - 1, 2):
        file_out.write(str(system.process_the_file(data[i], data[i + 1])) + '\n')
    file_out.close()


main()
