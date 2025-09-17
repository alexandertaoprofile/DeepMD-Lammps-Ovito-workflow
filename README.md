Overview:

This repository contains various LAMMPS simulation scripts for modeling and simulating atomic systems under different conditions, including molecular dynamics (MD) simulations, defect formation, and stress-strain calculations in materials like iron (Fe). The original simulations cover both relaxation and collision dynamics, along with looped iterations to assess system behavior under varying initial conditions and potentials.
New: This repo now also includes a full pipeline to train DeepMD machine-learning interatomic potentials from glass structure datasets (e.g., Li₂S–P₂S₅ glasses from Staacke et al., Edmond/GitLab), reshape/convert XYZ data for DeepMD ingestion, generate DeepMD .pb models, and run LAMMPS MD using the trained DeepMD potential — all packaged with Docker-friendly scripts for reproducibility.

Key Simulations:

BCC Iron Structure: Simulates the relaxation of a Body-Centered Cubic (BCC) iron structure using the EAM potential.
Interstitial and Vacancy Defects: Models defect formation in a metal (Fe) system, calculating formation energies of vacancies and interstitials.
Stress-Strain Simulation: Runs a stress-strain test on a simulated material under different conditions using the NPT and NVE ensembles.
Central Atom Heating: Simulates the heating of a central atom in a BCC structure and applies various fix commands to investigate system response.

Machine-Learning POTENTIAL → MD (new)
Preprocess and reshape open DFT glass structure datasets (e.g., Li₂S–P₂S₅ glasses from Staacke et al., Edmond/GitLab) for DeepMD.
Train DeepMD model (generate .pb model) from reshaped data.
Convert representative DFT snapshots to LAMMPS data files.
Run LAMMPS MD with pair_style deepmd using the trained model; output trajectories for OVITO visualization.
Dockerized workflow to ensure environment reproducibility.
