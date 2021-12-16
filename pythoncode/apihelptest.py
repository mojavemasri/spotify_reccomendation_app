from apihelper import apihelper
from db_operations import db_operations
from modifyRecord import modifyRecord
dbop = db_operations()
cursor = dbop.getCursor()
connection = dbop.getConnection()
apihelp = apihelper('BQBYkqX6YgiqhgIE_tPoJeUkEE8T6gIOdrWHO8UCcikpJO9aMedKB7zo8hLzYWoRpvkFkWMbRs-kljevQ2I')
#apihelp.extractUserPlaylists('https://open.spotify.com/user/_m_dogg?si=eb7e4f4c86494dd7')
query = '''SELECT trackID FROM track
WHERE NOT trackID in (
SELECT trackID FROM track_ATTRIBUTES
);'''
cursor.execute(query)
queryResults = cursor.fetchall()
print(len(queryResults))
counter = 0
for q in queryResults:
    print(q)
    print(f"i = {counter}")
    counter += 1
    print(q[0])
    modifyRecord.insertAttributes(q[0], apihelp)
    connection.commit()
