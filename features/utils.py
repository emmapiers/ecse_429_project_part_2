
def convert_doneStatus_to_bool(todo):
    if todo.get('doneStatus') == 'false':
        todo['doneStatus'] = False
    elif todo.get('doneStatus') == 'true':
        todo['doneStatus'] = True