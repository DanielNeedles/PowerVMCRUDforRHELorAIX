#!/bin/bash
######################################################################
# PROGRAM: managevm         Daniel Needles                05.18.2017 #
# PURPOSE: Simple list, add, delete of RHEL and AIX VMs              #
# TODO:                                                              #
# 1. Abstract to variable the IP addr and PORT.                      #
######################################################################

#####################################################################
## COMMANDLINE ARGUMENT PARSING
#####################################################################
err=1
cmd=""
FLAVORREF="211675700dbcaf2327640c31b76b2112"
if [ "$#" -le "4" ]; then
  if  [ "$#" -eq "0" ]; then
    cmd='usage'
    err=1
  elif  [ "$#" -eq "1" ] && [ "$1" == "vms" ]; then
    # echo "Valid List command"
    cmd='vms'
    err=0
  elif  [ "$#" -eq "1" ] && [ "$1" == "images" ]; then
    # echo "Valid List command"
    cmd='images'
    err=0
  elif  [ "$#" -eq "1" ] && [ "$1" == "flavors" ]; then
    # echo "Valid List command"
    cmd='flavors'
    err=0
  elif  [ "$#" -eq "2" ] && [ "$1" == "remove" ]; then
    export VMNAME=$2
    # echo "Valid Remove command"
    err=0
    cmd='remove'
  elif  [ "$#" -eq "3" ] && [ "$1" == "add" ]; then
    export VMNAME=$2
    OS=$3
    if [ "$OS" == "AIX" ]; then
      export IMAGEREF="47149635-026d-459e-8584-999f0743aca7"
    elif [ "$OS" == "RHELbe" ]; then
      export IMAGEREF="5d9e8bc3-ca17-4be3-8377-7ab8f3bfa122"
    elif [ "$OS" == "RHELbl" ]; then
      export IMAGEREF="e9212533-1ff2-40b8-9dad-19271fe143a1"
    else
      echo "E: Invalid OS."
      echo "USAGE: managevm (VMNAME) [AIX|RHELbe|RHELbl]"
      exit 1
    fi
    # echo "Valid Add command"
    err=0
    cmd='add'
  elif  [ "$#" -eq "4" ] && [ "$1" == "add" ]; then
    export VMNAME=$2
    OS=$3
    if [ "$OS" == "AIX" ]; then
      export IMAGEREF="47149635-026d-459e-8584-999f0743aca7"
    elif [ "$OS" == "RHELbe" ]; then
      export IMAGEREF="5d9e8bc3-ca17-4be3-8377-7ab8f3bfa122"
    elif [ "$OS" == "RHELbl" ]; then
      export IMAGEREF="e9212533-1ff2-40b8-9dad-19271fe143a1"
    else
      echo "E: Invalid OS."
      echo "USAGE: mkvm (VMNAME) [AIX|RHELbe|RHELbl]"
      exit 1
    fi
    export FLAVORREF=$4
    # echo "Valid Add command"
    err=0
    cmd='add'
  fi
fi
if [ "$err" -eq "1" ]; then
  echo "PURPOSE: 
  managevm: Simple list, add, delete of RHEL and AIX VMs
USAGE: 
  managevm add (VMNAME) (AIX|RHELbe|RHELbl) [FLAVOR ID]  ## USE ID, NOT NAME
       remove (VM ID)                                    ## USE ID, NOT NAME
       vms                                               ## LISTS ID THEN NAME
       images                                             ## LISTS ID THEN NAME"
       flavors                                           ## LISTS ID THEN NAME"
  exit 1
fi

## BUILD CREATE VM JSON COMMAND
export CREATEVM='{
  "server": {
    "name": "'$VMNAME'",
    "imageRef": "'$IMAGEREF'",
    "flavorRef": "'$FLAVORREF'",
    "max_count": 1,
    "min_count": 1,
    "networks": [
      { "uuid": "bcb1fdae-3dad-4a52-8ece-f32418a8fd09"}
    ],
    "security_groups": [
      { "name": "default"}
    ]
  }
}'

## GRAB THE TOKEN
export TOKEN=`curl -1 -k -i -s -X POST https://10.0.0.1:5000/v3/auth/tokens -H "Accept: application/json" -H "Content-Type: application/json" -d '
{"auth":
  {"scope":
    {"project":
      {"name": "ibm-default",
       "domain": {"name": "Default"}
      }
    },
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "domain": {
            "name": "Default"
          },
          "name": "root",
          "password": "Ibmp0wer8"
        }
      }
    }
  }
}' | grep X-Subject-Token | cut -d ' ' -f2 | tr -d $'\r'`

if [ $cmd == 'vms' ]; then
  curl -l -k -i -s  -X GET https://10.0.0.1:5000/powervc/openstack/compute/v2/servers -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" | sed -e 's/[{}]/''/g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | egrep "name|id\"" | sed 's:]::' | sed 's~"name":~~' | sed -e 's~"servers": \[~~'

## SHOW IMAGES
elif [ "$cmd" == 'images' ]; then
curl -l -k -i  -X GET https://10.0.0.1:5000/powervc/openstack/compute/v2/images -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" | sed -e 's/[{}]/''/g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | egrep "name|id\"" | sed 's:]::' | sed 's~"name":~~'i | sed -e 's~"flavors": \[~~'

## SHOW FLAVORS
elif [ "$cmd" == 'flavors' ]; then
 curl -l -k -i -s  -X GET https://10.0.0.1:5000/powervc/openstack/compute/v2/flavors -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json"  | sed -e 's/[{}]/''/g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | egrep "name|id\"" | sed 's:]::' | sed 's~"name":~~'i | sed -e 's~"flavors": \[~~'


## CREATE THE VM
elif [ "$cmd" == 'add' ]; then
  curl -g -l -k -i -s -X POST https://10.0.0.1:5000/powervc/openstack/compute/v2/servers -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d "$CREATEVM" 

## DELETE THE VM
elif [ "$cmd" == 'remove' ]; then
  curl -g -l -k -i -s -X DELETE https://10.0.0.1:5000/powervc/openstack/compute/v2/servers/$VMNAME -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"
fi
