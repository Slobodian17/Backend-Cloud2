from flask import Flask
from flask_bcrypt import Bcrypt
from waitress import serve
from total.blueprint import api_blueprint
import pymysql
from flask_cors import CORS

pymysql.install_as_MySQLdb()

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/users": {"origins": "http://127.0.0.1:5000"}})
# CORS(app, resources={r"*": {"origins": "*"}})

bycrypted_app = Bcrypt(app)
app.register_blueprint(api_blueprint, url_prefix="")
app.config.update({"TESTING": True})

# CORS(app, resources={r"": {"origins": "*"}})
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# curl -v app.run(host='0.0.0.0', port=5000)-XGET http://localhost:5000/api/v1/hello-world-10
