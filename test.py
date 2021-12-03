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
                    index = right_child_id
                    swap(array_given, index, right_child_id)
                else:
                    index = left_child_id
                    swap(array_given, index, left_child_id)
        else:
            # если существует только левый
            if array_given[left_child_id] < array_given[index]:
                swap(array_given, left_child_id, index)
                break
