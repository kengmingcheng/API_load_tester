# import requests
from typing import DefaultDict
from urllib.request import *
import urllib.parse
import threading
import time
import datetime
import copy
import xml.etree.ElementTree as ET
import random

from . import settings, generator

default_json = settings.read_default_json()
default_xml = settings.read_default_xml()

class request_sender(threading.Thread):
    
    def __init__(self, name, config, source, random_list, task = None):
        threading.Thread.__init__(self, name=name)
        self.url = config['url']
        self.loop = config['loop'] if 'loop' in config.keys() else 1
        self.sleep = config['interval'] if 'interval' in config.keys() else 0
        self.type = config['content-type'] if 'content-type' in config.keys() else 'json'
        self.source_name = config['source'] if 'source' in config.keys() else None
        self.source = source
        self.random_list_name = config['random_list'] if 'random_list' in config.keys() else None
        self.random_list = random_list

        self.payload = config['payload']
        self.headers = config['headers']
        self.task = task

        self.json = default_json
        self.xml = default_xml

    def run(self):
        print(self.name + " starting...")
        if self.task == None:
            self.default_task()
        else:
            self.task()
    
    def default_task(self):
        headers  =self.headers_composer()
        body = self.payload_composer()

        request = Request(self.url, data=body, headers=headers, method='POST')
        for i in range(0, self.loop):
            body = self.payload_composer(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
            request = Request(self.url, data=body, headers=headers, method='POST')
            try:
                with urlopen(request) as uo:
                    response = uo.read().decode('utf-8')
                print(self.name + "  " + response)
            except Exception as e:
                print(self.name + "  " + str(e))

            time.sleep(self.sleep)

        print(self.name + " finished...")

    def set_loop(self, loop):
        self.loop = loop
        return self

    def set_sleep(self, sleep):
        self.sleep = sleep
        return self

    def set_json(self, json):
        self.json = json

    def set_xml(self, xml):
        self.xml = xml

    def headers_composer(self):

        headers = copy.deepcopy(self.headers)
        # if self.type == "json":
        #     headers['Content-Type'] = 'application/json'
        # elif self.type == "xml":
        #     headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return headers

    def payload_composer(self, mark = ""):
        if self.type == "json":
            payload = copy.deepcopy(self.json)
            for key, value in self.payload.items():
                elements = []
                if value.startswith('%'):
                    elements = value.split('|',1)
                    elements[0] = elements[0][1:]
                    if len(elements) == 1:
                        elements.append(0)
                    elements[1] = int(elements[1]) - 1
                    if elements[0] == self.source_name:
                        payload[key] = self.source[elements[1]]

                    elif elements[0] == self.random_list_name:
                        payload[key] = []
                        for dest in self.random_list:
                            payload[key].append(dest[elements[1]])

                else:
                    payload[key] = value


            message = payload["SmsBody"] + '_' + self.name + " " + mark
            payload["SmsBody"] = generator.base64_convert(message)

            return urllib.parse.urlencode(payload).encode(encoding="utf-8")

        elif self.type == "xml":
            payload_xml = copy.deepcopy(self.xml)
            root = payload_xml.getroot()
            for key, value in self.payload.items():
                if value.startswith('%'):
                    elements = value.split('|',1)
                    elements[0] = elements[0][1:]
                    if len(elements) == 1:
                        elements.append(0)
                    elements[1] = int(elements[1]) - 1
                    if elements[0] == self.source_name:
                        ET.SubElement(root, key).text = self.source[elements[1]]

                    elif elements[0] == self.random_list_name:
                        for dest in self.random_list:
                            ET.SubElement(root, key).text = dest[elements[1]]

                else:
                    ET.SubElement(root, key).text = value

            # ET.SubElement(root, "SysId").text = self.sysid
            # ET.SubElement(root, "SrcAddress").text = self.account
            # ET.SubElement(root, "SmsBody").text = generator.base64_convert(self.message + " " + mark)
            # ET.SubElement(root, "ExpiryMinutes").text = "1440"
            # root.find("SysId").text = self.sysid
            # root.find("SrcAddress").text = self.account
            message = root.find("SmsBody").text + '_' + self.name + " " + mark
            root.find("SmsBody").text = generator.base64_convert(message)

            # for dest in self.dests:
            #     dest_node = ET.SubElement(root, "DestAddress")
            #     dest_node.text = dest
            payload_xml.write("resources/sent.xml")
            payload = {"xml": ET.tostring(root, encoding= "utf-8")}

            return urllib.parse.urlencode(payload).encode(encoding="utf-8")

def start():
    config = settings.read_config()
    files = {}
    for file_name in config["files"].keys():
        files[file_name] = settings.read_file(file_name)
        config["files"][file_name] = True

    threads = []
    source = files[config['source']]
    random_list = files[config['random_list']]
    flag = config['1to1_Or_1toM_flag'] if '1to1_Or_1toM_flag' in config.keys() else None
    threads_per_setting = config['thread']
    fill = len(str(threads_per_setting))

    thread_name_index = 0
    if thread_name_index == flag[1]:
        thread_name_index += 1

    for i in range(len(source)):
        if flag == None or files[flag[0]][i][flag[1]] == '1to1' :
            for t in range(0, threads_per_setting):
                thread_name = "Thread_" + source[i][thread_name_index] + "_" + str(t).zfill(fill)
                rand = random.randrange(len(random_list))
                threads.append(request_sender(thread_name, config, source[i], [random_list[rand]]))
        
        elif flag == None or files[flag[0]][i][flag[1]] == '1toM' :
            for t in range(0, threads_per_setting):
                thread_name = "Thread_" + source[i][thread_name_index] + "_" + str(t).zfill(fill)
                dests = []
                for j in range(0, config['num_of_rand_content']):
                    num = random.randrange(len(random_list))
                    dests.append(random_list[num])
                threads.append(request_sender(thread_name, config, source[i], dests))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Done!")