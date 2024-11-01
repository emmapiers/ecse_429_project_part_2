from behave import *
import requests
import json
from features.utils import *

url = "http://localhost:4567"
url_todos = "http://localhost:4567/todos"

@given('the user sends a POST request with the following JSON body')
def step_post_todo_header(context):
    #Prepare todo
    todo = json.loads(context.text)
    convert_doneStatus_to_bool(todo)

    response = requests.post(url_todos, json=todo)
    assert response.status_code == 201, f"Failed to create todo item: {response.text}"

    #Add to context
    created_todo = response.json()
    context.todo_id = created_todo.get("id")
    context.original_todo = created_todo

@when('a GET request is sent with the header {header}')
def step_get_todo_with_header(context, header):
    headers = {
        "Accept": header
    }
    response = requests.get(f"{url_todos}/{context.todo_id}", headers=headers)
    
    context.response = response
    context.header = header

@then('the todo list is returned in {requestedFormat} format')
def step_check_response_format(context, requestedFormat):
    if requestedFormat == "xml":
        assert context.header == "application/xml"
        assert context.response.headers['Content-Type'].startswith("application/xml")
    elif requestedFormat == "json":
        assert context.header == "application/json"
        assert context.response.headers['Content-Type'].startswith("application/json")
  
@given('the user sends a POST request with the following XML body')
def step_post_todo_item_xml(context):
    #Prepare xml todo for posting
    todo_xml = context.text
    headers = {
        "Content-Type": "application/xml"
    }
    
    response = requests.post(url_todos, data=todo_xml, headers=headers)
    assert response.status_code == 201

    #Add to context
    created_todo = response.json()
    context.todo_id = created_todo.get("id")
    context.original_todo = created_todo
 


