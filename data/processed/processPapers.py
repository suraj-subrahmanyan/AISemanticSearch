import xml.etree.ElementTree as ET
import json
import jsonlines

#Extracting these data tags:
# <id></id>
# <published></published>
# <summary></summary>
# <author><author> 
# <link></link>

#Parse through XML, Loop Through Each Paper, Extract and Map Fields, Create Json Object, Write to Jsonl

xml_files = ["AI_papers.xml", "CL_papers.xml", "CV_papers.xml", "IR_papers.xml", "LG_papers.xml"]
data_tags = ["id", "published", "summary", "link"]

namespace = '{http://www.w3.org/2005/Atom}'

adjustement = '../raw/'
entire_data = []

def XML_json(xml_files, data_tags):
    for file in xml_files:
        tree = ET.parse(adjustement + file)

        root = tree.getroot()

        for child in root:
            dict = {}
            for tags in data_tags:
                find_tags = child.find(namespace + tags)
                if (find_tags != None):
                    if (tags == 'link'):
                        dict[tags] = find_tags.attrib['href']
                    else:
                        dict[tags] = find_tags.text
            #logic must be different as name is within author element
            find_author = child.findall(namespace + 'author')
            names = []
            if (find_author != None):
                for children in find_author:
                    find_name = children.find(namespace + 'name')
                    if (find_name != None):
                        names.append(find_name.text)
            if names:
                dict['author'] = names

            if dict:
                entire_data.append(dict)

if __name__ == '__main__':
    XML_json(xml_files, data_tags)
    with jsonlines.open('processed_papers.jsonl', 'w') as w:
        w.write_all(entire_data)

