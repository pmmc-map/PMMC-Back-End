from app import app
from flask_cors import CORS

if __name__=="__main__":
    CORS(app, support_credentials=True, resources={r"*": {"origins": "*"}})
    app.run(debug=True, host="0.0.0.0", port=80)#, ssl_context='adhoc')#, ssl_context=('cert.pem', 'key.pem'))

