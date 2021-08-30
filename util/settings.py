import json
import xml.etree.ElementTree as ET

def read_config() :
    server = ""
    api = ""
    config = {}
    with open('resources/config.properties','r') as cfg :
        lines = cfg.readlines()
        payload = {}
        headers = {}
        files = {}
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue

            setting = [x.strip() for x in line.split('=', 1)]
            if len(setting) != 2:
                continue
            if setting[1].startswith('%'):
                file_name = setting[1][1:].split('|',1)[0]
                files[file_name] = False
            if 'server' in setting[0]:
                server = setting[1]
                if not server.endswith("/") :
                    server += '/'
                if not server.startswith("http"):
                    server = "http://" + server
            elif 'api' in setting[0] :
                api = setting[1]
            elif 'interval' in setting[0]:
                config['interval'] = int(setting[1])
            elif 'message' in setting[0]:
                config['message'] = setting[1]
            elif 'loop' in setting[0]:
                config['loop'] = int(setting[1])
            elif 'thread' in setting[0]:
                config['thread'] = int(setting[1])
            elif 'content-type' in setting[0]:
                config['content-type'] = setting[1]
            elif 'source' in setting[0]:
                value = setting[1]
                config['source'] = value[1:] if value.startswith('%') else value
            elif 'random_list' in setting[0]:
                value = setting[1]
                config['random_list'] = value[1:] if value.startswith('%') else value
            elif '1to1_Or_1toM_flag' in setting[0]:
                elements = setting[1].split('|',1)
                elements[0] = elements[0][1:] if elements[0].startswith('%') else elements[0]
                if len(elements) == 1:
                    elements.append(1)
                elements[1] = int(elements[1]) - 1
                config['1to1_Or_1toM_flag'] = elements
            elif 'num_of_rand_content' in setting[0]:
                config['num_of_rand_content'] = int(setting[1])
            elif setting[0].startswith('payload'):
                payload[setting[0].split('.',1)[1]] = setting[1]
            elif setting[0].startswith('headers'):
                headers[setting[0].split('.',1)[1]] = setting[1]
    
    if server is None or server == "":
        print("url is not defined...exit test")
        exit()
    url = server + api
    print("Target URL: " + url)
    config["url"] = url
    config["files"] = files
    config["payload"] = payload
    config["headers"] = headers

    return config

def read_file(file_name):
    file = []
    with open(f"resources/{file_name}", 'r') as f:
        lines = f.readlines()
        for line in lines:
            file.append([x.strip() for x in line.split(',')])

    return file

def read_accounts():
    accounts = {"1to1":[], "1toM":[]}
    with open("resources/accounts") as f:
        lines = f.readlines()
        for line in lines:
            account_setting = [x.strip() for x in line.split(',')]
            sysid = account_setting[0]
            account = account_setting[1]
            mode = account_setting[2] if len(account_setting) == 3 else '1to1'
            if mode == "1to1" :
                accounts["1to1"].append([sysid,account])
            elif mode == "1toM" :
                accounts["1toM"].append([sysid,account])
    
    return accounts

def read_source():
    accounts = {"1to1":[], "1toM":[]}
    with open("resources/accounts") as f:
        lines = f.readlines()
        for line in lines:
            account_setting = [x.strip() for x in line.split(',')]
            sysid = account_setting[0]
            account = account_setting[1]
            mode = account_setting[2] if len(account_setting) == 3 else '1to1'
            if mode == "1to1" :
                accounts["1to1"].append([sysid,account])
            elif mode == "1toM" :
                accounts["1toM"].append([sysid,account])
    
    return accounts

def read_dest():
    addresses = []
    with open("resources/destinations") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 10:
                addresses.append(line)
    return addresses


def read_default_json():
    json_file = ""
    with open("resources/payload.json") as f:
        json_file = json.load(f)

    return json_file

def read_default_xml():
    return ET.parse("resources/payload.xml")