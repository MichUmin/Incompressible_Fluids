def scalar(to_print):
    length = len(to_print.values)
    for index in range(length):
        print(to_print.values[index][0])

def scalar_to_string(to_print):
    result = ''
    length = len(to_print)
    for index in range(length-1):
        result += str(to_print[index][0])
        result += ' '
    result += str(to_print[length-1][0])
    return result

def scalar_field_to_string(to_print):
    result = ''
    length = len(to_print.values)
    for index in range(length-1):
        result += str(to_print.values[index][0])
        result += ' '
    result += str(to_print.values[length-1][0])
    return result