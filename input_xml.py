#!/usr/bin/python

import os
import sys
import cgi
import xml.etree
import hashlib 
import Cookie
import cgitb; cgitb.enable()

from sys import stdout, stderr
from xml.etree import ElementTree as et

def draw_node(step, name, lines):
    if str(0) == step: 
        lines.append("".join(["<br /><p>step:", step, "<p align = 'center'>[name:", name,"]</p></p>"])) 
    else:
        lines.append("".join(["<br /><p align = 'center'>|</p><p>step:", step, "<p align = 'center'>[name:", name,"]</p></p>"])) 

def draw_lines(level, lines):
    print level
    for each_level in level.values():
        if 1 != each_level:
            lines[each_level + 1] = "<p>/\\</p><br />" 
        else:
            lines[each_level + 1] = "<p>|</p><br />"

    #for each_level in level.values():
    #    if 1 != each_level:
    #        print """
    #            <p>/\\</p>
    #            <br />
    #        """
    #    else: print """
    #        <p>|</p>
    #        <br />
    #    """

def parse_xml(fp, f_name):
    if fp:
        et_instance = et.ElementTree()
        e = et_instance.parse(fp)
        level = {}; lines = [] 
        for item in e.findall("node"):
            #draw_node(item.attrib["step"], item.attrib["name"], lines)     
            if level.has_key(int(item.attrib["step"])): level[int(item.attrib["step"])] += 1
            else: level[int(item.attrib["step"])] = 1
        #draw_lines(level, lines) 

        #for item, c in zip(e.findall("node"), range(len(level))):
        #    if 1 == level[c]:
        #        draw_node(item.attrib["step"], item.attrib["name"], lines)
        #    else:
        #        lines.append("".join(["<br /><p>step:", item.attrib["step"], "<p align = 'center'>"]))  
        #        while(level[c] > 0):
        #            lines.append("".join(["[name:",item.attrib["name"],"]"])) 
        #            level[c] -= 1
        #        lines.append("</p></p>")

        e_arr = e.findall("node"); count = 0
        for c in range(len(level)):
            if 1 == level[c]: 
                draw_node(e_arr[count].attrib["step"], e_arr[count].attrib["name"], lines)
                count += 1
            else:
                lines.append("".join(["<p align = 'center'>/\\</p>"]))
                lines.append("".join(["<br /><p>step:", e_arr[count].attrib["step"], "<p align = 'center'>"]))  
                while(level[c] > 0):
                    lines.append("".join(["[name:", e_arr[count].attrib["name"],"]"])) 
                    level[c] -= 1
                    count += 1
                lines.append("</p></p>")
        
        f_name = f_name.split(".")[0] + ".html"
        fp = file(os.path.join("/tmp/", f_name), "w") 
        fp.writelines(lines)
        fp.close()
    else:
        print >> stderr, "xml descrption file could not be imported\n"

def get_form_data():
    upload_dir = "/tmp"
    form = cgi.FieldStorage()
    f_item = form["file_name"]

    #f_store = file(os.path.join(upload_dir, hashlib.md5(f_item.value).digest()), "wb")
    f_store = file(os.path.join(upload_dir, f_item.filename), "wb")
    f_store.write(f_item.file.read())
    f_store.close()
    fp = file(os.path.join(upload_dir, f_item.filename), "r")
    parse_xml(fp, os.path.join(upload_dir, f_item.filename))
    fp.close()
    return os.path.join(upload_dir, f_item.filename)

if "__main__" == __name__:
    xml_name = get_form_data()
    co = Cookie.SimpleCookie()
    co["xml_name"] = xml_name 
    print co
    print "Content-type: text/html\n"
    print "<html><body>"
#DEBUG
#    print "Cookie data: " + os.environ.get("HTTP_COOKIE")
    print "<p>xml description file uploaded</p>"
    print "<a href = '/cgi-bin/show_graph.py'>graph</a>"
    print "</body></html>"
