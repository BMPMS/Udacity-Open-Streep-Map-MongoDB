import re

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

#fetcht the database
db = get_db('examples')

#mapping lists for various updates

mapping = { "Crescent,": "Crescent",
            "Cresent": "Crescent",
            "HIll": "Hill",
            "Rd": "Road",
            "St": "Street",
            "avenue": "Avenue",
            "hill":"Hill",
            "kingsway":"Kingsway",
            "lane":"Lane",
            "road":"Road",
            "st":"Street"
            }

Pmapping = { "Bs": "BS",
            "Cf": "CF",
            "bs": "BS",
            "cf": "CF",
            "ta": "TA"
            }

Amapping = {"Convalescent Centre":"convalescent_centre",
            "Dental Hospital":"dental_hospital",
            "Health Centre":"health_centre",
            "Manège":"manège",
            "Pool": "pool",
            "Pool Hall": "pool_hall",
            "Showroom":"showroom",
            "Triangle Walk":"triangle_walk",
            "Truck Service Iveco":"truck_service_iveco",
            "University":"university"
}

Cmapping = {"BRIDGEND": "Bridgend",
            "PONTYCLUN": "Pontyclun",
            "PONTYPRIDD": "Pontypridd",
            "Brisol" :"Bristol",
            "Trefforest" :"Treforest",
            "Burnham-on-Sea" : "Burnham on Sea",
            "Weston-Super-Mare": "Weston super Mare",
            "Weston-super-Mare": "Weston super Mare"
}

#systematically going through the variables on the Data Cleaning Plan

def update_postcode():

    for items in Pmapping:
        old = ""
        new = ""
        regstr = "^" + items
        regx = re.compile(regstr)
        plist = list(db.bath.find({"address.postcode":regx}))
        for p in plist:
            old = p['address']['postcode']
            new = Pmapping[items] + old[2:]
            db.bath.update({"address.postcode":old},{"$set":{"address.postcode":new}})
            print('updating')

def update_address():

    for items in mapping:
        old = ""
        new = ""
        regstr = "\s" + items + "$"
        regx = re.compile(regstr)
        plist = list(db.bath.find({"address.street":regx}))
        for p in plist:
            old = p['address']['street']
            mylen = len(old) - len(items) - 1
            new = old[:mylen] + " " + mapping[items]
            db.bath.update({"address.street":old},{"$set":{"address.street":new}})
            print('updating',old, " -> ", new)

update_postcode()
update_address()
db.bath.update({"id":"3072293702"},{"$set":{"amenity":"water_bus_stop"}})
db.bath.update({"id":"3836219527"},{"$set":{"amenity":"hairdresser"}})
db.bath.remove({"id":"580823638"})
print(list(db.bath.find({"amenity":"lau"})))

def update_amenity():

    for items in Amapping:
        old = items
        new = Amapping[items]
        db.bath.update({"amenity":old},{"$set":{"amenity":new}})
        print(list(db.bath.find({"amenity":old})))

update_amenity()
db.bath.remove({"FIXME":{"$exists":1}})
print(db.bath.find({"FIXME":{"$exists":1}}).count())



def update_city():


    regstr = ",\s.+$"
    regx = re.compile(regstr)
    plist = list(db.bath.find({"address.city":regx}))
    for p in plist:
        old = p['address']['city']

        str = re.search(',\s.+$',old).group(0)
        mylen = len(old) - len(str)
        new = old[:mylen]
        db.bath.update({"address.city":old},{"$set":{"address.city":new}})
        print('updating',old, " -> ",new)

    for items in Cmapping:
        old = items
        new = Cmapping[items]
        print(old,";",new)
        db.bath.update({"address.city":old},{"$set":{"address.city":new}})
        print(list(db.bath.find({"address.city":old})))

#for some reason (spaces?) the update function was not working for these 2 cities
#after a while investigating I went the long way round
#good to practice a different way of updating!

weston = db.bath.find({"address.city":"Weston-super-Mare"})
for w in weston:
    w['address']['city'] = "Weston super Mare"
    db.bath.save(w)

pont = db.bath.find({"address.city":"PONTYCLUN"})
for p in pont:
    p['address']['city'] = "Pontyclun"
    db.bath.save(p)

update_city()
