from query import Query
class Institute:
    def __init__(self, URI):
        self.URI = URI
        self.graph = self.getGraphAsSubject()

    def __init__(self, URI, name, city):
        self.URI = URI
        self.name = name
        self.city = city

    def getGraphAsSubject(self):
        query = Query(f'''
        SELECT ?predicate ?object
        WHERE {{ {self.URI} ?predicate ?object. }}''')
        return query.execute() 

    def getRelations(self):
        if self.graph is None:  
            self.graph = self.getGraphAsSubject()
        return self.graph['results']['bindings']