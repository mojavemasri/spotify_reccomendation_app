from db_operations import db_operations
dbop = db_operations()
cursor = dbop.getCursor()
connection = dbop.getConnection()
query = '''
Select * from track where trackPopularity < 40 ;
'''
cursor.execute(query)
line = cursor.fetchone()[0]
while line:
    line = cursor.fetchone()

playlist = '7DzlwPsVvIYcvkGwC1CcNY'
query = f'''Select Count(*) from playlist
          WHERE playlistID = \'{playlist}\';'''
cursor.execute(query)
count = cursor.fetchone()
print(count)
