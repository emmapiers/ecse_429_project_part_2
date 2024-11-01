import requests
import random

url = "http://localhost:4567/todos"
url2 = "http://localhost:4567"


'''
#Run in sequential order
def before_all(context):
    print("========================================================================================================================")
    print("Running scenarios and examples in random order:")
    i = 1
    for feature in context._runner.features:  
        for scenario in feature.scenarios:
            print(f"{i}. FEATURE: {scenario.feature.name} ")
            print(f"    SCENARIO: {scenario.name} from feature")
            i = i+1
            for example in scenario.examples:
                print(f"       Random Example Order: {example.table.rows}")
                print("========================================================================================================================")
'''
#Run in random order
def before_all(context):
    all_scenarios = []
    for feature in context._runner.features:
        #Find scenario outlines
        for scenario_outline in feature.scenarios:
            if hasattr(scenario_outline, 'examples'):
                #Shuffle the examples within each scenario outline
                for example in scenario_outline.examples:
                    random.shuffle(example.table.rows)

        all_scenarios.extend(feature.scenarios)

    #Shuffle the scenarios randomly
    random.shuffle(all_scenarios)
    
    #Print the order of scenarios and examples
    print("========================================================================================================================")
    print("Running scenarios and examples in random order:")
    for i, scenario in enumerate(all_scenarios, start=1):
        print("========================================================================================================================")
        print(f"{i}. FEATURE: {scenario.feature.name} ")
        print(f"    SCENARIO: {scenario.name} from feature")
        if hasattr(scenario, 'examples'):
            for example in scenario.examples:
                print(f"       Random Example Order: {example.table.rows}")
    print("========================================================================================================================")

def before_scenario(context, scenario):
    #Save initial state
    response = requests.get(url)
    context.initial_todo_list = response.json().get('todos', [])

def after_scenario(context, scenario):
    response = requests.get(url)
    todos = response.json().get('todos', [])

    #Delete every todo
    for todo in todos:
        todo_id = todo["id"]
        delete_response = requests.delete(f"{url}/{todo_id}")
        assert delete_response.status_code == 200, f"Failed to delete todo {todo_id}"

    #Repost the initial todos to restore initial state
    for todo in context.initial_todo_list:
        #Remove the id and turn doneStatus into a boolean
        if 'id' in todo:
            del todo['id']
        if todo['doneStatus'] == "true":
            todo['doneStatus']=True
        elif todo['doneStatus'] == "false":
            todo['doneStatus']=False
  
        response = requests.post(url, json=todo)
        assert response.status_code == 201, f"Failed to restore todo item: {response.text}"
    