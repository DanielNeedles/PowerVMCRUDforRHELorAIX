#!/usr/bin/python
######################################################################
# PROGRAM: managevm.py              Daniel Needles        05.30.2017 #
# PURPOSE: Simple list, add, delete of RHEL and AIX VMs              #
# PACKAGES REQUIRED:                                                 #
#        easy_install simplejson                                     #
# NOTE:  Curl to Python Converter:  https://curl.trillworks.com/     #
#        Errors occur when '(' shows up instead of '['. So look.     #
#        See managevm.sh for original CURL commands used.            #
# TODO:                                                              #
# 1. When more than one Network is added it likely will change the   #
#    JSON returned and the parsing will need to change.              #
# 2. Make usage a functon rather than duplicated macro.              #
# 3. Generictize vms,images,flavors,networks, and loop through       #
#    array on same logic rather than repeated macros.                #
######################################################################
import requests    ## FOR ALL ReSTful CALLS
## IGNORE HTTPS CERTIFICATE ISSUE AND SUPRESS WARNING
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#import json       ## FOR JSON PARSING
import simplejson as json       ## FOR JSON PARSING
import sys         ## FOR COMMANDLINE ARGUMENT PARSING
import re          ## Regular expressions to decide if NAME or ID

#####################################################################
## NAME: pp_json
## PURPOSE: Provide pretty printing services for JSON
#####################################################################
def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        try:
            print(json.dumps(json_thing, sort_keys=sort, indent=indents))
        except:
            print(json_thing)
    return ''

#####################################################################
## DECLARE GLOBAL VARIABLES AND CONDITIONS
#####################################################################
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
POWERVMHOST='10.10.10.1'                             ## POWERVM SERVER NAME OR IP
POWERVMPORT='5000'                                   ## POWERVM SERVER PORT
FLAVORREF="211675700dbcaf2327640c31b76b2112"         ## VM SIZING
VMNAME=""                                            ## VM NAME
IMAGEREF=""                                          ## PATTERN USED
NETWORKREF="bcb1fdae-3dad-4a52-8ece-f32418a8fd09"    ## WHICH NETWORK
CREATEVM=""                         ## EXTENDED JSON FOR ADD
TOKEN=""                            ## CREDENTIAL TOKEN
DEBUG=""                            ## DEBUG LEVEL
ISVMNAME="No"                       ## WAS A VM ID OR NAME USED?  (Delete Fx)
ISIMAGENAME="No"                    ## WAS AN IMAGE ID OR NAME USED? (Add fx)
ISFLAVORNAME="No"                   ## WAS A FLAVOR ID OR NAME USED? (Add fx)
ISNETWORKNAME="No"                  ## WAS A NETWORK ID OR NAME USED? (Add fx)
RESTFULQUERY="Not Set"              ## BUFFERED FOR DEBUGGING PURPOSES

#####################################################################
## COMMANDLINE ARGUMENT PARSING
#####################################################################
err=1     ## FLAG IF ERROR IN COMMAND ARGUMENTS, DEFAULT TO TRUE
cmd=""    ## WHICH COMMAND WAS ASKED FOR IN COMMAND ARGUEMENTS
COUNT=len(sys.argv)-1  ## MORE TRADITIONAL ARG MATH (BASH, PERL, ETC)
if ( COUNT <= 6 ):
    ## COMMAND WITH NO ARGS => ASK FOR USAGE
    if ( COUNT == 0 ):
        cmd='usage'
        err=1

    ## LIST AVAILABLE VMS
    elif ( COUNT >= 1  and sys.argv[1] == "vms" ):
        cmd='vms'
        err=0

        ## LIST AVAILABLE VMS WITH DEBUG OPTION
        if ( COUNT == 2 ):
            DEBUG=sys.argv[2]

    ## LIST AVAILABLE NETWORKS
    elif ( COUNT >= 1 and sys.argv[1] == "networks" ):
        # print ("Valid List command")
        cmd='networks'
        err=0

        ## LIST AVAILABLE NETWORKS WITH DEBUG OPTION
        if ( COUNT == 2 ):
            DEBUG=sys.argv[2]

    ## LIST AVAILABLE VM TYPES (Linux, Windows, etc)
    elif ( COUNT >= 1 and sys.argv[1] == "images" ):
        # print ("Valid List command")
        cmd='images'
        err=0

        ## LIST AVAILABLE NETWORKS WITH DEBUG OPTION
        if ( COUNT == 2 ):
            DEBUG=sys.argv[2]

    ## LIST AVAILABLE VM SIZES/FLAVORS
    elif ( COUNT >= 1 and sys.argv[1] == "flavors" ):
        # print ("Valid List command")
        cmd='flavors'
        err=0

        ## LIST AVAILABLE NETWORKS WITH DEBUG OPTION
        if ( COUNT == 2 ):
            DEBUG=sys.argv[2]

    ## REMOVE A PARTICULAR VM
    elif ( COUNT >= 2 and sys.argv[1] == "remove" ):
        err=0
        cmd='remove'
        if (re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', sys.argv[2])):
            VMNAME=sys.argv[2]
        else:
            VMNAME=sys.argv[2]
            ISVMNAME="Yes"
            if (DEBUG != ""):
                print ("W: Name, not ID, provided for VM.")

        ## REMOVE A PARTICULAR VM WITH DEBUG OPTION
        if ( COUNT == 3 ):
            DEBUG=sys.argv[3]

    ## ADD A VM
    elif ( COUNT >= 3 and sys.argv[1] == "add" ):
        VMNAME=sys.argv[2]

        ## DEFAULT IMAGE DEPENDS ON SELECTED OS SO...
        if (re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', sys.argv[3])):
            IMAGEREF=sys.argv[3]
        else:
            IMAGEREF=sys.argv[3]
            ISIMAGENAME="Yes"
            if (DEBUG != ""):
                print ("W: Name, not ID, provided for VM.")
        err=0
        cmd='add'

        ## SPECIFY A SIZE/FLAVOR RATHER THAN ACCEPT THE DEFAULT SIZE
        if ( COUNT >= 4 ):
            if (re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', sys.argv[4])):
                FLAVORREF=sys.argv[4]
            else:
                if ( sys.argv[4] == 'debug'):
                    DEBUG=sys.argv[4]
                else:
                    FLAVORREF=sys.argv[4]
                    ISFLAVORNAME="Yes"
                    if (DEBUG != ""):
                        print ("W: Name, not ID, provided for flavor of VM.")

            ## SPECIFY A NETWORK TO USE RATHER THAN ACCEPT THE DEFAULT SIZE
            if ( COUNT >= 5 ):
                if (re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', sys.argv[5])):
                    NETWORKREF=sys.argv[5]
                else:
                    if ( sys.argv[5] == 'debug'):
                        DEBUG=sys.argv[5]
                    else:
                        NETWORKREF=sys.argv[5]
                        ISNETWORKNAME="Yes"
                        if (DEBUG != ""):
                            print ("W: Name, not ID, provided for network of VM.")

                ## PERFORM THE VM ADD WITH DEBUGGING TURNED ON
                if ( COUNT == 6 ):
                    DEBUG=sys.argv[6]

## INVALID COMMAND LINE ARGUEMENTS? THEN PRINT USAGE
if ( err == 1 ):
    print ("""PURPOSE:
    managevm: Simple list, add, delete of RHEL and AIX VMs
USAGE:
  managevm add (VMNAME) (IMAGE ID/NAME) [(FLAVOR ID/NAME) [{NETWORK ID/NAME)]] [debug]
           remove (VM ID/NAME) [debug]
           vms [debug]
           images [debug]
           flavors [debug]
           networks [debug]""")
    sys.exit(1)

## USE CREDENTIALS TO GET A TOKEN, WHICH WILL BE USED GOING FORWARD INSTEAD OF CREDENTIALS
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

## PERFORM ReSTful COMMAND TO GET CREDENTIAL TOKEN
data = '{"auth": {"scope": {"project": {"name": "ibm-default", "domain": {"name": "Default"} } }, "identity": { "methods": ["password"], "password": { "user": { "domain": { "name": "Default" }, "name": "root", "password": "Ibmp0wer8" }}}}}'
res=requests.post('https://' + POWERVMHOST + ':' + POWERVMPORT + '/v3/auth/tokens', headers=headers, data=data, verify=False)

## TOKEN IS EMBEDDED IN THE HEADER.  SO SCAN ITEMS LISTED IN HEADER AND GRAB TOKEN
for key,value in res.headers.iteritems():
    if key ==  'x-subject-token':
        TOKEN=value
headers['X-Auth-Token']=TOKEN

## SHOW AVAILABLE VMS OR GET VMS ID WITH VMS NAME (FOR ADD OR REMOVE)
if ( cmd == 'vms' or ISVMNAME == 'Yes'):
    RESTFULQUERY='https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/servers'
    res=requests.get('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/servers', headers=headers, verify=False)
    ## PARSE AND PRESENT JSON DATA ITEMS
    vms=json.loads(res.text)
    if (ISVMNAME == 'Yes'):
        ISVMNAME='NotFound'
    for i in range(len(vms['servers'])):
        if (ISVMNAME == 'No'):
            print(vms['servers'][i]['name'] + ',' + vms['servers'][i]['id'])
        elif (vms['servers'][i]['name'] == VMNAME):
            VMNAME=vms['servers'][i]['id']
            ISVMNAME='Found'

## SHOW IMAGE TYPES OR GET IMAGE ID WITH FLAVOR NAME (FOR ADD OR REMOVE)
if ( cmd == 'images' or ISIMAGENAME == 'Yes' ):
    RESFULQUERY= 'https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/images'
    res=requests.get('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/images', headers=headers, verify=False)
    ## PARSE AND PRESENT JSON DATA ITEMS
    images=json.loads(res.text)
    if (ISIMAGENAME == 'Yes'):
        ISIMAGENAME='NotFound'
    for i in range(len(images['images'])):
        if (ISIMAGENAME == 'No'):
            print(images['images'][i]['name'] + ',' + images['images'][i]['id'])
        elif (images['images'][i]['name'] == IMAGEREF):
            IMAGEREF=images['images'][i]['id']
            ISIMAGENAME='Found'

## SHOW FLAVORS OR GET FLAVOR ID WITH FLAVOR NAME (FOR ADD OR REMOVE)
if ( cmd == 'flavors' or ISFLAVORNAME == 'Yes' ):
    RESFULQUERY= 'https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/flavors'
    res=requests.get('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/flavors', headers=headers, verify=False)
    ## PARSE AND PRESENT JSON DATA ITEMS
    flavors=json.loads(res.text)
    if (ISFLAVORNAME == 'Yes'):
        ISFLAVORNAME='NotFound'
    for i in range(len(flavors['flavors'])):
        if (ISFLAVORNAME == 'No'):
            print(flavors['flavors'][i]['name'] + ',' + flavors['flavors'][i]['id'])
        elif (flavors['flavors'][i]['name'] == FLAVORREF):
            FLAVORREF=flavors['flavors'][i]['id']
            ISFLAVORNAME='Found'

## SHOW NETWORKS OR GET NETWORK ID WITH NETWORK NAME (FOR ADD OR REMOVE)
if ( cmd == 'networks' or ISNETWORKNAME == 'Yes' ):
    RESTFULQUERY='https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/network/v2.0/networks'
    res=requests.get('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/network/v2.0/networks', headers=headers, verify=False)
    ## PARSE AND PRESENT JSON DATA ITEMS
    networks=json.loads(res.text)
    if (ISNETWORKNAME == 'Yes'):
        ISNETWORKNAME='NotFound'
    for i in range(len(networks['networks'])):
        if (ISNETWORKNAME == 'No'):
            print(networks['networks'][i]['name'] + ',' + networks['networks'][i]['id'])
        elif (networks['networks'][i]['name'] == NETWORKREF):
            NETWORKREF=networks['networks'][i]['id']
            ISNETWORKNAME='Found'

## VALIDATE ANY AND ALL NAME LOOKUPS
err=0
if (ISVMNAME == 'NotFound'):
    err=1
    print ("E: " + VMNAME + " not a valid VM ID nor VM name.")
if (ISIMAGENAME == 'NotFound'):
    err=1
    print ("E: " + IMAGEREF + " not a valid IMAGE ID nor IMAGE name.")
if (ISFLAVORNAME == 'NotFound'):
    err=1
    print ("E: " + FLAVORREF + " not a valid FLAVOR ID nor FLAVOR name.")
if (ISNETWORKNAME == 'NotFound'):
    err=1
    print ("E: " + NETWORKREF + " not a valid NETWORK ID nor NETWORK name.")
if (err == 1):
    print ("""PURPOSE:
    managevm: Simple list, add, delete of RHEL and AIX VMs
USAGE:
  managevm add (VMNAME) (IMAGE ID/NAME) [(FLAVOR ID/NAME) [{NETWORK ID/NAME)]] [debug]
           remove (VM ID/NAME) [debug]
           vms [debug]
           images [debug]
           flavors [debug]
           networks [debug]""")
    sys.exit(1)
    
## CREATE THE VM
if ( cmd == 'add' ):
    ## BUILD CREATE VM JSON COMMAND
    CREATEVM = ''.join(('{ "server": { "name": "' + VMNAME + '", "imageRef": "' + IMAGEREF + '", "flavorRef": "' + FLAVORREF + '", "max_count": 1, "min_count": 1, "networks": [ { "uuid": "' + NETWORKREF + '"} ], "security_groups": [ { "name": "default"} ] } }'))
    headers['User-Agent']='python-novaclient'
    RESTFULQUERY='https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/servers'
    res=requests.post('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/servers', headers=headers, data=CREATEVM, verify=False)

## DELETE THE VM
elif ( cmd == 'remove' ):
    headers['User-Agent']='python-novaclient'
    url=''.join(('https://' + POWERVMHOST + ':' + POWERVMPORT + '/powervc/openstack/compute/v2/servers/',VMNAME))
    RESTFULQUERY=url
    res=requests.delete(url, headers=headers, verify=False)
    if (res.text != ""):
        print("E: Deletion failed with:")
        print(res.text.replace('"','').replace('{','').replace('}',''))

if (res.status_code < 200 or res.status_code > 299):
    print ("E: Non 200 status code returned: " + str(res.status_code))

## IF DEBUG IS ON, PRETTY PRINT WHAT WAS SENT AND WHAT WAS RECEIVED
if (DEBUG != ""):
    print ("SENT HEADERS")
    print (pp_json(headers))
    print ("SENT TEXT")
    print (RESTFULQUERY)
    print ("")
    if (CREATEVM != ""):
        print ("EXTENDED JSON SENT FOR ADD")
        print (pp_json(CREATEVM))
    print "RETURNED HEADERS"
    ## COMPLEXITY HERE FIXES SINGLE QUOTES RATHER THAN DOUBLES
    print (pp_json(str(res.headers).replace("'",'"')))
    print "RETURNED TEXT"
    ## COMPLEXITY HERE FIXES u PREPRENDING SO PARSING WORKS
    if (res.text != ""):
        print (pp_json(json.JSONDecoder().decode(res.text)))
    else:
        print ("")
    print "RETURNED STATUS CODE"
    print (res.status_code)
