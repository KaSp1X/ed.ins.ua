from flask import Flask, render_template
from model import MainPageModel
from institute import Institute

app = Flask(__name__)

@app.route("/")
def Home():
    mpModel = MainPageModel()
    institutes = [Institute(item['institute']['value'], 
                            item['instituteName']['value'], 
                            item['cityName']['value']) for item in mpModel.getInstitutes()]
    # print(len(institutes))
    return render_template('home.html', institutes=institutes)

@app.route("/<string:instituteURI>")
def FullInfo(instituteURI):
    institute = Institute(instituteURI)
    return render_template('fullInfo.html', institute=institute)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)