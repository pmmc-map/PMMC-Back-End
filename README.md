# PMMC-Back-End

## Back end
- Consists of a Flask back-end that serves a single HTML file (essentially a route that directs our "/" endpoint).
- Contain our REST API + endpoints that will connect to our database (currently using sqllite, but will switch to MySQL in production).
- Using SQLAlchemy (object oriented database) in order to abstract the SQL queries and make migration to MySQL easier in the future.

### Main priorities of back-end
- Handle the database and database session (Flask sqlalchemy)
- Be able to geocode lat/long coordinated from the front end to city/state/country
- Save confirmed locations in the database
- Send photos of each city back to the front end (as a blob, maybe b64 image?)
- Save responses to survey questions in database

### Local development
To start Flask app for local development in Terminal:  
```python3 app.py```  

Once the local dev server is running, you can access the endpoints at http://127.0.0.1:5000/

### For testing on the server
1. Download pem file (on Slack)
2. Change permissions of the pem file  
```chmod 600 uci-pmmc.pem```
3. ssh into the server using  
```ssh -i uci-pmmc.pem ubuntu@54.183.19.24```
4. Run the app
```sudo python3 app.py```
5. Wait until ```server running``` is printed on the console.

You can now access the 54.183.19.24 in a browser from any IP.

## Endpoint Documentation

### Survey endpoints

#### GET /api/questions
* Returns all (active) questions in the database
* Input parameters: No input parameters
* Response: Json list of questions with `text` and `qid`
* Example:     
```
{
  "questions": [
    {
      "qid": 1,
      "text": "What is your age"
    }
  ]
}
```

#### POST /api/questions 
* Adds a new question to the database
* Input parameters: JSON body with a `text` field defining the text of the new question
* Response: Success

#### DELETE /api/questions
* Deletes a question from the database (by making it inactive)
* Input parameters: JSON body with a `qid` field to define which question should be deleted.
* Response: Success

### GET /api/questions/qid/\<QID>
* Returns the question with qid=QID.
* Input parameters: QID defined in the URL.
* Response: JSON with the question 
* Example: 

```
{
  "question": {
    "qid": 1,
    "text": "What is your age"
  }
}
```


### POST /api/questions/qid/\<QID> 
* Updates a question's text by qid. 
* Input parameters: QID defined in the URL. JSON body with new question text defined as `updated_text`. 
* Response: Success 

#### DELETE /api/questions/qid/\<QID>
* Deletes a question from the database (by making it inactive). 
* NOTE: This is the same as the DELETE request in /api/questions.
* Input parameters: QID defined in URL.
* Response: Success 

#### GET /api/responses
* Returns all responses in the database. 
* NOTE: Refers to responses to questions, not responses submitted by the user.
* Input parameters: None 
* Response: JSON with list of Responses, each associated with an `rid` and `qid`. 
* Example: 

```
{
  "responses": [
    {
      "qid": 4,
      "rid": 1,
      "text": "Facebook"
    },
    {
      "qid": 4,
      "rid": 2,
      "text": "Word of mouth"
    }
  ]
}
```

#### DELETE /api/responses
* Deletes a response by rid
* Input parameters: JSON body with defined `rid` value. 
* Response: Success

#### GET /api/responses/rid/\<RID>
* Returns the Response associated with an rid
* Input parameters: RID defined in the URL
* Response: JSON with a Response object
  
#### POST /api/responses/rid/\<RID>
* Updates a Response's text
* Input paramters: RID defined in URL. JSON body with `updated_text` value set to new Response text.
* Response: Success
  
#### DELETE /api/responses/rid/\<RID>
* Delete a Response by rid
* Input parameters: RID defined in the URL.
* Response: Success
  
#### GET /api/responses/qid/\<QID>
* Returns all the Responses associated with a question.
* Input parameters: QID defined in the URL.
* Response: JSON with list of Response objects.

#### POST /api/responses/qid/\<QID>
* Add a Response to a question.
* Input parameters: QID defined in the URL. JSON body with `text` value set to new Response text.
* Response: Success
  
#### GET /api/visitor_response
* Returns all visitor responses in the database.
* Input parameters: None
* Response: JSON with list of rid's associated with a timestamp.

#### POST /api/visitor_response
* Add a visitor's response to a survey question to our database.
* Input parameters: JSON body with `rid` value defined.
* Response: Success
  

