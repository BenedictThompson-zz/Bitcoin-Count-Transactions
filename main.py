#!/usr/bin/env python

from websocket import create_connection
import simplejson as json
import time
time_to_run = 86400 
total = 0
def find_input_addresses(inputs):
    input_addressses = []
    for i in range(len(inputs)):
        for ins in inputs[i].values():
            try: 
                prev_out = dict(ins)
                if prev_out['addr'] != "None":
                    input_addressses.append(prev_out['addr'])
            except (ValueError, TypeError, KeyError): 
                pass
    return input_addressses

def find_output_addresses(outputs):
    output_addresses = []
    for out in outputs:
        if out['addr'] != "None":
            output_addresses.append(out['addr'])
    return output_addresses

def latest_transactions():
    global total
    ws = create_connection("ws://ws.blockchain.info/inv")
    ws.send('{"op":"unconfirmed_sub"}')
    start_time = time.time()
    while (time.time() - start_time) < time_to_run:
        result = ws.recv()
        
        result = json.loads(result)
        input_addresses =  find_input_addresses(result['x']['inputs'])
        output_addresses = find_output_addresses(result['x']['out'])
        addresses = filter(lambda x: x not in input_addresses, output_addresses)
        total += len(addresses)
            
    print total
    ws.close()
    

if __name__ == '__main__':
    latest_transactions()


    
