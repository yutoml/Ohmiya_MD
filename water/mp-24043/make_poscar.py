from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Poscar

from yVL.core import make_kpoints

import os


if __name__ == "__main__":
    # Define the structure using the lattice vectors and atomic positions
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(initial_dir)
    structure = Structure.from_file(os.path.join(initial_dir,"mp-24043.cif"))

    # Create a Poscar object
    poscar = Poscar(structure)
    poscar.structure.make_supercell([
        [1,0,0],
        [0,1,0],
        [0,0,2]
    ])

    # Write the POSCAR file
    poscar.write_file("POSCAR")
    
    kpoints = make_kpoints(poscar, 
                           a_factor=40)
    kpoints.write_file("KPOINTS")