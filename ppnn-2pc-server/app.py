from flask import Flask, jsonify, request
import os
from os import listdir
from os.path import isfile, join
import threading

HOST = '0.0.0.0'
HTTP_PORT = 5555
TCP_PORT = 9999

UPLOAD_DIRECTORY = '/app/config_files'
app = Flask(__name__)

@app.route('/classify/<noofsignals>/', methods=['GET', 'POST'])
def classify(noofsignals):
	print ("test")
	print ('cd 2pc_model_quantized_batches/ && ./server -a ' + HOST + ' -p '+str(TCP_PORT)+ ' -i ' + noofsignals)
	# For local tests
	#os.system('cd 2pc_model_quantized_batches/ && ./server -a 172.17.0.2 -p '+str(TCP_PORT)+ ' -i ' + noofsignals)
	# IBM Cloud version
	os.system('cd 2pc_model_quantized_batches/ && ./server -a ' + HOST + ' -p '+str(TCP_PORT)+ ' -i ' + noofsignals)
	# t = threading.Thread(target = run_2pc_server, args = (local_ip,))
	return jsonify({'message': '2pc server has just been started!'})


@app.route('/kill', methods=['GET','POST'])
def killp():
	os.system('pkill server')
	return jsonify({'message': 'Process killed'})
if __name__ == '__main__':
	app.run(debug=True,host=HOST, port=HTTP_PORT)