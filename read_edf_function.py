'''
화면안에 들어갈 정보만 간추린 2차원배열
'''
import pyedflib
import numpy as np

def get_signal_data(EDF, playtime, timescale, channel_index):

	unit = EDF.getSampleFrequency(channel_index[0])
	if playtime - timescale/2 < 0:
		playtime = timescale/2

	scale_index_range = timescale*unit
	startpt = playtime*unit
	
	signal_data = []
	for i in channel_index:
		signal_data.append(EDF.readSignal(i,int(startpt),int(scale_index_range)))

	return signal_data