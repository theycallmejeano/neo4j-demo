from neo4j import GraphDatabase

# Connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo4j"

# driver for neo4j connection
driver = GraphDatabase.driver(uri, auth=(username, password))

#####################################
#              DATA INSERTS
####################################

# We can define a cypher query which contains the nodes in the social network

cypher_query = """
// Person nodes
CREATE (p1:Person {name: 'Alpha', role: 'Amplifier'})
CREATE (p2:Person {name: 'Bravo', role: 'Amplifier'})
CREATE (p3:Person {name: 'Charlie', role: 'Amplifier'})
CREATE (p4:Person {name: 'Delta', role: 'Creator'})
CREATE (p5:Person {name: 'Echo', role: 'Unsuspecting'})

// Social Media Account nodes
CREATE (a1:SocialMediaAccount {username: '@alpha_influencer', platform: 'Twitter'})
CREATE (a2:SocialMediaAccount {username: '@bravo_follower', platform: 'Twitter'})
CREATE (a3:SocialMediaAccount {username: '@charlie_journalist', platform: 'Twitter'})
CREATE (a4:SocialMediaAccount {username: '@delta_fake', platform: 'Twitter'})
CREATE (a5:SocialMediaAccount {username: '@echo_innocent', platform: 'Twitter'})

// Content nodes (e.g., Posts)
CREATE (c1:Content {type: 'Post', content: '2+2 equals 5', date: '2025-03-22'})
CREATE (c2:Content {type: 'Post', content: '4 is a prime number', date: '2025-03-22'})

//  Relationships between people and accounts
CREATE (p1)-[:HAS_ACCOUNT]->(a1)
CREATE (p2)-[:HAS_ACCOUNT]->(a2)
CREATE (p3)-[:HAS_ACCOUNT]->(a3)
CREATE (p4)-[:HAS_ACCOUNT]->(a4)

// Create Relationships between social media accounts and content
CREATE (a4)-[:SPREADS]->(c1)
CREATE (a4)-[:SPREADS]->(c2)

// Create spreading relationships (Disinformation spreading)
CREATE (a1)-[:AMPLIFIES]->(c1)
CREATE (a2)-[:AMPLIFIES]->(c1)
CREATE (a3)-[:AMPLIFIES]->(c1)
CREATE (a5)-[:AMPLIFIES]->(c1)
CREATE (a1)-[:AMPLIFIES]->(c2)
CREATE (a2)-[:AMPLIFIES]->(c2)

"""

# General function to run cypher queries
def execute_cypher_query(driver, query):
    try:
        with driver.session() as session:
            session.run(query)
    except Exception as ex:
        print(f"Error occured: {ex}")
        raise

# run the query to insert the data
execute_cypher_query(driver, cypher_query)

print("Data has been inserted into Neo4j!")


# query disinfo data
disinfo_spreader_query = """
   MATCH (a:SocialMediaAccount)-[r:SPREADS|AMPLIFIES]->(c:Content)
   RETURN a, r, c
    """

# general function
def get_neo4j_data(driver, query):
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]
    except Exception as ex:
        print(f"Error occured {ex}")
        raise


# get data on disinfo
print(get_neo4j_data(driver, disinfo_spreader_query))

# close the Neo4j driver
#driver.close()