# Bosch-XDKAcousticSensorPoller

This python script is developed for the Bosch IoT 'Buildings of Tomorrow' Hackathon held at Blk 71 Singapore on May 13-14. The sole purpose of this script is to GET the data from the MS Azure server, which contains data from the sensor values periodically updated by the Bosch XDK devices. It then calculates the noise level of the ambience surrounding the device, using a normalizing value (calculated during the calibration phase at the start) to normalize the noise level before POST-ing it to a front-end Web API hosted on Heroku.
