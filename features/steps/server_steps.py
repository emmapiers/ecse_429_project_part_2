import requests
import json
from behave import *
from features.utils import convert_doneStatus_to_bool
import sys

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"

@given('the API server is running') 
def step_given_server_is_running(context):
    try:
        response = requests.get(url)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {url}. Please ensure the server is running.")
        sys.exit(1)  # Exit the test suite if the server is not available
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error occurred while connecting to the server: {e}")
        sys.exit(1)  # Exit t


@then('delete all the current todos')
def step_set_initial_state(context):
    response = requests.get(url_todos)
    todos = response.json().get('todos', [])  #Get all todos

    #Delete each todo individually
    for todo in todos:
        todo_id = todo["id"]
        delete_response = requests.delete(f"{url_todos}/{todo_id}")
        assert delete_response.status_code == 200

@then('post the todo item with the following JSON body')
def step_post_todo(context):
    # Debug: Check what context.text contains


    # Parse and prepare the todo item for posting
    todo = json.loads(context.text)
    convert_doneStatus_to_bool(todo)
 

    response = requests.post(url_todos, json=todo)


    assert response.status_code == 201, f"Failed to create todo item: {response.text}"

    created_todo = response.json()
    context.todo_id = created_todo.get("id")
    context.original_todo = created_todo


