from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('https://dbpedia.org/sparql')

class Query:
    def __init__(self, query):
        self.query = query
    
    def execute(self):
        sparql.setQuery(self.query)
        sparql.setReturnFormat(JSON)
        try:           
            return sparql.query().convert()
        except:
            print("Error has occured when tried to get query")
            pass