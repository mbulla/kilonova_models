import numpy as np
import scipy as sp
from pylab import *
import os

dMpc = 1e-5

filename = []
for r, d, f in os.walk("./"):
    for file in f:
        if 'nph' in file:
            filename.append(os.path.join(r, file))

# Number of observers
for ifile in range(len(filename)):

	# New filename
	#split = filename[ifile].split("/")[1].split("_")
	#output = split[0]+"_"+split[1]+"_"+split[2]+"_"+split[3]+".txt"
	l=0

	output = filename[ifile]
	aa = open(output)
	for ii in aa:
		if l==0:
			Nobs=int(ii)
		elif l==1:
			Nwave=int(ii)
		elif l==2:
			Ntime=int(ii.split()[0])
			ti = double(ii.split()[1])
			tf = double(ii.split()[2])
		l+=1


	f = open(filename[ifile]+"_new.txt","w")

	f.write("%d \n"%Nobs)
	f.write("%d \n"%Nwave)
	f.write("%d %s %s \n"%(Ntime,ti,tf))

	step_time = (tf-ti) / double(Ntime)

	a = genfromtxt(filename[ifile],skip_header=3)

	for j in range(0,Nobs):

		w = a[Nwave*j:Nwave*(j+1),0]
		
		for iw in range(0,len(w)):
			
			f.write("%.3e "%w[iw])
			
			for i in range(0,Ntime):

				time = ti + step_time * (i + 0.5)
				I = a[Nwave*j:Nwave*(j+1),1+i*3] * (1./dMpc)**2

				f.write("%.4e "%I[iw])

			f.write("\n")

	os.remove(filename[ifile])
