import requests
from behave import *
from features.utils import convert_doneStatus_to_bool  # Assuming this utility function exists

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"

@when('the user sends a PUT request with the {updated_field} field updated to {updated_value}')
def step_put_request_with_specific_field(context, updated_field, updated_value):
    todo_id = context.todo_id
    
    #Get current todo item state
    get_response = requests.get(f"{url_todos}/{todo_id}")
    assert get_response.status_code == 200
    
    todos = get_response.json().get('todos', [])
    current_todo = todos[0]

    #Need to remove ID since we cannot use put with an ID according to documentation
    if 'id' in current_todo:
        del current_todo['id']

    #Update todo
    current_todo[updated_field] = updated_value
    convert_doneStatus_to_bool(current_todo)

    #Update context
    context.response = requests.put(f"{url_todos}/{todo_id}", json=current_todo)
    context.updated_field= updated_field
    context.updated_value = updated_value

@then('the server responds with {statusCode}')
def step_check_status_code(context, statusCode):
    actual_status_code = context.response.status_code
    expected_status_code = int(statusCode)

    assert actual_status_code == expected_status_code, (
        f"Expected status code {expected_status_code} but got {actual_status_code}.\n"
        f"Response body: {context.response.text}\n"
    )

@then('the returned list confirms the field is updated correctly')
def step_confirm_field_updated(context):
    #Get todo item
    todo_id = context.todo_id
    
    get_response = requests.get(f"{url_todos}/{todo_id}")
    assert get_response.status_code == 200

    todos = get_response.json().get('todos', [])
    updated_todo = todos[0]

    #Assert updated
    assert updated_todo[context.updated_field] == context.updated_value

@when('the user sends a POST request with the {updated_field} field updated to {updated_value}')
def step_post_request_with_specific_field(context, updated_field, updated_value):
    todo_id = context.todo_id
    
    #Get current todo item state
    get_response = requests.get(f"{url_todos}/{todo_id}")
    assert get_response.status_code == 200
    
    todos = get_response.json().get('todos', [])
    current_todo = todos[0]

    #Need to remove ID since we cannot use put with an ID according to documentation
    if 'id' in current_todo:
        del current_todo['id']

    #Update todo
    current_todo[updated_field] = updated_value
    convert_doneStatus_to_bool(current_todo)

    #Update context
    context.response = requests.post(f"{url_todos}/{todo_id}", json=current_todo)
    context.updated_field= updated_field
    context.updated_value = updated_value

@then('the returned list confirms the field is NOT updated correctly')
def step_confirm_field_not_updated(context):
    #Get todo item
    todo_id = context.todo_id
    
    get_response = requests.get(f"{url_todos}/{todo_id}")
    assert get_response.status_code == 200

    todos = get_response.json().get('todos', [])
    updated_todo = todos[0]

    #Verify that the invalid field was not added
    assert context.updated_field not in updated_todo

    #Confirm that all original fields are unchanged
    original_todo = context.original_todo
    for key in ['title', 'description', 'doneStatus']:
        assert updated_todo[key] == original_todo[key]

