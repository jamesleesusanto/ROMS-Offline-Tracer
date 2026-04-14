import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_dataset('../out/gulf_guinea_offline.nc', decode_timedelta=False)

numpar = ds.sizes['numpar']
colors = cm.rainbow(np.linspace(0, 1, numpar))

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})

#Adjust Coord Window
ax.set_extent([-15, 10, -10, 8], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.OCEAN, alpha=0.3)
ax.add_feature(cfeature.LAND, alpha=0.3)
ax.add_feature(cfeature.COASTLINE)
ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

for i in range(numpar):
    ax.plot(ds.lon[:, i], ds.lat[:, i], transform=ccrs.PlateCarree(),
            color=colors[i], linewidth=0.8)
    ax.plot(ds.lon[0, i], ds.lat[0, i], 'k.', markersize=1,
            transform=ccrs.PlateCarree())

# Legend
legend_elements = [Line2D([0], [0], marker='.', color='w', markerfacecolor='black',
                          markersize=8, label='Start position')]
ax.legend(handles=legend_elements, loc='lower left')

plt.title('Offline Particle Trajectories - Gulf of Guinea')
plt.savefig('offline_trajectories.png', dpi=150, bbox_inches='tight')
print('saved to offline_trajectories.png')