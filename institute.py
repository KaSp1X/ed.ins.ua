from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

class Institute:
    def __init__(self, URI):
        self.URI = URI
        self.graph = self.getGraphAsSubject()

    def getGraphAsSubject(self):
        query = f'''
        SELECT ?predicate ?object
        WHERE {{ {self.URI} ?predicate ?object. }}'''
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:           
            return sparql.query().convert()
        except:
            print("Error has occured when tried to get query")
            pass

    def getRelations(self):
        if self.graph is None:  
            return ""
        return self.graph['results']['bindings']