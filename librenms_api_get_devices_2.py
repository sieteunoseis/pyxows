#!/usr/bin/python

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dynamic Ansible Inventory based on LibreNMS API access.
"""

#######################################################################
#                                                                     #
# This script has been superseded by:                                 #
#                                                                     #
#        https://github.com/tkjaer/ansible-dynamic-inventory          #
#                                                                     #
#######################################################################

import requests
import json
import re

headers = {
		'X-Auth-Token': '984711fdc0f7c9d86aa38585db979373',
		}

r = requests.get('http://170.2.96.200/api/v0/devices', headers=headers)
librenms_devices = json.loads(r.text)

# Create the basic inventory structure.
# - http://docs.ansible.com/ansible/devel/dev_guide/developing_inventory.html
ansible_inventory = {
		"_meta": {
			"hostvars": {},
			},
		"all": {
			"children": [
				"ungrouped",
				]
			},
		"ungrouped": {},
		}

for device in librenms_devices['devices']:
	# Get the devices type, based on the internal Naming Scheme
	# - https://XXXXXXXXXX/plugin/p=Namingscheme
	device_type = re.match("^([a-zA-Z]*).*", device['hostname']).group(1)
	try:
		if (ansible_inventory[device_type]):
			pass
	except KeyError:
		ansible_inventory[device_type] = {
				'hosts': [],
					'vars': {
						   #'ansible_connection': 'local',
						   'connection': 'network_cli',
						}
				}
		ansible_inventory['all']['children'].append('device_type')

	hostname = device['hostname']
	ansible_inventory[device_type]['hosts'].append(hostname)
	ansible_inventory['_meta']['hostvars'][hostname] = {
		'sysname': device['sysName'],
		'hardware': device['hardware'],
		'location': device['location_id'],
		'type': device['type'],
		'ansible_network_os': device['os'],
		}

print(ansible_inventory)