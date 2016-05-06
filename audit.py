#this code is adapted from the Udacity exercise.

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "bath.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcode_type_re = re.compile(r'[a-z][a-z]', re.IGNORECASE)


expected = ["South","West","East","North","Way","Walk","View","Terrace","Row","Rise","Parade","Park","Mead","Mews","Hill","Green","Grove","Gate","Gardens","Estate","Cottages","Crescent","Close","Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail","Buildings", "Parkway", "Broadway","Kingsway","Queensway","Commons"]

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


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_postcode(postcode_types, postcode_name):
    p = postcode_type_re.search(postcode_name)
    if p:
        postcode_type = p.group()
        postcode_types[postcode_type].add(postcode_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postcode(tag):
                    audit_postcode(postcode_types, tag.attrib['v'])
    osm_file.close()
    return street_types,postcode_types


def update_name(st_types):

    for st_type, ways in st_types.items():
        for name in ways:
            if name =="caerphilly_road":
                name = "Caerphilly Road"
            elif name != "Hillcrest" and name!= "Quadeast":
                for items in mapping:
                    strlen = len(items)
                    old = name[len(name)-strlen:len(name)]
                    if old == items:
                        better_name = name[0:len(name)-strlen] + mapping[items]
                        print (name, "=>", better_name)

def update_postcode(pt_types):

    for pt_type, ways in pt_types.items():
        for name in ways:
            for items in Pmapping:
                if name[0:2] == items[0:2]:
                    better_postcode = Pmapping[items] + name[2:len(name)]
                    print (name, "=>", better_postcode)


def test():
    st_types,pt_types = audit(OSMFILE)
    pprint.pprint(dict(pt_types))
    update_name(st_types)
    update_postcode(pt_types)


if __name__ == '__main__':
    test()
