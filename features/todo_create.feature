Feature: Making sure that todo items can be posted
  As a student user of the rest api todo list manager, I want to add new school items to my todo list 
  so that I can stay organized and keep track of the work I need to complete. 

  Background: 
    Given the API server is running
    Then delete all the current todos
  
  Scenario Outline: Successfully adding a new todo item with all fields present
    When the user sends a POST request with the following JSON body:
    """
    {
      "title": "<title>",
      "description": "<description>",
      "doneStatus": "<doneStatus>"
    }
    """
    Then the server responds with <statusCode>
    And the new todo item is added to the todo list
  
  Examples:
    | title               | description               | doneStatus | statusCode |
    | ECSE 429 Homework   | Write user stories        | false      | 201        |
    | Study for Midterm   | Read chapter 1 & 2        | false      | 201        |
    | Attend Office hours | Ask about use cases       | false      | 201        |

    
  Scenario Outline: successfully adding a new todo item with missing fields
    When the user sends a POST request with the following JSON body:
    """
    {
      "title": "<title>",
      "description": "<description>",
      "doneStatus": "<doneStatus>"
    }
    """
    Then the server responds with <statusCode>
    And the new todo item is added to the todo list
  
  Examples:
    | title               | description               | doneStatus | statusCode |
    | ECSE 429 Homework   |                           | true       | 201        |
    | Study for Midterm   |                           | false      | 201        |

  
  Scenario Outline: unsuccessfully adding a new todo item due to improper inputs
    When the user sends a POST request with the following JSON body:
    """
    {
      "title": "<title>",
      "description": "<description>",
      "doneStatus": "<doneStatus>"
    }
    """
    Then the server responds with <statusCode>
    And the new todo item is NOT added to the todo list
  
  Examples:
    | title               | description               | doneStatus | statusCode |
    |                     | Write user stories        | false      | 400        |
    |                     |                           |            | 400        |
    | Homework 1          | Do webwork                | 6          | 400        |
 

  