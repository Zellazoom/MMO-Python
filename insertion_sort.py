

def insertion_sort(list):
    selected_index = 1
    while selected_index < len(list):
        Index_old = selected_index
        Index_new = Index_old - 1
        for i in reversed(list[:selected_index]):
            if list[Index_old][1] > i[1]:
                z = list[Index_new]
                list[Index_new] = list[Index_old]
                list[Index_old] = z
                Index_old = Index_new
                Index_new -= 1
            else:
                pass
        selected_index += 1

    return_list = []
    for j in list:
        return_list.append(j[0])

    return return_list