# PAPAYA Privacy-preserving Arrhythmia Classifier

This work is implemented under the scope of H2020 PlAtform for PrivAcY-preserving data Analytics (PAPAYA) project and the full version of this work is presented by Mohamad MANSOURI, Beyza BOZDEMIR, Melek ÖNEN, and Orhan ERMIS in [FPS 2019](https://fps2019.sciencesconf.org/), 12th International Symposium on Foundations and Practice of Security, November 5-7, 2019, Toulouse, France / Also published in LNCS, Vol. 12056.

PAC is a privacy-preserving neural network classifier based on secure two-party computation designed for classifying heart arrhythmia. This repository consists of two docker containers as entities of the secure two party computation, namely the client and server, and the signals files obtained from [MIT-BIH Arrhythmia Database](https://www.physionet.org/content/mitdb/1.0.0/) and preprocessed for the proposed solution.

# Instructions to run the project

Issue the following commands to build and run the containers:

## Server-side Component:
```
cd ppnn-2pc-server
sudo docker build -t ppnn-2pc-server: latest .
sudo docker run -p 5555:5000 -v /$PWD:/home -it ppnn-2pc-server
```

## Client-side Component:
```
cd ppnn-2pc-client
sudo docker build -t ppnn-2pc-client: latest .
sudo docker run --env-file env-file -p 6000:5000 -v /$PWD:/home -it ppnn-2pc-client
```
Open a 3rd terminal window and type the following commands to run the classifier:

```
cd signals/mit-bih-processed-signals/signals/
curl -F 'file=@[nameofthefile.extension]' http://0.0.0.0:6000/classify/
```

For quick tests, you can use sample files under **signals/mit-bih-processed-signals/** directory


