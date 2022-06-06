import os
import numpy as np
from power_density_average import *
from phase_average import *
from mean_velocity import *
from budget import *
from smooth_FFT import *

#parameters
#Declare some variable 
nturbinex = 4
nturbiney = 4
nturbine = 16
#Diameter of turbine
D = 80
#Other variable
Sx = 7
Sy = 7
#kappa = 0.4
#nu = 1.511e-5
#PEX = 1.45444104333
#PEY = 8.72664625997
#hbar = 0.46
#uinfty = 2.54390548295
#dt = 0.2941315855
#dt = 0.68543297937
#dt = 0.461442495048675
dt = 0.3150659270689523
#Rotational angular period
T_turb = 42.84
T_wave = 126.02637082768938 
#T_wave = 14.7065792758511
#U_star = 0.356
H_hub = 70
#Mean finite velocity
U = 11.5258407161
U_star = 0.421
tis = 100
tie = 15000
tii = 100
nti = int((tie - tis) / tii + 1)
NPX = 192
NPY = 192
NPZ = 65
s =1   #number of sampling windows
path  = 'd:\post'
#path  = 'd:\post'
os.chdir(path)
#delare working casename
#casenames = ["Fixed_Turbine","Pitch_Turbine","SWAY_Turbine","fixed_no_swell"]
casenames = ["Test"]
unametags = ["U", "UI", "UI"]
casename_s = 0
casename_e = 1

time = get_time(path+"./"+casenames[casename_s],nturbine,T_wave)
print(len(time))
#data = np.zeros((len(time[-15000:]),int(casename_e-casename_s+1)))
data = np.zeros((len(time),int(casename_e-casename_s+1)))
data1 =  np.zeros((NPZ,7*int(casename_e-casename_s+1)))
#data2 = np.zeros((int(len(time[-15000:])/s),int(casename_e-casename_s+1)))
data2 = np.zeros((int(len(time)/s),int(casename_e-casename_s+1)))
#data [:,0] = time[-15000:]
data [:,0] = time
#N = len(time[-15000:])/s
N = len(time)/s
n = np.arange(N)
#data2[:,0] = n/time[int(14999/s)]
data2[:,0] = n/time
for icase in range(casename_s, casename_e):
    foldername = "./"+casenames[icase]
    #change working directory
    #os.chdir(path+foldername)

    #create dynamic variables
   
    globals()["{casenames[icase]}"] = power_density_average\
                                        (path+foldername,nturbine,dt,Sx,Sy,D)
#    globals()["Pmean_{casenames[icase]}"] = globals()["{casenames[icase]}"][-15000:].mean()
    globals()["Pmean_{casenames[icase]}"] = globals()["{casenames[icase]}"].mean()
#    globals()["Pshift_{casenames[icase]}"] = globals()["{casenames[icase]}"][-15000:]-\
#                                            globals()["Pmean_{casenames[icase]}"]
    globals()["Pshift_{casenames[icase]}"] = globals()["{casenames[icase]}"]-\
                                            globals()["Pmean_{casenames[icase]}"]                                        
  
#    globals()["reshape_"+casenames[icase]] = globals()["Pshift_{casenames[icase]}"]\
#                                            .reshape(s,int(len(time[-15000:])/s))
    globals()["reshape_"+casenames[icase]] = globals()["Pshift_{casenames[icase]}"]\
                                            .reshape(s,int(len(time)/s))                                        
    globals()["FFT_"+casenames[icase]] = np.copy(globals()["reshape_"+casenames[icase]])                                    
    for i in range(s):
        globals()["FFT_"+casenames[icase]][i,:] = np.absolute\
                                (smooth_FFT(globals()["reshape_"+casenames[icase]][i,:]))
    globals()["FFTmean_"+casenames[icase]] = np.mean(globals()["FFT_"+casenames[icase]],axis=0)
                                        
#    globals()["umean_{casenames[icase]}"] = get_mean_velocity\
#                                        (path+foldername,tis,tie,tii)*U
#    globals()["z_{casenames[icase]}"] = get_z_coordinate\
#                                        (path+foldername,tis)/H_hub
#    globals()["mkeb_wt_{casenames[icase]}"] = get_mkeb_wt\
#                                        (path+foldername,NPZ)
#    globals()["tau_sum_{casenames[icase]}"] = get_tau_sum\
#                                        (path+foldername,NPZ)
#    globals()["um_{casenames[icase]}"] = get_um\
#                                        (path+foldername,NPZ)                   

    #checked
    print(os.getcwd())
    print(len(globals()["{casenames[icase]}"]))        
#    data[:, int(icase+1)] = globals()["{casenames[icase]}"][15000:]
    data[:, int(icase+1)] = globals()["Pshift_{casenames[icase]}"]
    


    
#    data1[:, 7*int(icase):7*int(icase)+3] = globals()["umean_{casenames[icase]}"]
#    data1[:, 7*int(icase)+3] = globals()["z_{casenames[icase]}"]
#    data1[:, 7*int(icase)+4] = globals()["mkeb_wt_{casenames[icase]}"]
#    data1[:, 7*int(icase)+5] = globals()["tau_sum_{casenames[icase]}"]
#    data1[:, 7*int(icase)+6] = globals()["um_{casenames[icase]}"]

    data2[:, int(icase+1)] = globals()["FFTmean_"+casenames[icase]]

os.chdir('d:\post')
outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
print("Current working directory is: {0}".format(os.getcwd()))

f = open( outputfolder + "Power average_mean.plt",'w')

f.write("VARIABLES = t/T," + str(casenames).replace("'","")\
        .replace("[","").replace("]","")+ "\n")
np.savetxt(f, data)
f.close()
'''
f1 = open( outputfolder + "Budget average.plt",'w')
f1.write("VARIABLES = Z/H_fixed, <U>_fixed, <V>_fixed, <W>_fixed, mkeb_wt_fixed, tau_sum_fixed,um_fixed,\
                    Z/H_pitch, <U>_pitch, <V>_pitch, <W>_pitch, mkeb_wt_pitch, tau_sum_pitch,um_pitch,\
                    Z/H_sway, <U>_sway, <V>_sway, <W>_sway, mkeb_wt_sway, tau_sum_sway,um_sway \n")    
                            
np.savetxt(f1, data1)
f1.close()
'''
f2 = open( outputfolder + "Power average_FFTmean.plt",'w')
f2.write("VARIABLES = freq," + str(casenames).replace("'","")\
        .replace("[","").replace("]","")+ "\n")
np.savetxt(f2, data2)

data1 = get_phi(path+"./Pitch_DT031"+'\POST_U_2D3_0001', 1, 15300, 30000, 400, NPZ, NPX,U,U_star)
data2 = get_phi(path+"./Pitch_DT031"+'\POST_U_2D3_0002', 2, 15300, 30000, 400, NPZ, NPX,U,U_star)
data3 = get_phi(path+"./Pitch_DT031"+'\POST_U_2D3_0003', 3, 15300, 30000, 400, NPZ, NPX,U,U_star)
data4 = get_phi(path+"./Pitch_DT031"+'\POST_U_2D3_0004', 4, 15300, 30000, 400, NPZ, NPX,U,U_star)
#aveage data
data = np.zeros([NPZ*48, 10])
data = (data1 + data2 + data3 + data4)/4

os.chdir('d:\post')
outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
f = open('d:\post' + './'+ outputfolder + casenames[0]+ "_phase3_contour.plt",'w')
f.write("VARIABLES = X, Z, <U>/U*, <V>/U*, <W>/W*, UU/U*^2, VV/U*^2,\
         WW/U*^2, UW/U*^2, tke_tm  \n")

np.savetxt(f, data)
f.close()

data1 = time_average(path+"./Pitch_DT031"+'\POST_UI_2D3_0001', 1, 15000, 30000, 100, NPZ, NPX,U,U_star)
data2 = time_average(path+"./Pitch_DT031"+'\POST_UI_2D3_0002', 2, 15000, 30000, 100, NPZ, NPX,U,U_star)
data3 = time_average(path+"./Pitch_DT031"+'\POST_UI_2D3_0003', 3, 15000, 30000, 100, NPZ, NPX,U,U_star)
data4 = time_average(path+"./Pitch_DT031"+'\POST_UI_2D3_0004', 4, 15000, 30000, 100, NPZ, NPX,U,U_star)
#aveage data
data = np.zeros([NPZ*48, 10])
data = (data1 + data2 + data3 + data4)/4

os.chdir('d:\post')
outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
f1 = open('d:\post' + './'+ outputfolder + casenames[0]+ "_time_ave_contour.plt",'w')
f1.write("VARIABLES = X, Z, <U>/U*, <V>/U*, <W>/W*, UU/U*^2, VV/U*^2,\
         WW/U*^2, UW/U*^2, tke_tm  \n")

np.savetxt(f1, data)
f1.close()
'''
dat = np.zeros((NPZ,7))
dat[:,0] = get_z_coordinate(path+foldername,tis)/H_hub
dat[:,1:4] = (get_mean_velocity(path+foldername,tis,tie,tii)*U)#/U_star
dat[:,4] = get_mkeb_wt(path+foldername,NPZ)
dat[:,5] = get_tau_sum(path+foldername,NPZ)
dat[:,6] = get_um(path+foldername,NPZ)

f1 = open( 'd:\post'+'./' + outputfolder + './' + casenames[0]+"_budget_test.plt",'w')
f1.write("VARIABLES = Z/H, <U>, <V>, <W>, mkeb_wt, tau_sum,um \n")
         
np.savetxt(f1, dat)
f1.close()
'''
print("End process directory: {0}".format(os.getcwd()) )
