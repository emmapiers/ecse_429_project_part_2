import requests
import json
from behave import given, when, then
from features.utils import convert_doneStatus_to_bool  # Assuming this utility function exists

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"

@given('POST a todo item with the following JSON body')
def step_post_todo(context):
    #Prepare the todo item for posting
    todo = json.loads(context.text)
    convert_doneStatus_to_bool(todo)

    response = requests.post(url_todos, json=todo)
    assert response.status_code == 201

    #Add to context
    created_todo = response.json()
    context.todo_id = created_todo.get("id")
    context.original_todo = created_todo

@given('the todo list contains {beforeLength} items')
def step_check_initial_todo_length(context, beforeLength):
    response = requests.get(url_todos)
    assert response.status_code == 200, "Failed to retrieve the updated todo list."
    
    #Make sure no errors in retrieving the todos
    try:
        todos_returned = response.json().get('todos', [])
    except requests.exceptions.JSONDecodeError:
        raise AssertionError("The response did not contain valid JSON data.")
 
    context.length = beforeLength

    assert len(todos_returned) == int(beforeLength)

@when('the user sends a DELETE request for a todo with title {titleToDelete}')
def step_user_sends_delete_request_for_title(context, titleToDelete):
    response = requests.get(url_todos)
    todos = response.json().get('todos', [])
    
    #Find the todo to delete
    context.response = None
    for todo in todos:
        if todo['title'] == titleToDelete:
            todo_id = todo['id']
            delete_response = requests.delete(f"{url_todos}/{todo_id}")
            context.response = delete_response
            break
    
    assert context.response is not None, f"Todo with title '{titleToDelete}' not found."

@then('the returned list only contains todos WITHOUT the value {value} in field {field}')
def step_check_returned_list_for_values(context, value, field):
    response = requests.get(url_todos)
    assert response.status_code == 200

    todos_returned = response.json().get('todos', [])
    for todo in todos_returned:
        actual_value = todo.get(field)
        assert str(actual_value) != value

@given('the user sends a GET request with the query {query}')
def step_send_get_with_query(context, query):
    response = requests.get(f"{url_todos}{query}")
    context.reponse = response
    assert response.status_code == 200

    #Store the list of todos in the context for deletion
    todos = response.json().get("todos", [])
    context.todos_to_delete = [todo["id"] for todo in todos]

@when('the user sends DELETE request(s) to the result of the query')
def step_delete_todos_from_query(context):
    #Send delete requests for each todo by ID
    context.delete_responses = []
    for todo_id in context.todos_to_delete:
        delete_response = requests.delete(f"{url_todos}/{todo_id}")
        context.delete_responses.append(delete_response)
        
        #Store each response for future steps 
        assert delete_response.status_code == 200
    
@then('the todo list now contains {length} items')
def step_check_returned_length(context, length):
    response = requests.get(url_todos)
    assert response.status_code == 200
    
    #Make sure no errors in retrieving the todos
    try:
        todos_returned = response.json().get('todos', [])
    except requests.exceptions.JSONDecodeError:
        raise AssertionError("The response did not contain valid JSON data.")

    assert len(todos_returned) == int(length)

@then('the server responds with status code {statusCode} for all the deleted todos')
def step_check_delete_status_codes(context, statusCode):
    expected_status_code = int(statusCode)
    for delete_response in context.delete_responses:
        actual_status_code = delete_response.status_code
        assert actual_status_code == expected_status_code

@when('the user sends a DELETE request with {task_id}')
def step_send_delete_request_with_id(context, task_id):
    response = requests.delete(f"{url_todos}/{task_id}")
    context.response = response
