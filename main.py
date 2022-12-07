from flask import Flask, render_template, request
from model import MainPageModel, InfoPageModel
from institute import Institute

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def Home():
    mpModel = MainPageModel()
    institutes = [Institute(item['institute']['value'], 
                            item['instituteName']['value'], 
                            item['cityName']['value']) for item in mpModel.getInstitutes()]
    cities = sorted(set(institute.city for institute in institutes))

    if request.method == "POST":
        form = request.form
        city = form.get("city")
    else:
        city = cities[0]

    # print(city)
    
    filteredInstitutes = mpModel.filterByCity(institutes, city)

    # print(len(institutes))
    return render_template('home.html', institutes=filteredInstitutes, cities = cities, selectedCity = city)

@app.route("/<string:instituteURI>/fullInfo")
def FullInfo(instituteURI):
    ipModel = InfoPageModel()
    instituteFullInfo = ipModel.getFullInfo(instituteURI)
    title = ipModel.getValue(instituteFullInfo, "http://www.w3.org/2000/01/rdf-schema#label", ukLang=True)
    dbpediaURL = instituteURI.replace('dbr:','http://dbpedia.org/resource/')
    return render_template('fullInfo.html', instituteInfo=instituteFullInfo, title=title, dbpediaURL=dbpediaURL)


@app.route("/<string:instituteURI>/shortInfo")
def ShortInfo(instituteURI):
    ipModel = InfoPageModel()
    instituteFullInfo = ipModel.getFullInfo(instituteURI)
    
    name = ipModel.getValue(instituteFullInfo, "http://www.w3.org/2000/01/rdf-schema#label", ukLang=True)
    abstract = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/ontology/abstract", ukLang=True)
    imageLink = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/ontology/thumbnail", type = "uri")
    city = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/property/city")
    city = ipModel.shortenURI(city).replace("_"," ")
    country = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/property/country")
    country = ipModel.shortenURI(country).replace("_"," ")
    motto = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/ontology/motto")
    rector = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/property/rector")
    rector = ipModel.shortenURI(rector).replace("_"," ")
    website = ipModel.getValue(instituteFullInfo, "http://dbpedia.org/property/website", type="uri")

    instituteShortInfo = []
    instituteShortInfo.append({
        'name':name,
        'abstract':abstract,
        'image':imageLink,
        'city':city,
        'country':country,
        'motto':motto,
        'website':website,
        'rector':rector})
    # print(instituteShortInfo)
    dbpediaURL = instituteURI.replace('dbr:','http://dbpedia.org/resource/')
    return render_template('shortInfo.html', instituteInfo=instituteShortInfo[0], dbpediaURL=dbpediaURL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)