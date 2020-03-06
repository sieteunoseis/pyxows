#!/usr/bin/env python

import json
import urllib2


librenms = json.loads(
	urllib2.urlopen(urllib2.Request(
		'http://170.2.96.200/api/v0/devices',
		headers={'X-Auth-Token': '984711fdc0f7c9d86aa38585db979373'},
	)).read()
)

inventory = {
	"_meta": {
		"hostvars": {}
	},
	"all": [device['hostname'] for device in librenms['devices']],
	"seattle": [device['hostname'] for device in librenms['devices']],
}

for key in ('os', 'sysName', 'type', 'version'):
	for device in librenms['devices']:
		group = device.get(key)
		if not group:
			continue
		if not inventory.get(group):
			inventory[group] = []
		inventory[group].append(device['hostname'])

# converts the 'status' field to an 'available' list
inventory['available'] = [device['hostname'] for device in librenms['devices']
						  if int(device.get('status'))]

print json.dumps(inventory, indent=2)
 