import numpy as np

#dataid_201303 = np.load("stid_201303.npz")
#dataid_202111 = np.load("stid_202111.npz")
z13 = np.load("z13.npy", allow_pickle=True)
zfo = np.load("zfo.npy", allow_pickle=True)
zhm = np.load("zhm.npy", allow_pickle=True)
z21 = np.load("z21.npy", allow_pickle=True)
#data = np.load("cosmic2_2.npy")#
### Temp ###
#data2 = np.load("cosmic2_3.npy")
#data3 = np.load("cosmic2_4.npz")
##data4 = np.load("cosmic2_4.npy")
#data5 = np.load("cosmic2_5.npy")
#data6 = np.load("csmc2_tcp_foF2.npz")
#data7 = np.load("csmc2_tcp_hmF2.npz")
#data8 = np.load("HMF2_CTEC.npz")
#data8 = np.concatenate([[data8["arr_0"]], data8["arr_1"]])
    ### ###
    #if year=='2021': #If the selected storm ID is 2021, the appropriate data will be loaded
'''
pic=dataid_202111['arr_0'][0]
M_PE_diff = dataid_202111['arr_1'][0]
RP_par = dataid_202111['arr_2'][0]
MP_par = dataid_202111['arr_3'][0]
CC = dataid_202111['arr_4'][0]
Alldata = dataid_202111['arr_5'][0]
allphase = dataid_202111['arr_6'][0]
skillscore=dataid_202111['arr_7'][0]
All_nss=dataid_202111['arr_8'][0]
dstdata = np.load('dst_2021.npy')
#fig1=dstKp.dst_kp_plot(2021, index)


    #else: #For now, if 2021 is not selected the only other option will be 2013, thus else results in all the 2013 data being loaded
pic = dataid_201303['arr_0'][0]
M_PE_diff = dataid_201303['arr_1'][0]
RP_par = dataid_201303['arr_2'][0]
MP_par = dataid_201303['arr_3'][0]
CC = dataid_201303['arr_4'][0]
Alldata = dataid_201303['arr_5'][0]
allphase = dataid_201303['arr_6'][0]
skillscore=dataid_201303['arr_7'][0]
All_nss = dataid_201303['arr_8'][0]
'''
dst_2013 = np.load('./dst_2013.npy')
dst_2021 = np.load('./dst_2021.npy')
#fig1=dstKp.dst_kp_plot(2013, index)


#dataz = np.load("z.npy", allow_pickle=True)
#data = np.load("cosmic2_2.npy")#
### Temp ###
#data2 = np.load("cosmic2_3.npy")
data3 = np.load("./cosmic2_4.npz")
#data4 = np.load("cosmic2_4.npy")
#data5 = np.load("cosmic2_5.npy")
#data6 = np.load("csmc2_tcp_foF2.npz")
#data7 = np.load("csmc2_tcp_hmF2.npz")
#data8 = np.load("HMF2_CTEC.npz")
#data8 = np.concatenate([[data8["arr_0"]], data8["arr_1"]])
#data9 = np.load("DEPdatafiles/FOF2_CTEC.npz")
#data9 = np.concatenate([[data9["arr_0"]], data9["arr_1"]])
'''
c2_map_plot(data3['arr_0'], data3['arr_1'], data3['arr_2'])
rcpm_plot(np.load("csmc2_rcpm_foF2.npy")
fifth_Plot(np.load("csmc2_nSS_foF2.npy")
skill_scores_sum_plot(np.load("csmc2_tnSS_foF2.npy"),
tec_change_plot(data6['arr_0'], data6['arr_1'], data6['arr_2'],
rcpm_plot(np.load("csmc2_rcpm_hmF2.npy")
fifth_Plot(np.load("csmc2_nSS_hmF2.npy"),
skill_scores_sum_plot(np.load("csmc2_tnSS_hmF2.npy"),
tec_change_plot(data7['arr_0'], data7['arr_1'], data7['arr_2'], 
'''
#data10 = np.load('csmc2_tcp_foF2.npz')
#CC2 = data10['arr_0']
#RP_par2 = data10['arr_1']
#MP_par2 = data10['arr_2']
#data10 = np.load('csmc2_tcp_hmF2.npz')
#CC3 = data10['arr_0']
#RP_par3 = data10['arr_1']
#MP_par3 = data10['arr_2']
#Saving Data:
#np.savez("foF2_202111_storm", C2_foF2_map=data9["arr_0"],All_model_fof2=data9["arr_1"], RP_par=RP_par2, MP_par=MP_par2,CC=CC2, Alldata=np.load("csmc2_rcpm_foF2.npy"), allphase=np.load('csmc2_nSS_foF2.npy'), All_nss=np.load('csmc2_tnSS_foF2.npy'))
#np.savez("hmF2_202111_storm", C2_hmF2_map=data8["arr_0"],All_model_hmf2=data8["arr_1"], RP_par=RP_par3, MP_par=MP_par3,CC=CC3, Alldata=np.load("csmc2_rcpm_hmF2.npy"), allphase=np.load('csmc2_nSS_hmF2.npy'), All_nss=np.load('csmc2_tnSS_hmF2.npy'))
#np.savez("MTEC_201303_storm", TEC_all = pic, RP_par=RP_par, MP_par=MP_par, CC = CC, Alldata=Alldata, allphase=allphase, All_nss=All_nss)
#np.savez("dst_scatter_map", dst_2013= dst_2013, dst_2021=dst_2021, z_2013=z13, z_2021=z21, z_foF2=zfo,z_hmF2=zhm,  c2_lon=data3['arr_0'], c2_lat=data3['arr_1'], II_list=data3['arr_2'])