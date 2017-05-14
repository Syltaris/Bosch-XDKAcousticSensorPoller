#!/usr/bin/env python

import web
import requests
import json
import time
import threading

from math import log1p
from restful_lib import Connection

#no. of samples to get normalizing factor
INIT_SAMPLES = 10
#seconds to poll from XDK azure server
SAMPLING_PERIOD = 3
#no. of samples to take before sending result
SAMPLE_COUNT = 15

#network calls
base_url_XDK = 'http://boschxdk.southeastasia.cloudapp.azure.com:8082/v1/ctl/boschxdk02/messages'
base_url_CrowdedMah = 'http://crowdedmah.herokuapp.com/updateNoise'

def fetch_data():
	#GET data and parse as JSON
	XDK_GET = requests.get(base_url_XDK)
	if XDK_GET.status_code == 406 or XDK_GET.status_code == 404 or XDK_GET.text == '':
		return False
	else:
		return XDK_GET.json()

#post calculated noise levels to CrowdedMah app
def update_noise(noiseLvl):
	#GET data and parse as JSON
	#request_post(self, resource, args = None, body = None, filename=None, headers={}):
	payload = {'mag': int(noiseLvl)}
	CrowdedMah_POST = requests.post(base_url_CrowdedMah, data=payload)
	print CrowdedMah_POST.status_code
	
#compute ln(noiselevel/normalizingFactor)
def sample_noise(normalizingFactor):
	# threading.Timer(SAMPLING_PERIOD, sample_noise).start()
	sampleCount = 0
	noiseLevel_list = []

	while True:
		try:
			xdk_data = fetch_data()

			if xdk_data != False:
				noiseLvl = xdk_data['noiselevel']
				currTime = time.asctime(time.localtime(time.time()))
				noiseLevel_list.append(noiseLvl)
				print sampleCount+1, currTime, noiseLvl

				sampleCount += 1

				time.sleep(5)
			else:
				print 'Fetch error!'
				time.sleep(1)


			#calculate aggregated noise level average
			if sampleCount >= SAMPLE_COUNT:

				noiseLevel_list.sort
				aggregatedNoiseLevel = 0

				#samples around 90% of the readings
				for x in xrange(0, SAMPLE_COUNT*9/10): 
					aggregatedNoiseLevel += noiseLevel_list[x]

				noiseLvl = log1p(aggregatedNoiseLevel/(SAMPLE_COUNT*9/10 * normalizingFactor)) + 1
				print(noiseLvl)

				#check if within 1 to 5 
				if noiseLvl > 5:
					noiseLvl = 5
				elif noiseLvl < 1:
					noiseLvl = 1

				#push to boschenlighten heroku app
				update_noise(noiseLvl)

				sampleCount = 0 #reset counter
				noiseLevel_list =[] #clear list of aggregated noise levels
		except Exception:
			pass


#main execution
initTime = 0
initSampleCount = 0
sampleCount = 0
normalizingFactor = 0

print 'CALIBRATING! Will take approx.', INIT_SAMPLES*SAMPLING_PERIOD, 'secs'
while (initSampleCount < INIT_SAMPLES):
	xdk_data = fetch_data()
	if xdk_data != False:
		normalizingFactor += xdk_data['noiselevel']
		initTime = time.time()
		print 'Calculating normalizing factor...',xdk_data['noiselevel']
		initSampleCount += 1
		time.sleep(SAMPLING_PERIOD)
	else:
		print 'Fetch error!'

normalizingFactor = normalizingFactor/INIT_SAMPLES
print 'Avg. Noise:', normalizingFactor

sample_noise(normalizingFactor)
	