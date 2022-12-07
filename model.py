from query import Query

class MainPageModel:
    def getInstitutes(self):
        query = Query(f''' 
            SELECT ?institute (SAMPLE(?instName) AS ?instituteName) (SAMPLE(?cName) AS ?cityName)
            WHERE
            {{
                ?institute dbo:country dbr:Ukraine;
                            rdf:type ?type;
                            rdfs:label ?instName;
                            dbo:city ?c.

                ?c rdf:type dbo:City;
                    dbo:country dbr:Ukraine;
                    foaf:name ?cName.

                FILTER(langmatches(lang(?instName), "uk"))
                FILTER(?type IN (dbo:University, dbr:National_academy, dbr:Institute)) 
            }}
            GROUP BY ?institute
        ''')
        result = query.execute()['results']['bindings']
        return result
    
    def filterByCity(self, institutes, city):
        new_institutes = []
        for institute in institutes:
            if institute.city == city:
                new_institutes.append(institute)
        return new_institutes

class InfoPageModel:
    def groupByPredicate(self, JSONobject):
        new_data = []
        not_found = True
        for item in JSONobject:
            for new_item in new_data:
                not_found = True
                if item['predicate']['value'] == new_item['predicate']['value']:
                    not_found = False
                    new_item['object'].append(item['object'])
                    break
            if not_found:
                new_data.append({'predicate':item['predicate'], 'object':[item['object']]})
        return new_data

    def getValue(self, JSONObject, predicate, type = None, ukLang = False):
        value = ""
        for item in JSONObject:
            if item['predicate']['value'] == predicate:
                for object in item['object']:
                    if (type is not None and object['type'] == type) or (type is None):
                        if (ukLang == True and object.get('xml:lang') == "uk") or (ukLang == False):
                            value = object["value"]
                            break
                break
        # print(value)
        return value

    def shortenURI(self, URI):
        revURI = URI[::-1]
        try:
            revIndex = revURI.index("/")
        except:
            revIndex = 0
        index = len(URI) - revIndex
        return URI[index:]

    def getFullInfo(self, URI):
        query = Query(f'''
        SELECT ?predicate ?object
        WHERE {{ {URI} ?predicate ?object. }}''')
        result = self.groupByPredicate(query.execute()['results']['bindings'])
        # print(result)
        return result
