
import xml.etree.cElementTree as ET
import pprint
import re

def get_user(element):
    return

def process_map(filename):
    users = set()
    for event, element in ET.iterparse(filename):

        if element.tag == "relation" or element.tag == "node" or element.tag == "way":
            if "uid" in element.keys():
                if element.attrib['uid'] not in users:
                    users.add(element.attrib['uid'])

    return users


def test():

    users = process_map('bath.osm')
    pprint.pprint(len(users))



if __name__ == "__main__":
    test()
