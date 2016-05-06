
#fetching my database.  This has been imported using the following statement in the terminal
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


db = get_db('examples')


#print some summary data.
print('Number of Tags:', db.bath.find().count())
print('Number of Nodes:', db.bath.find({"type":"node"}).count())
print('Number of Ways:', db.bath.find({"type":"way"}).count())


unqusers = db.bath.aggregate([
                     { "$group": { "_id": "$created.user", "count": { "$sum": 1} } },
                     { "$sort": { "count": -1 } }
                   ])
for u in unqusers:
    print(u)

print("Unique Users:",len(list(unqusers)))


#check out amenities
amen = db.bath.distinct("amenity")
amen.sort()
for a in amen:
    print(a)

#find non-meaningful amenities
amenyes = db.bath.find({"amenity":"yes"})
for a in amenyes:
    print(a)
amenlau = db.bath.find({"amenity":"lau"})
for a in amenlau:
    print(a)

#look at cities
city = db.bath.distinct("address.city")
city.sort()
for c in city:
    print(c)

#dig deeper into addresses without cities or postcodes
print('Addresses with a City',db.bath.find({"address.city": {"$exists" : 1}}).count())
print('Addresses with no City',db.bath.find({"address": {"$exists" : 1},"address.city": {"$exists" : 0}}).count())
print('Addresses with no Postcode',db.bath.find({"address": {"$exists" : 1},"address.postcode": {"$exists" : 0}}).count())
print('Addresses with no City and no Postcode',db.bath.find({"node_refs":{"$exists" : 0},"pos":{"$exists" : 0},"address": {"$exists" : 1},"address.city": {"$exists" : 0},"address.postcode": {"$exists" : 0}}).count())

#checking for non-positional and non-created nodes...
print('Addresses with no Node Refs or Position or Created',db.bath.find({"node_refs":{"$exists" : 0},"pos":{"$exists" : 0},"created": {"$exists" : 0}}).count())

#what about fix me's?
fixes = db.bath.distinct("FIXME")
for f in fixes:
    print(f)
print(db.bath.find({"FIXME":{"$exists":1}}).count())
