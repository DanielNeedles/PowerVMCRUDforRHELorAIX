#!/usr/bin/bash
######################################################################
# PROGRAM: testmanagevm.sh          Daniel Needles        05.30.2017 #
# PURPOSE: Test the managevm.sh program which has the usage:         #
#   managevm add (VMNAME) (AIX|RHELbe|RHELbl) [(FLAVOR ID) \         #
#                [{NETWORK ID)]] [debug]  ## USE ID, NOT NAME        #
#            remove (VM ID) [debug]                                  #
#            vms [debug]                                             #
#            flavors [debug]                                         #
#            networks [debug]                                        #
# SAMPLES (Used to determine these tests)                            #
#          ./betamanagevm.sh images
#              AIX72TL01SP01,47149635-026d-459e-8584-999f0743aca7
#              RHEL 7.2ppc64be,5d9e8bc3-ca17-4be3-8377-7ab8f3bfa122
#              RHEL 7.2ppc64le,e9212533-1ff2-40b8-9dad-19271fe143a1
#          ./managevm.sh vms
#              Test1,edb23e24-cdea-4f25-a105-ea720be97a8b
#              DanTestAIX,0e96f785-15fd-42d0-84b8-7a9c1ce62e67
#              AIXTest2,09df7e6b-86d6-4d52-91cc-66b30fc08e29
#              RHELblTest2,1a4e0f71-5d62-4da3-8ddf-0401f0462b19
#              RHELbeTest2,1dc693a6-3573-4a67-8b6d-a8024fb348e5
#              DanRHELbl,ee00e912-e945-45cd-9840-ea6c4289367d
#              DanAIX,671f29ea-625d-4fb5-85d4-34c92674b656
#              RHELbltest,e87751bc-7615-4a2c-a705-16a9b94654c1
#              RHELbeTest,abd30328-c712-4946-afd0-2512c1cae7e4
#              TSM01,588dc831-d5c4-4edd-9925-7e34ef8d0af1
#          ./managevm.sh flavors
#              211675700dbcaf2327640c31b76b2112,211675700dbcaf2327640c31b76b2112
#              powervm.tiny,2c710505-79f7-4021-b7f5-98e113c261d4
#              35fccbcc466eb0351dc6da48b7eee6a0,35fccbcc466eb0351dc6da48b7eee6a0
#              powervm.large,388b8d80-bc79-42e3-9aac-3a73b5c32024
#              707c59e00f8dbe18eaf35cef094836a2,707c59e00f8dbe18eaf35cef094836a2
#              powervm.xxlarge,75bf7b06-760f-400e-b25b-58be990bcf4c
#              9017c674b0d3e57f425caccaecdd547e,9017c674b0d3e57f425caccaecdd547e
#              bccddede2ae403586a5ce4857f737476,bccddede2ae403586a5ce4857f737476
#              powervm.medium,ce5b1b67-53b4-4f1f-8cd3-c834d0c616d5
#              powervm.xlarge,def7aede-286b-4eb3-b12f-ed32201b5687
#              efa46d929e81d7371760ee2a639f5e28,efa46d929e81d7371760ee2a639f5e28
#              powervm.small,f74113a9-4a31-48d9-b3d3-6535a6de8d9d
#          ./managevm.sh networks
#              CSRA_Public,bcb1fdae-3dad-4a52-8ece-f32418a8fd09
######################################################################
declare -a arr=(
  './managevm.sh vms' 
  './managevm.sh images' 
  './managevm.sh flavors' 
  './managevm.sh networks'
  './managevm.sh vms debug'
  './managevm.sh images debug' 
  './managevm.sh flavors debug' 
  './managevm.sh networks debug'
  './managevm.sh add testmanageAIX1 AIX72TL01SP01'
  './managevm.sh add testmanageRHELbe1 "RHEL 7.2ppc64be"'
  './managevm.sh add testmanageRHELle1 "RHEL 7.2ppc64le"'
  './managevm.sh add testmanageAIX2 AIX72TL01SP01 2c710505-79f7-4021-b7f5-98e113c261d4'
  './managevm.sh add testmanageRHELbe2 "RHEL 7.2ppc64be" powervm.tiny'
  './managevm.sh add testmanageRHELle2 "RHEL 7.2ppc64le" powervm.small'
  './managevm.sh add testmanageAIX3 AIX72TL01SP01 2c710505-79f7-4021-b7f5-98e113c261d4 bcb1fdae-3dad-4a52-8ece-f32418a8fd09'
  './managevm.sh add testmanageRHELbe3 "RHEL 7.2ppc64be" powervm.tiny bcb1fdae-3dad-4a52-8ece-f32418a8fd09'
  './managevm.sh add testmanageRHELle3 "RHEL 7.2ppc64le" powervm.small CSRA_Public'
  './managevm.sh vms' 
  './managevm.sh remove testmanageAIX1'
  './managevm.sh remove testmanageRHELbe1'
  './managevm.sh remove testmanageRHELle1'
  './managevm.sh remove testmanageAIX2'
  './managevm.sh remove testmanageRHELbe2'
  './managevm.sh remove testmanageRHELle2'
  './managevm.sh remove testmanageAIX3'
  './managevm.sh remove testmanageRHELbe3'
  './managevm.sh remove testmanageRHELle3'
  './managevm.sh vms' 
)

for i in "${arr[@]}"
do
  CNT=$(expr $CNT + 1)
  echo "################################################################################"
  echo "##  TEST NUMBER: $CNT  #########################################################"
  echo "##  $i  ##"
  echo "################################################################################"
  eval $i
  echo "################################################################################"
  echo "###############################  END TEST $CNT  ################################"
  echo "################################################################################"
  echo ""
  echo ""
  echo ""
  sleep 2
done
