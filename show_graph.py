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

if "__main__" == __name__:
    #fp = file("/tmp/graph.html", "r")
    co = Cookie.SimpleCookie()
    co_str = os.environ.get("HTTP_COOKIE")
    html_name = ""
    if co_str:
        co.load(co_str)
        xml_name = str(co["xml_name"].value)
        html_name = xml_name.split(".")[0] + ".html"
#DEBUG:
    print "".join(["<p>Cookie data:", html_name, "</p>"])
    fp = file(os.path.join("/tmp/", html_name), "r")
    print "Content-type: text/html\n"
    print "<html><body>"
    print fp.read()
    print "<a href = '/cgi-bin/generate_procedure.py'>generate procedure</a>"
    print "</body></html>"
    fp.close()
