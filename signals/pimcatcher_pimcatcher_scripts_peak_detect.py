import os
import sys
import wfdb
from wfdb import processing
import shutil

def peaks_hr(sig, peak_inds, fs, title, figsize=(20, 10), saveto=None):
	"Plot a signal with its peaks and heart rate"
	# Calculate heart rate
	hrs = processing.compute_hr(sig_len=sig.shape[0], qrs_inds=peak_inds, fs=fs)
	print ("hours: %s", hrs)
	N = sig.shape[0]
	

file_list = []

for file in os.listdir("mit-bih"):
	if file.endswith(".dat"):
		file_list.append("mit-bih/"+file.replace(".dat", ""))

for data in file_list:
	print ("Processing patient: ", data)
	qrs_inds = []
	increment = 180
	while len(qrs_inds) == 0:
	# Load the wfdb record and the physical samples
		record = wfdb.rdrecord(data, channels=[0])
		# begin -= 100
		# if begin < 0:
		# 	begin = 0
		# end += increment
		# print ('begin-end', begin, end)
	#record = wfdb.rdrecord(data,sampfrom=0, sampto=len(data), channels=[0])
	# Use the gqrs algorithm to detect qrs locations in the first channel
	# print('signals', record.p_signal[:,0])
		qrs_inds = processing.gqrs_detect(sig=record.p_signal[:,0],  fs=record.fs)

	# print (qrs_inds)

	# Correct the peaks shifting them to local maxima
	min_bpm = 20
	max_bpm = 230
	#min_gap = record.fs * 60 / min_bpm
	# Use the maximum possible bpm as the search radius

	search_radius = int(record.fs * 60 / max_bpm)
	# print ('qrs_inds', qrs_inds)
	corrected_peak_inds = processing.correct_peaks(record.p_signal[:,0], peak_inds=qrs_inds, search_radius=search_radius, smooth_window_size=150)

	corrected_peak_inds= sorted(corrected_peak_inds)
	#print (type (corrected_peak_inds))
	#print (len(corrected_peak_inds))
	if os.path.exists(data+".txt"):
		os.remove(data+".txt")

	for indexOfpeak in range(len(corrected_peak_inds)):
		r=record.p_signal[corrected_peak_inds[indexOfpeak]-90:corrected_peak_inds[indexOfpeak]+90,0]
		
		with open(data+'.txt', 'a') as f:
			for item in r:
				f.write("%s "% item)
			f.write('\n')


