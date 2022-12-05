from flask import Flask, render_template
from model import MainPageModel, FullInfoPageModel
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

@app.route("/institute/<string:instituteURI>")
def FullInfo(instituteURI):
    fipModel = FullInfoPageModel()
    instituteInfo = fipModel.getFullInfo(instituteURI)
    title = fipModel.getName(instituteInfo)
    return render_template('fullInfo.html', instituteInfo=instituteInfo, title=title)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)