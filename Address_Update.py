#!/usr/bin/python3

#Allow Helpdesk to update the address for the network device.

#imports
import requests
import json

#Private credentials file, used to make life easy when I deploy new scripts.
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key

#Main URL for the Meraki Platform
dashboard = "https://api.meraki.com/api/v0"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#variables for testing ***** Need to switch to an argument or something else
# make sure that when store is taken in it comes in with quotes single or double doesn't matter.
store = str(input("What store are we creating?: "))
address = input("What is the address for this store?: ")

#Pull the information from the Meraki cloud to get the network id
#pull back all of the networks for the organization
get_network_id_url = dashboard + '/organizations/%s/networks' % organization

#request the network data
get_network_id_response = requests.get(get_network_id_url, headers=headers)

#puts the data into json format
get_network_id_json = get_network_id_response.json()

#pull back the network_id of the store that you are configuring
for i in get_network_id_json:
    if i["name"] == str(store):
        network_id=(i["id"])

#Need to get s/n of of the device in that network
get_devicesn_url = dashboard + '/networks/%s/devices' % network_id

#requests the s/ns of the devices in the network
get_devicesn_response = requests.get(get_devicesn_url, headers=headers)

#put the data pulled back into json
get_devicesn_json = get_devicesn_response.json()

#Loop through the data looking for the MX
for x in get_devicesn_json:
    if x["model"] == "MX64W":
        serial_num = x['serial']

#Set the address for the device
update_address = dashboard + '/networks/%s/devices/%s' % (network_id, serial_num)

#Update the Address for the device and set the name, it also moves the mapmarker in the Meraki Portal
UPDATE_ADDRESS_JSON = {}
UPDATE_ADDRESS_JSON["name"] = store
UPDATE_ADDRESS_JSON["address"] = address
UPDATE_ADDRESS_JSON["moveMapMarker"] = "true"

get_update_address = requests.put(update_address, data=json.dumps(UPDATE_ADDRESS_JSON), headers=headers)
