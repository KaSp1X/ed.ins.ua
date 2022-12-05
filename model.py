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

    def getValue(self, JSONObject, predicate, type = "literal", ukLang = False):
        value = ""
        for item in JSONObject:
            if item['predicate']['value'] == predicate:
                for object in item['object']:
                    if (object['type'] == type):
                        if (ukLang == True and object['xml:lang'] == "uk") or (ukLang == False):
                            value = object["value"]
                            break
                break
        # print(value)
        return value

    def getFullInfo(self, URI):
        query = Query(f'''
        SELECT ?predicate ?object
        WHERE {{ {URI} ?predicate ?object. }}''')
        result = self.groupByPredicate(query.execute()['results']['bindings'])
        # print(result)
        return result
