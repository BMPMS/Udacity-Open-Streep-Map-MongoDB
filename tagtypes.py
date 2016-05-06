
import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            if lower.search(tag.attrib['k']) is not None :

                keys["lower"] = keys["lower"] + 1
            elif lower_colon.search(tag.attrib['k']) is not None:
                keys["lower_colon"] = keys["lower_colon"] + 1
            elif problemchars.search(tag.attrib['k']) is not None:
                keys["problemchars"] = keys["problemchars"] + 1
                print ('Problem Char',tag.attrib['k'])
            else:
                keys["other"] = keys["other"] + 1
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    keys = process_map('bath.osm.json')
    pprint.pprint(keys)



if __name__ == "__main__":
    test()
