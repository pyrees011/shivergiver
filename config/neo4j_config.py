from neo4j import GraphDatabase

class Neo4jConfig:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    def close(self):
        self.driver.close()

    def query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result
        
    def check_connection(self):
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        

neo4j_config = Neo4jConfig()