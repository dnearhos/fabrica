'''
Created on 11Nov.,2017
MIT License
Copyright (c) 2017 David Nearhos
'''

import json
import uuid

def fablog(log_statement):
    # flexible logger for debuging
    print(log_statement)

def load_connection(connect_file = 'connect.json'):
    # load connection and register device if need
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

def fab_input():
    # check and get any input
    fablog("Input Check and Get")
    return True

def fab_output():
    # push any output back to central
    fablog("Output Push")

def fab_condition_test():
    # test if conditions are met to trigger an action
    fablog("Condition Test")
    return True

def fab_action():
    # implement an action that has been triggered
    fablog("Implement Action")

def fab_loop():
    # commence device loop
    fablog("Device loop started")

    while True:
        # manual device loop to be replaced with timed polling interval
        loop_again = input("Press x to exit device loop cycle: ")
        if loop_again in ('x'):
            # exit device loop cycle
            fablog("Device loop stopped")
            return False
        else:
            # execute device loop cycle
            fablog("Commence device loop cycle")
            if fab_input() == True:
                # input received
                if fab_condition_test() == True:
                    # condition triggered
                    fab_action()
                    fab_output()


if __name__ == '__main__':
    # main program - execution starts here
    fablog("*** fabrica Device Started ***")
    
    connect_file = 'connect_test.json'
    connect_json = load_connection(connect_file)
    
    # log connection results
    s = "Device ID = " + connect_json['device_id']
    fablog(s)
    s = "Device Token = " + connect_json['device_token']
    fablog(s)
    s = "Device UUID = " + connect_json['device_uuid']
    fablog(s)
    
    # polling loop
    fab_loop()
    
    
    # main program - execution stops here
    fablog("*** fabrica Device Stoped ***")
