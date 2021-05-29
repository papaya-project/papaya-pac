from flask import Flask, jsonify, request
import requests
from urllib.request import urlopen
import json
import os
import threading
import time as sleeptime
from datetime import datetime
import subprocess
import pickle
import numpy as np
from flask import make_response

app = Flask(__name__)

@app.route('/<ip_server>/<url>/<port>/', methods=['GET','POST'])
@app.route('/init/<ip_server>/<url>/<port>/', methods=['GET','POST'])
def init(ip_server, url, port):
    # print ("test")

    try:
        with open('/app/config/server_ip', 'w') as writeIPS:
            writeIPS.write(ip_server)
        writeIPS.close()
        with open('/app/config/server_port', 'w') as writeIPS:
            writeIPS.write(port)
        writeIPS.close()
        with open('/app/config/server_url', 'w') as writeIPS:
            writeIPS.write(url)
        writeIPS.close()
    except:
        return jsonify({'error':"Server configuration is missing"})
        
    return jsonify({'message':'Server\'s IP address and TCP port have been successfully stored!'})


def poke_server():
    os.system("curl http://172.17.0.1:5555/classify/")

def load_obj(name):
    with open("/app/"+name + '.pkl', 'rb') as f:
        return pickle.load(f)

@app.route('/classify/', methods=['GET','POST'])
def classify():
    
    server_ip = ""
    server_url = ""
    server_port = ""

    try:
        file = request.files["file"]
        file.save(os.path.join('/app/2pc_model_quantized_batches/input/input_files', file.filename))
    except:
        return make_response(jsonify({'error': 'Input file not found!'}), 409)
    
    try:
       for variable, value in os.environ.items():
        if variable == "SERVER_URL":
            server_url=value
        if variable == "SERVER_IP":
            server_ip = value
        if variable == "SERVER_TCP_PORT":
            server_port = value
    except:
        return make_response(jsonify({'error':"Incorrect or missing configuration file"}), 409)

    if server_url == "" or server_ip == "" or server_port == "":
        return make_response(jsonify({'error':"Incorrect or missing configuration file"}), 409)       
        
    reset() 
    # try:
    #     with open('/app/config/server_ip', 'r') as writeIPS:
    #         server_ip = writeIPS.read()
    #     writeIPS.close()
    #     with open('/app/config/server_port', 'r') as writeIPS:
    #         server_port = writeIPS.read()
    #     writeIPS.close()
    #     with open('/app/config/server_url', 'r') as writeIPS:
    #         server_url = writeIPS.read()
    #     writeIPS.close()
    # except:
    #     return jsonify({'error':"Server configuration is missing"})
    

    if os.path.exists("2pc_model_quantized_batches/input/signal_pca/"):
        os.system("rm -r 2pc_model_quantized_batches/input/signal_pca/")
    os.system("cd 2pc_model_quantized_batches/input/ && mkdir signal_pca/")
    output = subprocess.check_output("cat 2pc_model_quantized_batches/input/input_files/"+file.filename+" | wc -l", shell=True)
    datalength=int(output.decode("utf-8").strip())
    option=200
    now = datetime.now()
    execution_time = now.strftime("%m-%d-%Y__%H_%M_%S")
    '''PCA Version'''

    pca = load_obj("PCA")
    for j in range(0,datalength,option):
        line_counter = 0
        try:
            with open('/app/2pc_model_quantized_batches/input/input_files/'+file.filename) as f:
                lines = f.readlines()
                os.system("rm -r '/app/2pc_model_quantized_batches/input/input_files/*")
                for position, line in enumerate(lines):
                    if (position>=j and position<j+option):
                        ldata = [float(x) for x in line.split() if x not in ("", "\n")]
                        array_np = np.array(ldata).reshape(1,-1)
                        signal_pca = pca.transform(array_np)[0]
                        with open("2pc_model_quantized_batches/input/signal_pca/signal"+str(line_counter+1) ,'w') as wfile:

                            for i in range(0, len(signal_pca)):
                                if signal_pca[i] not in ("", "\n"):
                                    wfile.write("%f " % signal_pca[i])
                        wfile.close()
                        line_counter += 1

        except Exception as e:
            return jsonify({'error':"Incorrect input file format! "+str(e)})

    # for j in range(0,datalength,option):
    #     line_counter = 0
    #     try:
    #         with open('/app/2pc_model_quantized_batches/input/input_files/'+file.filename) as f:
    #             lines = f.readlines()
    #             os.system("rm -r '/app/2pc_model_quantized_batches/input/input_files/*")
    #             for position, line in enumerate(lines):
    #                 if (position>=j and position<j+option):
    #                     ldata = (line.split())
    #                     with open("2pc_model_quantized_batches/input/signal_pca/" + "signal"+str(line_counter+1) ,'w') as wfile:
    #                         for i in range(0, len(ldata)):
    #                             if ldata[i] not in ("", "\n"):
    #                                 wfile.write("%f " % float(ldata[i]))
    #                     wfile.close()
    #                     line_counter += 1

    #     except:
    #         return jsonify({'error':"Incorrect input file format!"})




    # url = 'http://0.0.0.0:8000/classify/'
    # PARAMS = None
    # print ("send request")
    # response = requests.get(url, params=PARAMS
    # return response.json()
    # t = threading.Thread(target=poke_server, args=())
    # os.system("nohup curl http://172.17.0.3:5000/classify/ &")



    # Local test
    #os.system("nohup curl http://172.17.0.2:5555/classify/"+ str(line_counter)+"/ &")
    #os.system("cd results/ && touch result_" + execution_time + ".txt")
    
    # IBM Cloud commands 
        
        # print ("nohup curl http"+param+"://"+server_url+"/classify/"+ str(line_counter)+"/ &", flush=True)
        try:
            requests.post(server_url+'/classify/'+ str(line_counter)+"/", timeout=0.1)
        except:     
            pass
        # os.system('nohup curl http'+param+'://'+server_url+'/classify/'+ str(line_counter)+'/ &')
        

    # Hardcoded IBM Cloud test -- url should be updated after each deployment
    # # os.system("nohup curl --insecure https://f2aa71.papaya.eu-de.containers.appdomain.cloud/classify/"+ str(line_counter)+"/ &")

    
        print (server_ip, flush=True)
        #sleeptime.sleep(1)
        print ('cd 2pc_model_quantized_batches/ && ./client -a ' + str(server_ip) + ' -p ' + server_port + ' -i ' + str(line_counter))
        os.system('cd 2pc_model_quantized_batches/ && ./client -a ' + str(server_ip) + ' -p ' + server_port + ' -i ' + str(line_counter) + ' >> ../result_' + execution_time + '.txt')
        
    #sleeptime.sleep(5)
    counter = 0
    results = []
    
    while not os.path.exists("result_" + execution_time + ".txt"):
        sleeptime.sleep(2)
    with open("result_" + execution_time + ".txt" ,'r') as file:
        for line in file:
            if line.find(" : ") > 0:
                line = line.split(" : ")
                results.append(line[1].replace('\n', ''))
                counter += 1

    return jsonify({'results':", ".join(results)})

@app.route('/reset/', methods=['GET','POST'])
def reset():
    server_ip = ""
    server_url = ""
    server_port = ""
    
    try:
       for variable, value in os.environ.items():
        if variable == "SERVER_URL":
            server_url=value
            break
    except:
        return jsonify({'error':"Incorrect configuration file"})
    requests.post(server_url+'/kill', timeout=0.1)
    # os.system('nohup curl http'+param+'://'+server_url+'/kill')
    killp()
    return jsonify({'message': 'Reset Done'})

@app.route('/kill', methods=['GET','POST'])
def killp():
    os.system('pkill client')
    return jsonify({'message': 'Process killed'})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')