#!/usr/bin/python

import os
import sys
import cgi
import xml.etree
import random
import Cookie
import cgitb; cgitb.enable()

from sys import stdout, stderr
from xml.etree import ElementTree as et

def get_max(level):
    if not level: return 0
    res = level[0]
    for l in level:
        if res < level[l]: res = level[l] 
    return res

def check_break(level):
    if not level: return True
    for l in level:
        if 0 != level[l]:
            return False
    return True

def get_step_nodes(step, e_arr):
    res = []
    for e in e_arr:
        if step == int(e.attrib["step"]): res.append(e)
    return res

def form_graph(fp):
    if not fp: return
    et_instance = et.ElementTree()
    e = et_instance.parse(fp)
    level = {}; lines = [] 
    e_arr = e.findall("node"); count = 0; graph = {} 
    for item in e_arr: 
        if level.has_key(int(item.attrib["step"])): level[int(item.attrib["step"])] += 1
        else: level[int(item.attrib["step"])] = 1

#DEBUG:
#    print e_arr
#    print level
    limit = get_max(level)
    steps = len(level)

    while(count < steps):
        step_arr = get_step_nodes(count, e_arr)
        li = len(step_arr)
        while(li < limit):
            if len(step_arr):step_arr.append(step_arr[li % len(step_arr)])             
            li += 1
        graph[count] = step_arr
        count += 1
    return graph

#FIXME:
#   mind is not clear, matrix is fine, but output wrong routines
    #while count <= limit:
    #    arr_index = 0
    #    graph[count] = []
    #    for l in level:
    #        if 1 == level[l]: 
    #            graph[count].append(e_arr[arr_index])
    #            arr_index += 1
    #        elif limit != level[l]:
    #            if count > level[l]:
    #                rand_seed = random.seed
    #                rand_index = arr_index + rand_seed.im_self.randint(0, level[l] - 1)
    #                graph[count].append(e_arr[rand_index]) 
    #                arr_index += level[l]
    #        elif limit == level[l]:
    #            arr_index += count
    #            graph[count].append(e_arr[arr_index])
    #    count += 1 
#DEBUG
#    print graph

def generate_procedure(xml_name):
    fp = file(xml_name, "r")
    graph = form_graph(fp)
    fp.close()
    return graph
    
if "__main__" == __name__:
    print "Content-type: text/html\n"
    co = Cookie.SimpleCookie()
    co_str = os.environ.get("HTTP_COOKIE")
    xml_name = ""
    if co_str:
        co.load(co_str)
        xml_name = str(co["xml_name"].value)
#DEBUG:
#    print "Cookie data:" + xml_name
    graph = generate_procedure(xml_name) 
    for l in range(len(graph[0])):
        print "".join(["<p>Senario ", str(l), ":"])
        for g in graph:
            step_name = graph[g][l].attrib["name"]
            if step_name == "end": print step_name 
            else: print step_name + "  ->  "
            #print "".join([graph[g][l].attrib["name"], " -> "])
        print "</p>"
    print "<a href = '/paper/input_xml.html'>return back</a>"

