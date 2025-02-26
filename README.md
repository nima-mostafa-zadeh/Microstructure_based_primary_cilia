# Primary Cilium Model Generator for Abaqus

This script generates a microstructure-based model of a primary cilium in Abaqus for finite element analysis, as used in "Microstructure-based modeling of primary cilia mechanics" (Mostafazadeh et al., 2024).

## Adjustable Properties

### 1. Cilium Geometry
- `CILIUM_RADIUS`: Radius of the cilium
- `CILIUM_LENGTH`: Length of the cilium

### 2. Microtubule Arrangement
- `MT_DOUBLET_NUMBER`: Number of microtubule doublets
- `MT_RADIAL_DISTANCE`: Distance of microtubules from cilium center

### 3. Microtubule Geometry
- `MT_RADIUS`: Radius of each microtubule in the doublets (array of values for each doublet)
- `MT_LENGTH_A`: Length of A tubules in each doublet (customizable array)
- `MT_LENGTH_B`: Length of B tubules in each doublet (customizable array)
- `MT_COINCIDENT_RADIUS`: Controls the intersection depth between A and B tubules

### 4. Orientation Parameters
- `MT_TILT_ANGLE`: Tilt angle of microtubule doublets relative to cilium axis
- `MT_ROTATION_ANGLE`: Rotation angle of the entire microtubule array

### 5. Material Properties (Anisotropic)
#### Ciliary Membrane
- `CILIUM_E1`, `CILIUM_E2`: Longitudinal and circumferential Young's moduli
- `CILIUM_v12`: Poisson's ratio
- `CILIUM_G12`, `CILIUM_G13`, `CILIUM_G23`: Shear moduli
- `CILIUM_DENSITY`: Mass density
- `CILIUM_ALPHA`: Damping coefficient

#### Microtubules
- `MT_E1`, `MT_E2`: Longitudinal and circumferential Young's moduli
- `MT_v12`: Poisson's ratio
- `MT_G12`, `MT_G13`, `MT_G23`: Shear moduli
- `MT_DENSITY`: Mass density
- `MT_ALPHA`: Damping coefficient

### 6. Shell Thickness
- `CILIUM_THICKNESS`: Thickness of ciliary membrane
- `MICROTUBULE_THICKNESS`: Thickness of microtubule shell

## Simulation Setup

The script generates a model for a single cilium and applies a unidirectional load on the cap region of the cilium to bend it. This simulates an optical tweezer experiment where force is applied to the tip of the cilium while the base is fixed.

- The base of the cilium (both membrane and microtubules) is fixed using an encastre boundary condition
- A surface traction (`LOADING_VALUE`) is applied to the cap region
- The loading is ramped using a smooth step amplitude function (`AMPLITUDE`)

## Analysis and Output

The simulation runs as an explicit dynamic analysis with the following outputs:

- Stress and strain distributions throughout the cilium membrane and microtubules
- Deformation patterns including displacement and rotation
- Reaction forces at the base
- Contact stress and forces between microtubules and membrane
- Energy metrics (kinetic, strain, etc.)

These outputs can be used to analyze the mechanical behavior of primary cilia, the influence of microtubule arrangement on cilium bending stiffness, and the stress distributions that may activate mechanosensitive channels.
