# PowerVMCRUDforRHELorAIX
Simple CRUD of RHEL and AIX VMs on PowerVM

The program was created to allow Redhat's CloudForms to create RHEL and AIX VMs on IBM's PowerVC using effectively calls to Openstack.  It comes in two flavors: python and bash.  The usage is similar.

NOTE:  The following are hardcoded into the scripts and not parameterized:
  server IP and port
  server credentials (user and password)
  OS images (via their ids) 

# PYTHON

## PROGRAM:

    ./managevm.py
    
## PURPOSE:

    managevm: Simple list, add, delete of RHEL and AIX VMs

## USAGE:

    managevm add (VMNAME) (AIX|RHELbe|RHELbl) (FLAVOR ID) ## USE ID, NOT NAME
        remove (VM ID)                                  ## USE ID, NOT NAME
        vms                                    
        flavors                               

## INSTALL:

The managevm.py script is a standalone script.  Its only dependencies are the simplejson python package.  In the script for the server change the IP address (10.1.1.X), the port (5000), the user (root), and the password (PASSWORD) to the desired values.  Also the CRUD of images isn't supported by the script.  The image selection is currently hardcoded and should be modified to taste.

## TEST:

No fancy testing for the simple script.  Only a shell script in the test directory that runs several of the commands.  Note either the test script will need either the managevm.py script local or on the path.
  
  
# BASH

## PROGRAM: 

    ./managevm.sh

## PURPOSE:

    managevm: Simple list, add, delete of RHEL and AIX VMs

## USAGE:

    managevm add (VMNAME) (AIX|RHELbe|RHELbl) [FLAVOR ID]  ## USE ID, NOT NAME
       remove (VM ID)                                    ## USE ID, NOT NAME
       vms                                               ## LISTS ID THEN NAME
       flavors                                           ## LISTS ID THEN NAME


## INSTALL:

The managevm.sh script is a standalone script.  It has no real dependencies except standard Linux/UNIX commands such as curl.  In the script for the server change the IP address (10.1.1.X), the port (5000), the user (root), and the password (PASSWORD) to the desired values.    Also the CRUD of images isn't supported by the script.  The image selection is currently hardcoded and should be modified to taste.

## TEST:

No fancy testing for the simple script.  Only a shell script in the test directory that runs several of the commands.  Note either the test script will need either the managevm.py script local or on the path.

# LINKS

## IBM PowerVC Doc

https://www.ibm.com/support/knowledgecenter/SSXK2N_1.3.2/com.ibm.powervc.standard.help.doc/powervc_pg_novacompute_hmc.html#powervc_pg_novacompute__d26793e426

## Python Web Sessions

http://docs.python-requests.org/en/master/user/advanced/

## ISSUED – OpenStack CURL

https://developer.openstack.org/api-guide/quick-start/api-quick-start.html

## OpenStack Commandline Cheats

https://docs.openstack.org/user-guide/cli-cheat-sheet.html

## Delete an Instance

NOTE:  Use –debug to see the CURL behind the command
https://docs.openstack.org/user-guide/cli-delete-an-instance.html 

# PYTHON EXAMPLES

## LIST CURRENT VMS BY ID:

    [root@localhost DNEEDLES]# ./managevm.py vms
    DanRHELbe,57cd0794-4d5e-46ec-be70-878251874509
    DanRHELbl,ee00e912-e945-45cd-9840-ea6c4289367d
    DanAIX3,3135bdab-f305-40e5-acf6-fd4d17e75bd2
    DanAIX2,b575f793-233a-4a3f-a92f-c51a818d9b7d
    DanAIX2,75f2a9ff-e6c5-429d-9041-872776f4059a
    DanAIX,671f29ea-625d-4fb5-85d4-34c92674b656
    RHELbltest,e87751bc-7615-4a2c-a705-16a9b94654c1
    RHELbeTest,abd30328-c712-4946-afd0-2512c1cae7e4
    TSM01,588dc831-d5c4-4edd-9925-7e34ef8d0af1

## LIST POSSIBLE FLAVORS:

    [root@localhost DNEEDLES]# ./managevm.py flavors
    211675700dbcaf2327640c31b76b2112,211675700dbcaf2327640c31b76b2112
    powervm.tiny,2c710505-79f7-4021-b7f5-98e113c261d4
    35fccbcc466eb0351dc6da48b7eee6a0,35fccbcc466eb0351dc6da48b7eee6a0
    powervm.large,388b8d80-bc79-42e3-9aac-3a73b5c32024
    707c59e00f8dbe18eaf35cef094836a2,707c59e00f8dbe18eaf35cef094836a2
    powervm.xxlarge,75bf7b06-760f-400e-b25b-58be990bcf4c
    9017c674b0d3e57f425caccaecdd547e,9017c674b0d3e57f425caccaecdd547e
    bccddede2ae403586a5ce4857f737476,bccddede2ae403586a5ce4857f737476
    powervm.medium,ce5b1b67-53b4-4f1f-8cd3-c834d0c616d5
    powervm.xlarge,def7aede-286b-4eb3-b12f-ed32201b5687
    efa46d929e81d7371760ee2a639f5e28,efa46d929e81d7371760ee2a639f5e28
    powervm.small,f74113a9-4a31-48d9-b3d3-6535a6de8d9d

## ADD A RHEL VM BY IMAGE NAME:

    [root@localhost DNEEDLES]# ./managevm.py add RHELbeTest2 RHELbe

## ADD A RHEL VM BY IMAGE ID:

    [root@localhost DNEEDLES]# ./managevm.py add RHELblTest2 RHELbl 2c710505-79f7-4021-b7f5-98e113c261d4

## ADD A AIX VM BY IMAGE ID:

    [root@localhost DNEEDLES]# ./managevm.py add AIXTest2 AIX 2c710505-79f7-4021-b7f5-98e113c261d4

## LIST CURRENT VMS BY ID:

    [root@localhost DNEEDLES]# ./managevm.py vms
    AIXTest2,09df7e6b-86d6-4d52-91cc-66b30fc08e29
    RHELblTest2,1a4e0f71-5d62-4da3-8ddf-0401f0462b19
    RHELbeTest2,1dc693a6-3573-4a67-8b6d-a8024fb348e5
    RHELbeTest2,7c1b93f0-2c21-47fc-ad90-a2612ba29fef
    RHELbeTest2,7c3a7c26-ec6d-48a3-915a-4fed245fe703
    DanRHELbe,57cd0794-4d5e-46ec-be70-878251874509
    DanRHELbl,ee00e912-e945-45cd-9840-ea6c4289367d
    DanAIX3,3135bdab-f305-40e5-acf6-fd4d17e75bd2
    DanAIX2,b575f793-233a-4a3f-a92f-c51a818d9b7d
    DanAIX2,75f2a9ff-e6c5-429d-9041-872776f4059a
    DanAIX,671f29ea-625d-4fb5-85d4-34c92674b656
    RHELbltest,e87751bc-7615-4a2c-a705-16a9b94654c1
    RHELbeTest,abd30328-c712-4946-afd0-2512c1cae7e4
    TSM01,588dc831-d5c4-4edd-9925-7e34ef8d0af1

## REMOVE THREE IMAGES BY THEIR IDs:

    [root@localhost DNEEDLES]# ./managevm.py remove b575f793-233a-4a3f-a92f-c51a818d9b7d

    [root@localhost DNEEDLES]# ./managevm.py remove 7c3a7c26-ec6d-48a3-915a-4fed245fe703

    [root@localhost DNEEDLES]# ./managevm.py remove 7c1b93f0-2c21-47fc-ad90-a2612ba29fef

## LIST CURRENT VMS BY ID:

    [root@localhost DNEEDLES]# ./managevm.py vms
    AIXTest2,09df7e6b-86d6-4d52-91cc-66b30fc08e29
    RHELblTest2,1a4e0f71-5d62-4da3-8ddf-0401f0462b19
    RHELbeTest2,1dc693a6-3573-4a67-8b6d-a8024fb348e5
    DanRHELbe,57cd0794-4d5e-46ec-be70-878251874509
    DanRHELbl,ee00e912-e945-45cd-9840-ea6c4289367d
    DanAIX3,3135bdab-f305-40e5-acf6-fd4d17e75bd2
    DanAIX2,75f2a9ff-e6c5-429d-9041-872776f4059a
    DanAIX,671f29ea-625d-4fb5-85d4-34c92674b656
    RHELbltest,e87751bc-7615-4a2c-a705-16a9b94654c1
    RHELbeTest,abd30328-c712-4946-afd0-2512c1cae7e4
    TSM01,588dc831-d5c4-4edd-9925-7e34ef8d0af1


# BASH EXAMPLES

## LIST CURRENT VMS BY ID:

    [root@localhost DNEEDLES]# ./managevm.sh vms
    "id": "c2ec56b3-efdc-4481-a84e-50cb191ae852"
      "NewRHELbl"
    "id": "588dc831-d5c4-4edd-9925-7e34ef8d0af1"
      "TSM01"

## REMOVE A VM BY ITS ID:

    [root@localhost DNEEDLES]# ./managevm.sh remove "c2ec56b3-efdc-4481-a84e-50cb191ae852"
    HTTP/1.1 204 No Content
    Date: Fri, 19 May 2017 06:29:11 GMT
    Server: Apache
    Content-Length: 0
    Content-Type: application/json
    X-Compute-Request-Id: req-5ac0a230-0b38-45c0-9129-45fcff6bd935
    Cache-control: max-age=0, no-cache, no-store, must-revalidate
    Pragma: no-cache

## LIST POSSIBLE FLAVORS:

    [root@localhost DNEEDLES]# ./managevm.sh vms
    "id": "588dc831-d5c4-4edd-9925-7e34ef8d0af1"
      "TSM01"
    [root@localhost DNEEDLES]# ./managevm.sh flavors
    "id": "211675700dbcaf2327640c31b76b2112"
      "211675700dbcaf2327640c31b76b2112"
    "id": "2c710505-79f7-4021-b7f5-98e113c261d4"
      "powervm.tiny"
    "id": "35fccbcc466eb0351dc6da48b7eee6a0"
      "35fccbcc466eb0351dc6da48b7eee6a0"
    "id": "388b8d80-bc79-42e3-9aac-3a73b5c32024"
      "powervm.large"
    "id": "707c59e00f8dbe18eaf35cef094836a2"
      "707c59e00f8dbe18eaf35cef094836a2"
    "id": "75bf7b06-760f-400e-b25b-58be990bcf4c"
      "powervm.xxlarge"
    "id": "9017c674b0d3e57f425caccaecdd547e"
      "9017c674b0d3e57f425caccaecdd547e"
    "id": "bccddede2ae403586a5ce4857f737476"
      "bccddede2ae403586a5ce4857f737476"
    "id": "ce5b1b67-53b4-4f1f-8cd3-c834d0c616d5"
      "powervm.medium"
    "id": "def7aede-286b-4eb3-b12f-ed32201b5687"
      "powervm.xlarge"
    "id": "efa46d929e81d7371760ee2a639f5e28"
      "efa46d929e81d7371760ee2a639f5e28"
    "id": "f74113a9-4a31-48d9-b3d3-6535a6de8d9d"
      "powervm.small"

## ADD AN AIX VM:

    [root@localhost DNEEDLES]# ./managevm.sh add AIXtest AIX "2c710505-79f7-4021-b7f5-98e113c261d4"
    HTTP/1.1 202 Accepted
    Date: Fri, 19 May 2017 06:30:39 GMT
    Server: Apache
    Content-Length: 338
    Location: https://10.1.1.24:8774/v2/servers/d42c5b75-0f35-480b-8d56-a3ebbdbe35ed
    Content-Type: application/json
    X-Compute-Request-Id: req-96cd5373-ad55-46f6-a848-4f204c8c533d
    Cache-control: max-age=0, no-cache, no-store, must-revalidate
    Pragma: no-cache
        {"server": {"OS-DCF:diskConfig": "MANUAL", "id": "d42c5b75-0f35-480b-8d56-a3ebbdbe35ed", "links": [{"href": "https://10.1.1.24:8774/v2/servers/d42c5b75-0f35-480b-8d56-a3ebbdbe35ed", "rel": "self"}, {"href": "https://10.1.1.24:8774/servers/d42c5b75-0f35-480b-8d56-a3ebbdbe35ed", "rel": "bookmark"}], "adminPass"

## ADD A RHELbe VM:

    [root@localhost DNEEDLES]# ./managevm.sh add RHELbeTest RHELbe
    HTTP/1.1 202 Accepted
    Date: Fri, 19 May 2017 06:39:03 GMT
    Server: Apache
    Content-Length: 338
    Location: https://10.1.1.24:8774/v2/servers/abd30328-c712-4946-afd0-2512c1cae7e4
    Content-Type: application/json
    X-Compute-Request-Id: req-b7bc1bca-ab57-487d-9013-a1da9b985af4
    Cache-control: max-age=0, no-cache, no-store, must-revalidate
    Pragma: no-cache
    {"server": {"OS-DCF:diskConfig": "MANUAL", "id": "abd30328-c712-4946-afd0-2512c1cae7e4", "links": [{"href": "https://10.1.1.24:8774/v2/servers/abd30328-c712-4946-afd0-2512c1cae7e4", "rel": "self"}, {"href": "https://10.1.1.24:8774/servers/abd30328-c712-4946-afd0-2512c1cae7e4", "rel": "bookmark"}], "adminPass": "fishhead"}}[root@localhost DNEEDLES]#

## ADD A RHELbl VM:

    [root@localhost DNEEDLES]# ./managevm.sh add RHELbltest RHELbl
    HTTP/1.1 202 Accepted
    Date: Fri, 19 May 2017 06:40:37 GMT
    Server: Apache
    Content-Length: 338
    Location: https://10.1.1.24:8774/v2/servers/e87751bc-7615-4a2c-a705-16a9b94654c1
    Content-Type: application/json
    X-Compute-Request-Id: req-be748aa1-30c8-4cb6-b9de-b0e366f45313
    Cache-control: max-age=0, no-cache, no-store, must-revalidate
    Pragma: no-cache
    {"server": {"OS-DCF:diskConfig": "MANUAL", "id": "e87751bc-7615-4a2c-a705-16a9b94654c1", "links": [{"href": "https://10.0.0.24:8774/v2/servers/e87751bc-7615-4a2c-a705-16a9b94654c1", "rel": "self"}, {"href": "https://10.0.0.24:8774/servers/e87751bc-7615-4a2c-a705-16a9b94654c1", "rel": "bookmark"}], "adminPass": "fishhead"}}[root@localhost DNEEDLES]#

## LIST TO SHOW VMS:

    [root@localhost DNEEDLES]# ./managevm.sh vms
    "id": "e87751bc-7615-4a2c-a705-16a9b94654c1"
      "RHELbltest"
    "id": "abd30328-c712-4946-afd0-2512c1cae7e4"
      "RHELbeTest"
    "id": "d42c5b75-0f35-480b-8d56-a3ebbdbe35ed"
      "AIXtest"
    "id": "588dc831-d5c4-4edd-9925-7e34ef8d0af1"
      "TSM01"
