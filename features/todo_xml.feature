Feature: Making sure responses can be received in xml format
  As an admin, I want to ensure I can receive todo list items in XML format 
  so that I can verify compatibility across formats to meet different system requirements.

  Background: 
    Given the API server is running
    Then delete all the current todos
 
  Scenario Outline: successfully returning the todo list in xml format if todo posted in JSON format
    Given the user sends a POST request with the following JSON body
    """
    {
      "title": "<title>",
      "description": "<description>",
      "doneStatus": "<doneStatus>"
    }
    """
    When a GET request is sent with the header <header>
    Then the server responds with <statusCode>
    And the todo list is returned in <requestedFormat> format
  
  Examples:
    | title     | description  | doneStatus | header            | statusCode | requestedFormat |
    | Title 1   | desc. 1      | false      | application/xml   | 200        | xml             |
    | Title 2   | desc. 2      | false      | application/xml   | 200        | xml             |
    | Title 2   | desc. 2      | false      | application/json  | 200        | json            |
    | Title 3   | desc. 3      | false      | application/xml   | 200        | xml             |


  Scenario Outline: successfully returning the todo list in xml format if todo posted in XML format
    Given the user sends a POST request with the following XML body
    """
        <todo>
            <title><titleToAdd></title>
            <description><descriptionToAdd></description>
            <doneStatus><doneStatusToAdd></doneStatus>
        </todo>
    """
    When a GET request is sent with the header <header>
    Then the server responds with <statusCode>
    And the todo list is returned in <requestedFormat> format
  
  Examples:
    | titleToAdd          | descriptionToAdd          | doneStatusToAdd | header            | statusCode | requestedFormat |
    | ECSE 429 Homework   | Write user stories        | false           | application/xml   | 200        | xml             |
    | Study for Midterm   | Read chapter 1 and 2      | false           | application/xml   | 200        | xml             |
    | Buy groceries       | Get cereal                | false           | application/json  | 200        | json            |
    | Buy groceries       | Get cereal                | false           | application/xml   | 200        | xml             |


   Scenario Outline: unsuccessfully returning the todo list in xml format due to malformatting of accept header
    Given the user sends a POST request with the following XML body:
    """
        <todo>
            <title><titleToAdd></title>
            <description><descriptionToAdd></description>
            <doneStatus><doneStatusToAdd></doneStatus>
        </todo>
    """
    When a GET request is sent with the header <header>
    Then the server responds with <statusCode>
  
  Examples:
    | titleToAdd     | descriptionToAdd   | doneStatusToAdd | header                | statusCode | requestedFormat |
    | Title 1        | desc. 1            | false           | application/invalid   | 406        | xml             |
   
 