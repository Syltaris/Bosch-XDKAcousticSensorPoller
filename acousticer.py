#!/usr/bin/env python

import web
import requests
import json
import time
import threading

from math import log1p
from restful_lib import Connection

#network calls
base_url_XDK = "http://boschxdk.southeastasia.cloudapp.azure.com:8082/v1/ctl/"
base_url_CrowdedMah = "http://boschenlighten.herokuapp.com/"
urls_XDK = (
    'boschxdk02/messages'
)
url_CrowdedMah = 'updateNoise'


conn_XDK = Connection(base_url_XDK)
conn_CrowdedMah = Connection(base_url_CrowdedMah)


#instantiated classes
JEncoder = json.JSONEncoder()

def fetch_data():
	#GET data and parse as JSON
	resp = conn_XDK.request_get(urls_XDK, args={}, headers={'content-type':'application/json', 'accept':'application/json'})
	status = resp[u'headers']['status']
	# check that we either got a successful response (200) or a previously retrieved, but still valid response (304)
	if status == '200' or status == '304':
		return json.loads(resp[u'body'])

	else:
	    print 'Error status code: ', status
	    return False

def update_noise(noiseLvl):
	#GET data and parse as JSON
	#request_post(self, resource, args = None, body = None, filename=None, headers={}):
	noiseLevel = JEncoder.encode(noiseLvl)
	resp = conn_CrowdedMah.request_post('updateNoise', args={}, body={noiseLevel}, filename={}, headers={'content-type':'application/json', 'accept':'application/json'})
	status = resp[u'headers']['status']
	if status == '200' or status == '304' :
		print 'Noise data is sent successfully.'
	else:
		print 'Error in sending data'

#compute ln(noiselevel)
def sample_noise():
	threading.Timer(5, sample_noise).start()

	# xdk_data = fetch_data()
	# if xdk_data != False:
	# 	noiseLvl = log1p(xdk_data['noiselevel'])
	# 	currTime = time.asctime(time.localtime(time.time()))
	# 	print currTime, noiseLvl

	noiseLvl = 8.0;
	#push to boschenlighten heroku app
	update_noise(noiseLvl)
	# else:
	# 	print 'Fetch error!'

sample_noise()
	