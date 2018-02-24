'''
Created on 11Nov.,2017
MIT License
Copyright (c) 2017 David Nearhos
Version 1.0
'''

import json
import uuid
import os
import sys
import requests
from array import *

def fablog(log_statement):
    # logger for debuging
    print(log_statement)

def load_json(json_file):
    # load a json file and returns a json as a decoded python object
    fablog("Loading: " + json_file)
    
    f = open(json_file, 'r')
    json_result = json.load(f)
    f.close()
    return json_result

def write_json(json_file, json_payload):
    # takes a python object and encodes it into json and writes a json file
    fablog("Writing: " + json_file)
    
    f = open(json_file, 'w')
    json.dump(json_payload, f, sort_keys=True, indent=4)
    f.close()
    return True


def load_connection(connect_file = 'connect.json'):
    # load connection and register device if need
    # returns the connection as a decoded python object
    fablog("Load Connection")
    
    f = open(connect_file, 'r')
    connect_json = json.load(f)
    f.close()
    if len(connect_json['device_uuid']) > 18:
        fablog("UUID Exists")
        return connect_json
    else:
        # create a device id and register it
        fablog("Creating new UUID")
        device_uuid = uuid.uuid4()
        device_uuid_str = device_uuid.urn
        connect_json['device_uuid'] = device_uuid_str[9:]
        
        f = open(connect_file, 'w')
        json.dump(connect_json, f, sort_keys=True, indent=4)
        f.close()
        return connect_json

def initalise_device(fabrica_json):
    # send initialisation message to host with device_id and uuid
    # get connection settings
    fablog("Performing device initalisation with host sync")
    host_connection = fabrica_json['host'] + fabrica_json['device_init']
    fablog("Host Connection:")
    fablog(host_connection)

    connect_json = load_connection(fabrica_json['connect_json'])
    fablog("DEBUG connect json:")
    fablog(connect_json)
    
    # create payload with connection credentials
    # payload = connect_json
    payload = {"connect_json" : "NULL"}
    payload["connect_json"] = connect_json
    json_payload = json.dumps(payload, sort_keys=True, indent=4)
    fablog("DEBUG json_payload:")
    fablog(json_payload)
    
    # send and receive data
    r = requests.post(host_connection, json_payload)
    inbound_data = json.loads(r.text)
    fablog("DEBUG raw inbound:")
    fablog(inbound_data)
    
    # update connect json with the first token
    connect_json['device_token'] = inbound_data['connect_json']['device_token']
    fablog("DEBUG inbound_data:")
    fablog(json.dumps(inbound_data, sort_keys=True, indent=4))
    write_json(fabrica_json['connect_json'], connect_json)
    
    return inbound_data

def sync_device(fabrica_json):
    # Send data and receive data with host
    # get connection settings
    fablog("Performing device initalisation with host sync")
    host_connection = fabrica_json['host'] + fabrica_json['device_message']
    fablog("Host Connection:")
    fablog(host_connection)

    connect_json = load_connection(fabrica_json['connect_json'])
    fablog("DEBUG connect json:")
    fablog(connect_json)
    
    # create payload with connection credentials
    # payload = connect_json
    payload = {"connect_json" : "NULL", "data_json" : "NULL"}
    output_data = load_json(fabrica_json['output_data'])    
    payload["connect_json"] = connect_json
    payload["data_json"] = output_data
    
    
    #payload.append(connect_json)
    #payload.append(output_data)
    fablog("DEBUG payload:")
    fablog(payload)
    
    json_payload = json.dumps(payload, sort_keys=True, indent=4)
    fablog("DEBUG json_payload:")
    fablog(json_payload)
    
    # send and receive data
    r = requests.post(host_connection, json_payload)
    fablog("DEBUG raw inbound:")
    fablog(r.text)
    
    inbound_data = json.loads(r.text)
    #inbound_data = r.json()
    fablog("DEBUG inbound_data:")
    fablog(json.dumps(inbound_data, sort_keys=True, indent=4))
    write_json(fabrica_json['input_data'], inbound_data)
    
    # update connect json with new token
    connect_json['device_token'] = inbound_data['connect_json']['device_token']
    write_json(fabrica_json['connect_json'], connect_json)
    
    return inbound_data


def func_turn_pump_on(on_time):
    # device defined function called by action - turn_pump_on
    fablog("Turn pump on for : " + str(on_time) + " sec")

def fab_process_actions(fabrica_json):
    # process actions from input data within 'data_json'
    fablog("Get Current Input Data From JSON")
    input_data = load_json(fabrica_json['input_data'])
    num_triggers = len(input_data['data_json'])
    fablog("Number of triggers to process: " + str(num_triggers))
    for i in range(num_triggers):
        num_actions = len(input_data['data_json'][i]['actions'])
        fablog("Number of actions to process: " + str(num_actions) + " ... in trigger number " + str(i))
        for j in range(num_actions):
            fablog("Process action: " + str(input_data['data_json'][i]['actions'][j]))
            
            # ################################################
            # ###   INITIATE LOCAL DEVICE FUNCTIONS HERE   ###
            # ################################################
            if input_data['data_json'][i]['actions'][j] in ('turn_pump_on'):
                # call to func_turn_pump_on(on_time)
                func_turn_pump_on(input_data['data_json'][i]['data']['device_on_time'])
    
    return True

def fab_loop(fabrica_json):
    # commence device loop
    fablog("Device loop started")

    while True:
        # manual device loop - can be replaced with timed polling interval etc.
        loop_again = input("Press x to exit, press i to initialise, s to sync with host, p to process device action : ")

        if loop_again in ('x'):
            # exit device loop cycle
            fablog("Device loop stopped")
            return False
        elif loop_again in ('i'):
            # initialise device
            fablog("Initialising device")
            initalise_device(fabrica_json)
        elif loop_again in ('s'):
            # sync with host
            fablog("Sync with host")
            sync_device(fabrica_json)
        elif loop_again in ('p'):
            # process device action
            fablog("Process device action")
            fab_process_actions(fabrica_json)
        else:
            # execute device loop cycle
            fablog("Invalid command")


if __name__ == '__main__':
    # main program - execution starts here
    fablog("*** fabrica Device Started ***")
    os.system("which python")
    fablog(sys.version)

    # load configuration 
    fabrica_json = load_json('fabrica_test.json')
    fablog("connect_json: " + fabrica_json['connect_json'])
    connect_json = load_connection(fabrica_json['connect_json'])
    
    
    # log connection results
    s = "Device ID = " + connect_json['device_id']
    fablog(s)
    s = "Device Token = " + connect_json['device_token']
    fablog(s)
    s = "Device UUID = " + connect_json['device_uuid']
    fablog(s)
    
    # polling loop
    fab_loop(fabrica_json)
    
    
    # main program - execution stops here
    fablog("*** fabrica Device Stoped ***")
