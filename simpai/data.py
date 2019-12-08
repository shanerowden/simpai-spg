#!/usr/bin/env python3

import json, logging

def jload(path):
    with open(path) as fo:
        data = json.load(fo)
        logging.debug(f'data: {data}, path: {path}')
        return data
    
def jdump(data, path):
    strpath = str(path)
    with open(strpath, 'w') as fo:
        json.dump(data, fo)
    logging.debug(f'data: {data}, path: {path}, strpath: {strpath}')
    return data

logging.info(f'loaded simpai.data')

if __name__ == '__main__':
    pass
