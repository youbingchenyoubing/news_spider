import db_connection


connection_obj = db_connection.MongoDBConnection('user')

collection = connection_obj.dbConnection()

if collection:
    print "hello word"
else:
    print "error"