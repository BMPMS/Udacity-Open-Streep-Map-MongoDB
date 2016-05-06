
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
Wrangling the Data into following format as per OSM project:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
for amenities..
{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}
Way nodes should be turned into.
"node_refs": ["305896090", "1719825889"]
"""



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    created = {}
    address = {}
    pos = []
    noderefs = []
    others = {}
    if element.tag == "node" or element.tag == "way" :
        for tag in element.iter():
            for c in CREATED:
                if c in element.keys():
                    created[c] = element.attrib[c]
            if "lon" in element.keys() and "lat" in element.keys():
                if len(pos) < 2:
                    pos.append(float(element.attrib['lat']))
                    pos.append(float(element.attrib['lon']))
            for child in element:
                if element.tag == "way":
                    if child.tag == "nd":
                        if child.attrib['ref'] not in noderefs:
                            noderefs.append(child.attrib['ref'])
                try:
                    chars = problemchars.search(tag.attrib['k'])
                    add = tag.attrib['k'].split(":")
                    if len(add) < 3 and len(add) > 0:
                        if add[0][0:4] == "addr":
                            address[add[1]] = tag.attrib['v']
                        else:
                            others[add[0]] = tag.attrib['v']
                except:
                    pass
            try:
                node['id'] = tag.attrib['id']
                node['visible'] = tag.attrib['visible']
            except:
                pass
            node['type'] = element.tag
            if len(created) > 0:
                node['created'] = created
            if len(address) > 0:
                node['address'] = address
            if len(noderefs) > 0:
                node['node_refs'] = noderefs
            if len(pos) > 0:
                node['pos'] = pos
            for o in others:
                node[o] = others[o]
        return node
    else:
        return None


def process_map(file_in, pretty = False):

    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():

    data = process_map('bath.osm', False)

test()
