#!/usr/bin/env python

import argparse

__author__ = 'lphan'

import sys
import epicclient

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EPIC API create, read, update, delete probe')
    parser.add_argument('--url', action='store', dest='url', required=True)
    parser.add_argument('--username', action='store', dest='username', required=True)
    parser.add_argument('--pass', action='store', dest='password', required=True)
    parser.add_argument('--prefix', action='store', dest='prefix',required=True)
    parser.add_argument('--debug', action='store_true', dest='debug')

    param = parser.parse_args()

    cred = epicclient.Credentials(uri=param.url, username=param.username, password=param.password,
                        prefix=param.prefix, dbg=param.debug)

    client = epicclient.EpicClient(cred)
    
    print "Testing creating handle:\n"

    create_result = client.createHandle(
            cred.prefix, 'http://www.testB2SafeCmd.com/1', None, None,
            None, 'TEST_CR1')

    if create_result == str(cred.prefix + '/TEST_CR1'):
        print "Create handle successful.\n"
    else:
        print "Create handle returns unexpected response.\n"
        sys.exit(2)
    
    print "Testing reading handle:\n"

    search_result = client.searchHandle(
            cred.prefix, 'URL', 'http://www.testB2SafeCmd.com/1')
  
    if search_result == create_result:
        print "Read handle successful.\n"
    else:
        print "Read handle returns unexpected response.\n"
        client.deleteHandle(cred.prefix, '', 'TEST_CR1')
        sys.exit(2)
    
    print "Testing updating handle:\n"

    key = 'URL'
    value_after = 'http://www.testB2SafeCmd.com/2'
    modify_result = client.modifyHandle(
        cred.prefix, key, value_after, 'TEST_CR1')

    if not modify_result:
        print "Modify handle value should return True.\n"
        client.deleteHandle(cred.prefix, '', 'TEST_CR1')
        sys.exit(2)

    get_value_result = client.getValueFromHandle(
        cred.prefix, key, 'TEST_CR1')

    if get_value_result == value_after:
        print "Modify handle successful.\n"
    else:
        print "Modify handle value failed to update value.\n"
        client.deleteHandle(cred.prefix, '', 'TEST_CR1')
        sys.exit(2)

    print "Testing deleting handle:\n"

    delete_result = client.deleteHandle(cred.prefix, '', 'TEST_CR1')

    if delete_result:
        print "Delete handle successful.\n"
        sys.exit(0)
    else:
        print "Delete existing handle should return True\n"
        sys.exit(2)

    

