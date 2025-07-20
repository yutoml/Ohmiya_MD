from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Poscar, Potcar

from yVL.core import make_kpoints
import os

if __name__ == "__main__":
    # Define the structure using the lattice vectors and atomic positions
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(initial_dir)
    poscar = Poscar.from_file(os.path.join(initial_dir, "POSCAR"))
    
    kpoints = make_kpoints(poscar, 
                           a_factor=40)
    kpoints.write_file("KPOINTS")
    
    potcar_dict = {
        "H": "H",
        "O": "O"
    }
    potcar = Potcar(
        symbols=[potcar_dict[key] for key in poscar.site_symbols]
    )
    potcar.write_file("POTCAR")