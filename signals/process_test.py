from flask import Flask, jsonify, request
import requests
import urllib 
from urllib.request import urlopen
import json
import os
import threading
import time as sleeptime
from datetime import datetime

def process_input():
	filename ="pimcatcher_pimcatcher_scripts_100.txt"
	line_counter = 0
	for line in open(filename):
		ldata = (line.split())
		with open("signal"+str(line_counter+1) ,'w') as wfile:
			for i in range(0, len(ldata)):
				print (ldata[i])
				if ldata[i] not in ("", "\n"):
					wfile.write("%f " % float(ldata[i]))
		wfile.close()
		line_counter += 1


process_input()