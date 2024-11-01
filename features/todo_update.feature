Feature: Making sure that todo items can be updated
  As a mother using the rest api todo list manager, I want to update todo items from my list 
  so that my todo list accurately reflects the tasks I need to accomplish.

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

  Scenario Outline: successfully updating a todo task using a PUT request
    When the user sends a PUT request with the <updated_field> field updated to <updated_value>
    Then the server responds with <statusCode>
    And the returned list confirms the field is updated correctly
  
  Examples:
    | updated_field | updated_value  | statusCode |
    | description  | Set up lunch    | 200        |
    | doneStatus   | true            | 200        |
    | title        | Call Todd       | 200        |


  Scenario Outline: successfully updating a todo task using a POST request
    When the user sends a POST request with the <updated_field> field updated to <updated_value>
    Then the server responds with <statusCode>
    And the returned list confirms the field is updated correctly
  
  Examples:
    | updated_field | updated_value  | statusCode |
    | description  | Set up lunch    | 200        |
    | doneStatus   | true            | 200        |
    | title        | Call Todd       | 200        |


  Scenario Outline: unsuccessfully updating a todo task due to the field being invalid
    When the user sends a PUT request with the <updated_field> field updated to <updated_value>
    Then the server responds with <statusCode>
    And the returned list confirms the field is NOT updated correctly

  Examples:
    | updated_field | updated_value  | statusCode |
    | wrong_field   | wrong_value    | 400        |
    | wrong_title   | Call Julie     | 400        |






