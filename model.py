from query import Query

class MainPageModel:
    def __init__(self) -> None:
        pass

    def get_institutes(self):
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
        return query.execute()
