from app import app
from flask_cors import CORS

if __name__=="__main__":
    CORS(app, support_credentials=True)
    app.run(debug=True)#, host='0.0.0.0', port=5000)
