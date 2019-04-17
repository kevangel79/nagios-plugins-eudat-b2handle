#!/usr/bin/env python

import argparse
import sys
import b2handle
import traceback
from b2handle.clientcredentials import PIDClientCredentials
from b2handle.handleclient import EUDATHandleClient
from b2handle.handleexceptions import *

import signal

from time import strftime,gmtime

TEST_SUFFIX='NAGIOS-' +  strftime("%Y%m%d-%H%M%S",gmtime())
VALUE_ORIG='http://www.' + TEST_SUFFIX + '.com/1'
VALUE_AFTER='http://www.' + TEST_SUFFIX + '.com/2'

def handler(signum, stack):
    print "UNKNOWN: Timeout reached, exiting."
    sys.exit(3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EPIC API create, read, update, delete probe')
    req = parser.add_argument_group('required arguments')
    req.add_argument('-f', '--file', action='store', dest='json_file', required=True,
            help='JSON credentials file')
    req.add_argument('-p', '--prefix', action='store', dest='prefix',
            help='prefix to test')
    req.add_argument('-t', '--timeout', action='store', dest='timeout',
            help='timeout')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
            help='debug mode')

    param = parser.parse_args()

    if param.timeout and int(param.timeout) > 0 :
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(param.timeout))

    try:

        print "Creating credentials"
        cred = PIDClientCredentials.load_from_JSON(param.json_file)
        client = EUDATHandleClient.instantiate_with_credentials(cred)

        print('PID prefix ' + cred.get_prefix())
        print('Server ' + cred.get_server_URL())

        handle = cred.get_prefix() + '/' + TEST_SUFFIX
        
        # Create test
        print "Creating handle " + handle
        create_result = client.register_handle(
            handle, VALUE_ORIG)

        if create_result == handle:
            print "OK: Create handle successful."
        else:
            print "CRITICAL: Create handle returned unexpected response."
            sys.exit(2)
         
        # Read test
        key = 'URL'
        read_value = client.get_value_from_handle(
            handle, key)
        
        if read_value == VALUE_ORIG:
            print "OK: Read handle successful."
        else:
            print "CRITICAL: Read handle returned unexpected response."
            client.delete_handle(handle)
            sys.exit(2)
        
        # Modify test
        client.modify_handle_value(
            handle, **{key: VALUE_AFTER} )

        get_value_result = client.get_value_from_handle(
            handle, key)

        if get_value_result == VALUE_AFTER:
            print "OK: Modify handle successful."
        else:
            print "CRITICAL: Modify handle value returned unexpected value."
            print "Expected : " + VALUE_AFTER
            print "Returned : " + get_value_result
            client.delete_handle(handle)
            sys.exit(2)
        
        # Delete test

        delete_result = client.delete_handle(handle)
        print "OK: Delete handle successful."
        
    except (GenericHandleError, CredentialsFormatError, HandleSyntaxError, HandleNotFoundException, HandleAuthenticationError) as e:
        print "CRITICAL: " + e.msg
        sys.exit(2)
    except Exception as e:
        print "UNKNOWN: " + traceback.format_exc()
        sys.exit(3)
    

