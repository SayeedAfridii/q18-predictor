# Q18 Arrival Predictor

A tool that predicts when the MTA Q18 bus in Queens will actually arrive at a stop.

It pulls live bus data from the MTA Bus Time API every 60 seconds: each bus's location, direction, next stop, distance to that stop, and the MTA's own expected arrival time.

The goal is to train a model that predicts arrival times more accurately than the MTA's estimated ETA.s