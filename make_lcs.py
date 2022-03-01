#!/usr/bin/env python3

import os
import numpy as np
import sncosmo
from scipy.signal import savgol_filter
import argparse
from scipy.interpolate import interpolate as interp

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filters',type=str,default='sdss::u,sdss::g,sdss::r,sdss::i,sdss::z,swope2::y,swope2::J,swope2::H,cspk',
    help='comma-separated list of filters for photometric lcs; must be from the bandpasses listed here: \
    https://sncosmo.readthedocs.io/en/stable/bandpass-list.html')
    parser.add_argument('--modeldir',type=str,help='directory where .txt files are located',default='model/')
    parser.add_argument('--lcdir',type=str,help='output directory for generated lightcurves',default='lcs/')
    parser.add_argument('--doLbol',help='extract bolometric lightcurves',action="store_true",default=False)
    parser.add_argument('--doAB',help='extract photometric lightcurves',action="store_true",default=False)
    parser.add_argument('--doSmoothing',help='Employ Savitzky-Golay filter for smoothing',action="store_true",default=False)
    parser.add_argument('--dMpc',type=float,help='distance in Mpc, default is 10 pc to get lightcurves in Absolute Mag',default=1e-5)

    return parser.parse_args()

args = parse()

filters = args.filters.split(',')
lcdir = args.lcdir
if not os.path.isdir(lcdir): os.makedirs(lcdir)
if not args.doAB and not args.doLbol:
    raise SystemExit('ERROR: Neither --doAB nor --doLbol are enabled. Please enable at least one.')

files = [f for f in os.listdir(args.modeldir) if 'txt' in f]
numfiles = len(files)

dMpc = args.dMpc
D_cm = 10*3.0857e16*100 # 10 pc in cm
H0 = 73
CLIGHT = 2.99792458e5
z = H0 * dMpc / CLIGHT

for kk,filename in enumerate(files):
    if kk % 10 == 0: print(f'{kk * 100 / numfiles:.2f}% done')
    
    a = open(os.path.join(args.modeldir,filename))
    l=0
    for ii in a:
        if l==0:
            Nobs=int(ii)
        elif l==1:
            Nwave=int(ii)
        elif l==2:
            Ntime=int(ii.split()[0])
            ti = float(ii.split()[1])
            tf = float(ii.split()[2])
        l+=1

    step_time = (tf - ti) / float(Ntime);
    a = np.genfromtxt(os.path.join(args.modeldir,filename),skip_header=3)

    cos = np.linspace(0,1,Nobs)
    thetas = np.arccos(cos) * 180 / np.pi

    for obs,theta in enumerate(thetas):
        mall, fls, waves, ph = [],[],[],[]

        for ifilt in range(len(filters)):
            wave = a[Nwave*obs:Nwave*(obs+1),0] * (1+z)
            waves.append(wave)
            fl = np.ones((Ntime,len(wave)))
            
            for i in range(0,Ntime):
                
                if ifilt == 0:
                    time = ti + step_time * (i + 0.5)
                    ph.append(time)
                
                I = a[Nwave*obs:Nwave*(obs+1),1+i] * (1e-5/dMpc)**2
                fl[i] = I
            
            ph = np.array(ph)
            fls.append(fl)

        # extract photometric lightcurves
        if args.doAB:
            lc = open(os.path.join(lcdir,f'{filename[:-4]}_theta{theta:.2f}.dat'),'w')
            lc.write(f'# t[days] {" ".join(filters)} \n')
            m_tot = []
            
            for ifilt,filt in enumerate(filters):
                source = sncosmo.TimeSeriesSource(ph,waves[ifilt],fls[ifilt])
                m = source.bandmag(filters[ifilt],"ab",ph)
                
                # apply smoothing filter
                if args.doSmoothing:
                    ii = np.where(~np.isnan(m))[0]
                    if len(ii) > 1:
                        f = interp.interp1d(ph[ii], m[ii], fill_value='extrapolate')
                        m = f(ph)
                    m = savgol_filter(m,window_length=17,polyorder=3)

                m_tot.append(m)

            for i,t in enumerate(ph):
                lc.write(f'{t:.3f} ')
                for ifilt in range(len(filters)):
                    lc.write(f'{m_tot[ifilt][i]:.3f} ')
                lc.write('\n')
            lc.close()

        # extract bolometric lightcurves
        if args.doLbol:
            Lbol_f = open(os.path.join(lcdir,f'{filename[:-4]}_theta{theta:.2f}_Lbol.dat'),'w')
            Lbol_f.write('# t[days] Lbol[erg/s] \n')

            Lbol = np.trapz(fl*(4*np.pi*D_cm**2),x=wave)

            if args.doSmoothing:
                ii = np.where(np.isfinite(np.log10(Lbol)))[0]
                f = interp.interp1d(ph[ii], np.log10(Lbol[ii]), fill_value='extrapolate')
                Lbol = 10**f(ph)
                Lbol = savgol_filter(Lbol,window_length=17,polyorder=3)

            for i,t in enumerate(ph):
                Lbol_f.write(f'{t:.3f} {Lbol[i]:.5e} \n')

            Lbol_f.close()
