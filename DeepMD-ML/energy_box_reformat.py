import os
import re
import numpy as np

def parse_xyz(xyz_file):
    """
    Parse the .xyz file and extract the energy, coordinates, forces, and box for all timesteps.
    """
    coords_all = []  # This will hold coordinates for all systems (timesteps)
    forces_all = []  # This will hold forces for all systems (timesteps)
    energies_all = []  # This will hold energies for all systems (timesteps)
    box_all = []  # This will hold box data for all systems (timesteps)

    # Step 1: Read all lines from the file
    with open(xyz_file, 'r') as file:
        lines = file.readlines()

    current_coords = []
    current_forces = []
    current_box = None

    atom_count = None  # This will store the atom count for each system

    # Step 2: Extract all energies
    energies = []
    for line in lines:
        # Look for lines that contain energy values
        energy_match = re.search(r'energy\s*=\s*(-?\d+\.\d+e?[+-]?\d*)', line)
        if energy_match:
            energy_value = float(energy_match.group(1))  # Extract the energy value
            energies.append(energy_value)  # Store in the energy list
            print(f"Extracted energy: {energy_value}")  # Debugging output

    # Step 3: Now we process the rest of the file (coordinates, forces, and box)
    atom_count = None
    current_energy_idx = 0  # Index for energy list

    for line in lines:
        print(f"Line: {line.strip()}")  # Debugging output: show each line being processed

        if 'Lattice' in line:
            # Extract full Lattice line with Properties and energy in it
            lattice_line = line.split('Properties')[0].strip()  # Remove 'Properties' and the following part
            box_str = lattice_line.split('Lattice=')[-1].strip().replace('"', '')
            
            # Extract box data and store as a 1D list
            box = list(map(float, box_str.split()))
            current_box = box  # Store as a 1D list of 9 elements

        elif line.strip().isdigit():
            # Atom count line for each timestep
            if atom_count is not None:  # If atom_count is set, that means we have completed a system (timestep)
                # Save the data for the current system
                coords_all.append(current_coords)  # Append the list of coords for this timestep
                forces_all.append(current_forces)  # Append the list of forces for this timestep
                
                # Add the energy from the pre-extracted list
                energies_all.append(energies[current_energy_idx])  # Directly store energy
                box_all.append(current_box)  # Append the box as a 1D list

                # Move to the next energy value
                current_energy_idx += 1

            # Reset for the new system (timestep)
            atom_count = int(line.strip())  # The number of atoms in this system
            current_coords = []
            current_forces = []

        elif line[0] in ('C', 'H', 'O', 'P', 'S', 'Li'):  # Assuming these are the atom types
            # Read atom positions and forces
            parts = line.split()
            coords = [float(parts[1]), float(parts[2]), float(parts[3])]
            forces = [float(parts[4]), float(parts[5]), float(parts[6])]

            current_coords.extend(coords)  # Add coordinates to current_coords (flattened)
            current_forces.extend(forces)  # Add forces to current_forces (flattened)

    # Don't forget to save the last system after loop ends
    if atom_count is not None:
        coords_all.append(current_coords)  # Append the last timestep's coords
        forces_all.append(current_forces)  # Append the last timestep's forces
        energies_all.append(energies[current_energy_idx])  # Directly store energy
        box_all.append(current_box)  # Append the last timestep's box

    # Now return everything as numpy arrays
    return np.array(coords_all), np.array(energies_all), np.array(forces_all), np.array(box_all)

def process_data(data_dir):
    """
    Process the data in the provided directory and save the npy files for each .xyz file.
    Each .xyz file will produce a single set of npy files for coords, energy, forces, and box.
    """
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.xyz'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                coords_all, energies_all, forces_all, box_all = parse_xyz(file_path)

                # Saving data into npy format for the entire file
                base_name = os.path.splitext(file)[0]  # Using the filename (without extension) as base name

                # Save the data for all systems as single files
                #np.save(os.path.join(root, f"{base_name}_coord.npy"), coords_all)
                np.save(os.path.join(root, f"{base_name}_energy.npy"), energies_all)
                #np.save(os.path.join(root, f"{base_name}_force.npy"), forces_all)
                np.save(os.path.join(root, f"{base_name}_box.npy"), box_all)

                print(f"Data saved for {file_path}")

if __name__ == '__main__':
    # Set the data directory path here
    data_dir = "E:/deepmd/glass/Li3PS4"  # Replace with your actual data folder path
    process_data(data_dir)
