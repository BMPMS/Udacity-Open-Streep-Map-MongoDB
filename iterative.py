#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
From Case Study -  use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.

"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tagdict = {}
    for event,elems in ET.iterparse(filename):
        if elems.tag not in tagdict:
            tagdict[elems.tag] = 1
        else:
            tagdict[elems.tag] = tagdict[elems.tag] + 1
    return tagdict

def test():

    tags = count_tags('bath-json.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}



if __name__ == "__main__":
    test()
