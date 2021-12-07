from db_operations import db_operations
dbop = db_operations()
query = '''
Select * from track where trackPopularity < 40 ;
'''
print(dbop.fetchRow(query))
