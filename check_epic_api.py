#!/usr/bin/env python

import argparse
import sys
import epicclient

import signal

from time import strftime,gmtime

TEST_SUFFIX='NAGIOS-' +  strftime("%Y%m%d-%H%M%S",gmtime())
VALUE_ORIG='http://www.testB2SafeCmd.com/1'
VALUE_AFTER='http://www.testB2SafeCmd.com/2'

def handler(signum, stack):
    raise Exception("Timeout reached, exiting.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EPIC API create, read, update, delete probe')
    req = parser.add_argument_group('required arguments')
    req.add_argument('--url', action='store', dest='url', required=True,
            help='baseuri of EPIC API to test')
    req.add_argument('--username', action='store', dest='username', required=True,
            help='EPIC API user')
    req.add_argument('--pass', action='store', dest='password', required=True,
            help='EPIC API key')
    req.add_argument('--prefix', action='store', dest='prefix', required=True,
            help='prefix to test')
    req.add_argument('--timeout', action='store', dest='timeout',
            help='timeout')
    parser.add_argument('--debug', action='store_true', dest='debug',
            help='debug mode')

    param = parser.parse_args()

    if param.timeout and int(param.timeout) > 0 :
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(param.timeout))

    try:

        url = param.url

        if (url[-1] != '/'):
            url = url + '/'

        # Credentials __init__ has been modified to accept url,username,password,prefix and dbg as arguments
        cred = epicclient.Credentials(uri=url, username=param.username, password=param.password,
                        prefix=param.prefix, dbg=param.debug)

        client = epicclient.EpicClient(cred)

        # Create test

        create_result = client.createHandle(
            cred.prefix, VALUE_ORIG, None, None,
            None, TEST_SUFFIX)

        if create_result == str(cred.prefix + '/' + TEST_SUFFIX):
            print "OK: Create handle successful.\n"
        else:
            print "CRITICAL: Create handle returned unexpected response.\n"
            sys.exit(2)
    
        # Read test

        read_value = client.getValueFromHandle(
            cred.prefix, 'URL', TEST_SUFFIX)
  
        if read_value == VALUE_ORIG:
            print "OK: Read handle successful.\n"
        else:
            print "CRITICAL: Read handle returned unexpected response.\n"
            client.deleteHandle(cred.prefix, '', TEST_SUFFIX)
            sys.exit(2)

        # Modify test

        key = 'URL'
        modify_result = client.modifyHandle(
            cred.prefix, key, VALUE_AFTER, TEST_SUFFIX)

        if not modify_result:
            print "CRITICAL: Modify handle value returned unexpected response.\n"
            client.deleteHandle(cred.prefix, '', TEST_SUFFIX)
            sys.exit(2)

        get_value_result = client.getValueFromHandle(
            cred.prefix, key, TEST_SUFFIX)

        if get_value_result == VALUE_AFTER:
            print "OK: Modify handle successful.\n"
        else:
            print "CRITICAL: Modify handle value returned unexpected value.\n"
            print "Expected : " + VALUE_AFTER + "\n"
            print "Returned : " + get_value_result + "\n"
            client.deleteHandle(cred.prefix, '', TEST_SUFFIX)
            sys.exit(2)

        # Delete test

        delete_result = client.deleteHandle(cred.prefix, '', TEST_SUFFIX)

        if delete_result:
            print "OK: Delete handle successful.\n"
            sys.exit(0)
        else:
            print "CRITICAL: Delete existing handle returned unexpected response.\n"
            sys.exit(2)

    except Exception as e:
        print e + "\n"
        sys.exit(3)
    

