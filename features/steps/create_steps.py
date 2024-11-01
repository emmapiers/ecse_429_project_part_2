from behave import *
import requests
import json
from features.utils import *

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"


@when('the user sends a POST request with the following JSON body')
def step_post_request(context):
    #Setup the todo for posting
    todo = json.loads(context.text)
    convert_doneStatus_to_bool(todo)

    response = requests.post(url_todos, json=todo)
    
    #Add info to context
    context.new_todo_item = todo
    context.response = response

@then('the new todo item is added to the todo list')
def step_check_todo_added_to_list(context):
    todo_expected = context.new_todo_item

    response = requests.get(url_todos)
    todos_outputted = response.json().get('todos', [])

    #Confirm if one of the todos on the list is equal to the one we posted
    AreEqual = False
    for todo in todos_outputted:
        if 'id' in todo:
            del todo['id']
        if 'doneStatus' in todo:
            convert_doneStatus_to_bool(todo)

        if (todo == todo_expected):
            AreEqual = True
    
    assert AreEqual

@then('the new todo item is NOT added to the todo list')
def step_check_todo_not_added_to_list(context):
    todo_expected = context.new_todo_item

    response = requests.get(url_todos)
    todos_outputted = response.json().get('todos', [])

    #Confirm none of the todos on the list are equal to the one we tried to post
    noneEqual = True
    for todo in todos_outputted:
        if 'id' in todo:
            del todo['id']
        if 'doneStatus' in todo:
            convert_doneStatus_to_bool(todo)

        if (todo == todo_expected):
            noneEqual = False
    
    assert noneEqual

