import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import argparse

def haversine(lon1, lat1, lon2, lat2):
    R = 6371
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

#Plot mode
def plot_trajectories(ds):
    numpar = ds.sizes['numpar']
    colors = cm.rainbow(np.linspace(0, 1, numpar))

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})

    # ******************
    # Coordinate window set for gulf of Guinea. Change if Different Area
    # ******************    
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

    legend_elements = [Line2D([0], [0], marker='.', color='w', markerfacecolor='black',
                              markersize=8, label='Start position')]
    ax.legend(handles=legend_elements, loc='lower left')
    

    # ******************
    # Title of Plot, Change to Preference
    # ******************    
    plt.title('Offline Particle Trajectories - Gulf of Guinea')
    plt.savefig('offline_trajectories.png', dpi=150, bbox_inches='tight')
    print('saved to offline_trajectories.png')

def print_summary(ds):
    numpar = ds.sizes['numpar']
    lon = ds.lon.values
    lat = ds.lat.values

    total_distances = []
    net_distances = []

    for i in range(numpar):
        lo = lon[:, i]
        la = lat[:, i]
        valid = (~np.isnan(lo)) & (~np.isnan(la)) & (np.abs(lo) < 1e10) & (np.abs(la) < 1e10)
        lo = lo[valid]
        la = la[valid]
        if len(lo) < 2:
            continue

        dist = sum(haversine(lo[j], la[j], lo[j+1], la[j+1]) for j in range(len(lo)-1))
        total_distances.append(dist)

        net = haversine(lo[0], la[0], lo[-1], la[-1])
        net_distances.append(net)

    total_distances = np.array(total_distances)
    net_distances = np.array(net_distances)

    print("=" * 45)
    print("  FLOAT TRAJECTORY SUMMARY - Gulf of Guinea")
    print("=" * 45)
    print(f"  Number of floats:       {numpar}")
    print()
    print("  PATH LENGTH (km):")
    print(f"    Average:              {total_distances.mean():.2f}")
    print(f"    Longest:              {total_distances.max():.2f}")
    print(f"    Shortest:             {total_distances.min():.2f}")
    print(f"    Std dev:              {total_distances.std():.2f}")
    print()
    print("  NET DISPLACEMENT (km):")
    print(f"    Average:              {net_distances.mean():.2f}")
    print(f"    Maximum:              {net_distances.max():.2f}")
    print(f"    Minimum:              {net_distances.min():.2f}")
    print("=" * 45)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze float trajectories')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-p', '--plot', action='store_true', help='Plot trajectories')
    group.add_argument('-s', '--summary', action='store_true', help='Print statistics')
    args = parser.parse_args()

    # ***********************
    # Path & name of offline output - Change
    # ***********************
    ds = xr.open_dataset('../out/gulf_guinea_offline.nc', decode_timedelta=False)

    if args.plot:
        plot_trajectories(ds)
    elif args.summary:
        print_summary(ds)