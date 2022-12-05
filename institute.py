from query import Query
class Institute:
    def __init__(self, URI, name = None, city = None):
        self.URI = URI
        self.name = name
        self.city = city
        self.graph = None

    def getGraphAsSubject(self):
        query = Query(f'''
        SELECT ?predicate ?object
        WHERE {{ {self.URI} ?predicate ?object. }}''')
        return query.execute() 

    def getRelations(self):
        if self.graph is None:  
            self.graph = self.getGraphAsSubject()
        return self.graph['results']['bindings']