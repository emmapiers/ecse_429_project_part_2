Feature: Making sure that todo items can be deleted
  As a mother using the rest api todo list manager, I want to delete todo items from my list 
  that are no longer needed so that my todo list accurately reflects the tasks I need to accomplish.

  Background: 
    Given the API server is running
    Then delete all the current todos
    And post the todo item with the following JSON body
     """
      {
          "title": "Call Rebecca",
          "description": "Set up a playdate",
          "doneStatus": "false"
      }
     """
    And post the todo item with the following JSON body
     """
      {
          "title": "Grocery shop",
          "description": "Pick up bananas",
          "doneStatus": "true"
      }
     """

  Scenario Outline: successfully deleting a single todo item
    Given the todo list contains <beforeLength> items
    When the user sends a DELETE request for a todo with title <titleToDelete>
    Then the server responds with <statusCode>
    And the todo list now contains <length> items
  
  Examples:
    | beforeLength | titleToDelete    | length | statusCode |
    | 2            | Call Rebecca     | 1      | 200        |
    | 2            | Grocery shop     | 1      | 200        |


  Scenario Outline: successfully deleting all todo items that were found using a query
    Given the user sends a GET request with the query <query>
    When the user sends DELETE request(s) to the result of the query
    Then the server responds with status code <statusCode> for all the deleted todos
    And the returned list only contains todos WITHOUT the value <value> in field <field>

  Examples:
    | query             | statusCode | value | field      |
    | ?doneStatus=false | 200        | false | doneStatus |
    | ?doneStatus=true  | 200        | true  | doneStatus |


  Scenario Outline: unsuccessfully deleting a todo item with an invalid id 
    When the user sends a DELETE request with id <task_id>
    Then the server responds with <statusCode>

  Examples:
    | task_id  | statusCode |
    | -10      | 404        |
    | yellow   | 404        |






