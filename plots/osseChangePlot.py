import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
csmc2_foF2 = np.load('data/foF2_202111_storm.npz')
csmc2_hmF2 = np.load('data/hmF2_202111_storm.npz')

osse_foF2 = np.load('data/temp_osse.npy')
osse_hmF2 = np.load('data/temp_osse2.npy')
TITLES=['FORMOSAT-7/COSMIC2','GIS_NCKU','IRI2016','IRI2020','SAMI3-RCM','SAMI3-TIEGCM','SAMI3-ICON','WACCM-X','GITM-SWMF','TIEGCM-Weimer','TIEGCM-Heelis','WAM-IPE','CTIPe']
x, y = np.meshgrid(np.arange(0,48,1),np.arange(-45,46,1))
ERRP=np.zeros([len(TITLES),x.shape[0],x.shape[1]])
        
def secPlot(z, multi, data_sm, hmfo):
    if hmfo == "hm":
        osse = osse_hmF2
        csmc2 = csmc2_hmF2
    else:
        osse = osse_foF2
        csmc2 = csmc2_foF2
    TITLES=['FORM-7/COS-2','GIS_NCKU','IRI2016','IRI2020','SAMI3-RCM','SAMI3-TIEGCM','SAMI3-ICON','WACCM-X','GITM-SWMF','TIEGCM-Weimer','TIEGCM-Heelis','WAM-IPE','CTIPe']
    if z==0:
        z0=np.tile(csmc2["C2_"+hmfo+"F2_map"][:,:24],[1,2])
        err1=(csmc2["C2_"+hmfo+"F2_map"][:,24:]-z0)/z0*100
        ERRP[0,:,:]=err1
    elif (z>=1) & (z<=12):
        z0=np.tile(osse[z-1][:,:24],[1,2])
        err1=(osse[z-1][:,24:]-z0)/z0*100
        ERRP[z,:,:]=err1
   # xtitle = YY+' '+TITLES[0][flag]
    
    fig = make_subplots(1, 1, subplot_titles=(''))


    fig.add_trace(go.Heatmap(
        z=err1, #previously controled by z
        zmax = 30,
        zmin = -30,
        x=np.arange(0,72,1),
        y=np.arange(-40,40.5,1),
        colorbar=dict(bordercolor="black",title = "%",tickvals=np.arange(-30,31,15),ticks='outside', outlinecolor='black',outlinewidth=1), #len=.15, thickness=6,

        colorscale="RdBu_r",
    ))


    fig.update_yaxes(title='MLat', range=[-50, 60], tickvals =np.arange(-45,46,15), showgrid=False, 
                     showline=True, linewidth=2, linecolor='black', ticks="outside", mirror=True, title_standoff = 4)
    fig.update_xaxes(title_text="MLT (hr)", showgrid=False,  showline=True, linewidth=2, linecolor='black', 
                     mirror=True,tickmode = 'array',tickvals = np.arange(0, 73, 12), ticks="outside", ticktext = np.mod(np.arange(0,73,12),24))
    
    if not multi:
        b = 70
    else:
        fig.update_traces(colorbar_thickness=10, colorbar_len=data_sm[0])
        fig.update_yaxes(title_standoff = 0)
        b = data_sm[1]
    fig.update_layout(title=TITLES[z]+" OSSE " + hmfo + "F2 Rel. Diff.", title_x=0.5, plot_bgcolor='white', showlegend=False, margin=dict(b=b,  # bottom margin 
                                                                          t=b,  # top margin
                                                                          pad=1))
    return fig