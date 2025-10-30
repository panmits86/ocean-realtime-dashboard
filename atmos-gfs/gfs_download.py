#!/usr/bin/python3

import xarray as xr
import os
import numpy as np

# for plotting
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def gfs_dl():
    """
    """
    # import the global gfs dataset
    gfs_atmos=xr.open_dataset(os.path.join(os.environ['dir_gfs_subset'],'gfs.t'+os.environ['cycle']+'z.pgrb2.0p25.f000'),
                              engine='cfgrib',filter_by_keys={'typeOfLevel': 'heightAboveGround', 'level': 100})
    # select the area of interest
    gfs_atmos = gfs_atmos.where((gfs_atmos.longitude>=284.)&(gfs_atmos.longitude<=294.)&(gfs_atmos.latitude>=39.)&(gfs_atmos.latitude<=44.5),
                                drop=True)
    # calculate the wind speed at 100 meters using the u100 and v100 variables
    gfs_atmos['wsp100'] = ((['latitude','longitude']), np.sqrt(gfs_atmos['u100'].data**2 + gfs_atmos['v100'].data**2))
    # create and save the gfs subset to netcdf
    gfss = xr.Dataset(data_vars=dict(time=([],gfs_atmos.valid_time.data),
                                     lat=(['latitude'],gfs_atmos.latitude.data),
                                     lon=(['longitude'],gfs_atmos.longitude.data),
                                     wsp100=(['latitude','longitude'],gfs_atmos.wsp100.data),),
                     )
    gfss.to_netcdf(path=os.path.join(os.environ['dir_gfs_subset'],'gfs.'+os.environ['cdate']+'.wsp100.t'+os.environ['cycle']+'z.pgrb2.0p25.f000.nc'),format='NETCDF4')
    
    #======================================================================================================================#
    # plot the gfs 100-m wind speed
    crs = ccrs.LambertConformal()
    fig, ax = plt.subplots(1, 1,figsize=(10., 8.), gridspec_kw={'hspace': 0.05, 'wspace': 0.},
    subplot_kw=dict(projection=crs))
    
    matplotlib.rcParams['font.size'] = 11
    
    cmap10 = (mpl.colors.ListedColormap(['#CAE1FF', '#A2B5CD', '#63B8FF', '#4682B4',
                                         '#CAFE70','#9ACD32','#00FF7F','#00CD00','#FFB6C1',
                                         '#CD919E','#FF6A6A','#CD5555','#FFB90F','#CD950C',
                                         '#FF4500', '#CD3700', '#FFBBFF', '#CD96CD', '#A020F0', 
                                         '#68228B', '#F0E68C', '#CDC673', '#FFA500', '#CD853F'])
              .with_extremes(over='#8B4513'))
    # set the colorbar limits
    bounds1 = np.arange(0.,25.,1.).tolist()
    ticks1=np.arange(0.,25.,2.).tolist()
    norm1 = mpl.colors.Normalize(vmin=0.,vmax=25.,clip=False)
    
    ax.set_extent((-76., -67., 40., 44.5), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.5,edgecolor='black',
                   alpha=0.4,zorder=1)
    ax.coastlines(resolution='10m',linewidth=0.4,alpha=0.8,zorder=1)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, y_inline=False, 
                      linestyle='--',alpha=0.2,linewidth=0.5)
    gl.bottom_labels = False
    gl.top_labels = True
    gl.right_labels = True
    gl.left_labels = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    cs3 = ax.contourf(gfss.lon, gfss.lat, gfss.wsp100,
                      levels=bounds1,norm=norm1,vmin=0.,vmax=24,cmap=cmap10,
                      extend='max',corner_mask=False,zorder=0,transform=ccrs.PlateCarree())
                      
    cax,kw = matplotlib.colorbar.make_axes(ax,location='bottom',pad=0.05,aspect=25,shrink=0.7)

    out=fig.colorbar(cs3,cax=cax,ticks=ticks1,**kw)
    out.set_label('100-m Wind Speed (m/s)',size=12)
    out.ax.tick_params(direction='in',size=3., width=0.7)
    out.ax.tick_params(which='minor', size=0., width=0., direction='in')

    plt.savefig(os.path.join(os.environ['dir_gfs_subset'],'gfs.'+os.environ['cdate']+'.t'+os.environ['cycle']+'.png'), 
                format='png', transparent=False, dpi=600, bbox_inches='tight')
                
                
if __name__=='__main__':
    gfs_dl()
