from behave import *
import requests
from features.utils import *

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"

@when('the user sends a GET request')
def step_get_todo(context):
    response = requests.get(url_todos)
    context.response = response

@when('the user sends a GET request with the query {query}')
def step_send_get_with_query(context, query):
    response = requests.get(f"{url_todos}{query}")
    context.response = response

@then('the returned list only contains todos with the value {value} in field {field}')
def step_check_returned_list_for_query(context, value, field):
    todos_returned = context.response.json().get('todos', [])

    for todo in todos_returned:
        actual_value = todo.get(field)
        assert str(actual_value) == value

@when('the user sends a GET request with {task_id}')
def step_send_get_request_with_id(context, task_id):
    response = requests.get(f"{url_todos}/{task_id}")
    context.response = response


