# ROMSPath
Offline particle tracking (OPT) is a widely used tool for the analysis of data in oceanographic research. Given the output of a hydrodynamic model, OPT can provide answers to a wide variety of research questions involving fluid kinematics, zooplankton transport, the dispersion of pollutants, and the fate of chemical tracers, among others. In this paper, we introduce ROMSPath, an OPT model designed to complement the Regional Ocean Modelling System (ROMS). Based on the Lagrangian TRANSport (LTRANS) model (North et al., 2008), ROMSPath is written in Fortran 90 and provides advancements in functionality and efficiency compared to LTRANS.  First, ROMSPath now calculates particle trajectories using the ROMS native grid, which provides advantages in interpolation, masking, and boundary interaction, while improving accuracy. Second, ROMSPath enables simulated particles to pass between nested ROMS grids, which are an increasingly popular tool to simulate the ocean over multiple scales.  Third, the ROMSPath vertical turbulence module enables the turbulent (diffusion) time step and advection time step to be specified separately, adding flexibility and improving computational efficiency.  Lastly, ROMSPath includes new infrastructure enabling input of auxiliary parameters for added functionality. In particular, Stokes drift can be input and added to particle advection. Here we describe the details of these updates and improvements. 


# Running Directions

## Prerequisites

Make sure you have a C/Fortran compiler available and the required Python packages installed before getting started.

---

## Running the Offline Tracer

### 1. Configure Initial Particles

Edit `init_particles.csv` to define your initial particle positions. The file format is:

```
<pLon, pLat, pZ, pDOB>
```

### 2. Compile

```bash
make
```

### 3. Run

```bash
./ROMSPath.exe ROMSPath.data
```

---

## Visualization (Python)

### 1. Navigate to the Python directory

```bash
cd python/
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

### 3. Run the script

The plotting script supports two modes:

**Plot trajectories** : generates a map of particle trajectories and saves it as `offline_trajectories.png`:

```bash
python3 plot_offline.py --plot
```

or

```bash
python3 plot_offline.py -p
```

**Summary statistics** : prints key statistics about the particle trajectories including path length and net displacement:

```bash
python3 plot_offline.py --summary
```

or

```bash
python3 plot_offline.py -s

### Honors 212 Coding Project, James Susanto and Ryo Ikeda
