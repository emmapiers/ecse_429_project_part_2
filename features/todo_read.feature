Feature: Making sure that todo items can be read
  As a student user of the rest api todo list manager, I want to retrieve todo list items 
  from the server so that I can plan what tasks I will accomplish this week.

  Background: 
    Given the API server is running
    Then delete all the current todos
    And post the todo item with the following JSON body
     """
      {
          "title": "ECSE 429 Homework",
          "description": "Write user stories",
          "doneStatus": "false"
      }
     """
     And post the todo item with the following JSON body
     """
      {
          "title": "Study for Midterm",
          "description": "Read chapter 1 and 2",
          "doneStatus": "true"
      }
     """

  Scenario Outline: successfully reading the current todo list tasks
    Given the todo list contains <beforeLength> items
    When the user sends a GET request
    Then the server responds with <statusCode>
    And the todo list now contains <length> items
  
  Examples:
    | beforeLength | statusCode | length | 
    | 2            | 200        |  2     |

  Scenario Outline: successfully reading the current todo items with a specific query
    When the user sends a GET request with the query <query>
    Then the server responds with <statusCode>
    And the returned list only contains todos with the value <value> in field <field>
  
  Examples:
    | query                       | value             | field         | statusCode |
    | ?doneStatus=false           | false             | doneStatus    | 200        |
    | ?doneStatus=true            | true              | doneStatus    | 200        |
    | ?title="Study for Midterm"  | Study for Midterm | title         | 200        |


  Scenario Outline: unsuccessfully reading a todo list task with an invalid id
    When the user sends a GET request with id <task_id>
    Then the server responds with <statusCode>
    

  Examples:
    | task_id  | statusCode |
    | -12      | 404        |
    | banana   | 404        |


