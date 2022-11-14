from flask import Flask
from institute import *

app = Flask(__name__)

@app.route("/")
def Home():
    return ""

@app.route("/<string:instituteURI>/")
def FullInfo(instituteURI):
    s = Institute(instituteURI)
    return str(s.getRelations())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)