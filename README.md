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

