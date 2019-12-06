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
- Retrieve lat/long from given animal address, and save it to database
- Save rescued animals' pictures in database

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

### Location endpoints

#### GET /api/locations
* Returns all pin locations in the database
* Input parameters: No input parameters
* Response: Json list of pin locations with `city`, `state`, `country`, `visit_date` and a `coodinates` object holding the `latitude` and `longitude`.

#### POST /api/locations
* Adds a new pin location to the database
* Input parameter: Json body with `lat` and `long` variables.
* Response: `success` response and `city`, `state`, `country`, `city_count`, `state_count`, and `country_count`. The `_count` attributes refer to the total number of pins also belonging to the newly selected city/state/country (for display purposes).

#### GET /api/locations/counts
* Returns count information about total and unique visitors.
* Input parameters: No input params
* Response: Json object with `success`, `total_visitors`, `unique_states`, and `unique_countries`. The `_unique` variables are used to display graphs and totals on the home display.

#### GET /api/locations/\<city_name>
* Returns json list of pin locations with the <city_name> `city` field.
* Response: Json list of pin locations with `city`, `state`, `country`, `visit_date` and a `coodinates` object holding the `latitude` and `longitude`.


#### GET /api/locations/\<state_name>
* Returns json list of pin locations with the <state_name> `state` field.
* Response: Json list of pin locations with `city`, `state`, `country`, `visit_date` and a `coodinates` object holding the `latitude` and `longitude`.


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

#### GET /api/options
* Returns all options associated with questions in the database. 
* NOTE: Refers to multiple choice options presented to the user, not responses submitted by the user.
* Input parameters: None 
* Response: JSON with list of Options, each associated with an `oid` and `qid`. 
* Example: 

```
{
  "options": [
    {
      "qid": 4,
      "oid": 1,
      "text": "Facebook"
    },
    {
      "qid": 4,
      "oid": 2,
      "text": "Word of mouth"
    }
  ]
}
```

#### DELETE /api/options
* Deletes an existing option by oid
* Input parameters: JSON body with defined `oid` value. 
* Response: Success

#### GET /api/options/oid/\<OID>
* Returns the Options associated with an oid
* Input parameters: OID defined in the URL
* Response: JSON with an Option object
  
#### POST /api/options/oid/\<OID>
* Updates an Option's text
* Input paramters: OID defined in URL. JSON body with `updated_text` value set to new Option text.
* Response: Success
  
#### DELETE /api/options/oid/\<OID>
* Delete an Option by oid
* Input parameters: OID defined in the URL.
* Response: Success
  
#### GET /api/options/qid/\<OID>
* Returns all the Options associated with a question.
* Input parameters: QID defined in the URL.
* Response: JSON with list of Option objects.

#### POST /api/options/qid/\<QID>
* Add a multiple choice Option to a question.
* Input parameters: QID defined in the URL. JSON body with `text` value set to new Option text.
* Response: Success
  
#### GET /api/visitor_response
* Returns all visitor responses in the database.
* Input parameters: None
* Response: JSON with list of oid's associated with a timestamp.

#### POST /api/visitor_response
* Add a visitor's response to a survey question to our database.
* Input parameters: JSON body with `oid` value defined.
* Response: Success
  
#### POST /api/animal_locations/address
* Adds information about an animal that has been rescued and placed
* This is used if the exact latitude and longitude of the location is unknown, only know the address of placement
* Input parameters: JSON body with required parameters: 'animal_name', 'address', 'location_name', optional parameters: 'placement_year', 'animal_type', 'animal_notes', 'animal_images'
* Response: Success along with JSON of added fields

```
{
  "animal_name": "Nick",
  "address": "2300 Steele St, Denver, CO 80205",
  "animal_notes": "Now an adult male, has fathered pups",
  "animal_type": "Sea lion",
  "location_name": "Denver Zoo",
  "placement_year": 2006,
  "animal_images": "PMMC_images/nick_by_wl.jpg2.jpg"
}
```

#### GET /api/animal_locations/address
* Retrieves information about the placed animal
* Input parameters: None
* Response: JSON list of 'latitude', 'longitude', 'animal_name', 'location_name', 'placement_year', 'animal_type', 'animal_notes', 'animal_images'

```
{
  "animal_location": [
    {
      "animal_name": "Nick",
      "animal_notes": "Now an adult male, has fathered pups",
      "animal_type": "Sea lion",
      "latitude": 39.75118,
      "longitude": -104.948906,
      "location_name": "Denver Zoo",
      "placement_year": 2006,
      "animal_images": "PMMC_images/nick_by_wl.jpg2.jpg"
    },
    {
      "animal_name": "Sage",
      "animal_notes": ",
      "animal_type": "Sea lion",
      "latitude": 30.422618,
      "longitude": -89.025583,
      "location_name": "Institute for Marine Mammal Studies in Louisiana",
      "placement_year": 2013
    }
  ]
}
```

#### POST /api/animal_locations
* Adds information about an animal that has been rescued and placed
* This is used if the exact latitude and longitude of the location is known
* Input parameters: JSON body with required parameters: 'animal_name', 'lat', 'long', 'location_name', optional parameters: 'placement_year', 'animal_type', 'animal_notes', 'animal_images'
* Response: Success along with JSON of added fields

```
{
  "animal_name": "Nick",
  "lat": 39.75118,
  "long": -104.948906,
  "animal_notes": "Now an adult male, has fathered pups",
  "animal_type": "Sea lion",
  "location_name": "Denver Zoo",
  "placement_year": 2006,
  "animal_images": "PMMC_images/nick_by_wl.jpg2.jpg"
}
```

#### GET /api/animal_locations
* Retrieves the information about the placed animal
* Input parameters: None
* Response: JSON list of 'latitude', 'longitude', 'animal_name', 'address', 'location_name', 'placement_year', 'animal_type', 'animal_notes', 'animal_images'

#### GET /api/animal_locations/lat_long
```
/api/animal_locations/lat_long?latitude=39.75118&longitude=-104.948906
```
* Retrieves inforamtion about the placed animal at the given latitude and longitude
* Input parameters: None
* Response: JSON list of 'latitude', 'longitude', 'animal_name', 'address', 'location_name', 'placement_year', 'animal_type', 'animal_notes', 'animal_images'

#### POST /admin/email
* Sends email with survey, visitor, and donation information in CSV files
* Input parameters: Json body with `email_address` defined
* Response: `success` response

#### GET /admin/count
* Returns count objects in database (right now, only using this table to store the "rescues" count.
* Input params: None
* Response: Json list of `counts`, each `count` having a string `name` and integer `total`.

#### POST /admin/count
* Adds *new* count to the count table
* Input params: Json body with string `name` and init integer `total` fields
* Response: `success` response

#### POST /admin/count/\<name>
* Updates the count of an existing field (used to update rescue count on display)
* Input params: the \<name> variable in url, json body with `new_total` integer field
* Response: `success`

#### GET /api/donation_redirect
* Redirects the user to the PayPal donation page while saving a running count and timestamp to the database
* Input params: None
* Response: None (user is redirected)

#### GET /api/donation_visits
* Returns the donation visit information saved during redirection
* Input params: None
* Response: List of `donation_visits`, each with an `id` and `timestamp`

#### GET /api/snap/location
* Removes half of the database entries in the Location table
* Input params: None
* Response: `success`
  


