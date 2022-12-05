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

class FullInfoPageModel:
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

    def getName(self, JSONObject):
        name = ""
        not_found = True
        for item in JSONObject:
            if item['predicate']['value'] == "http://www.w3.org/2000/01/rdf-schema#label":
                for object in item['object']:
                    if (object['type'] == 'literal' and object['xml:lang'] == "uk"):
                        not_found = False
                        name = object["value"]
                        break
            if not_found == False:
                break
        print(name)
        return name

    def getFullInfo(self, URI):
        query = Query(f'''
        SELECT ?predicate ?object
        WHERE {{ {URI} ?predicate ?object. }}''')
        result = self.groupByPredicate(query.execute()['results']['bindings'])
        # print(result)
        return result
