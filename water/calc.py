"""
GSF計算の例
例に使用している入力ファイルの値は比較的悪い値を利用しているためまじめに計算するときは少なくとも一桁は精度の高い値を利用すること。
"""

from yVL.core import VaspInput, make_kpoints, OddOrEven
from yVL.core import ML_AB
from yVL.job import vaspjob

from pymatgen.io.vasp.inputs import Poscar, Incar, Potcar, Kpoints
from pymatgen.core import Structure

import shutil
import datetime
import os
import glob

def md_calc(vasp_input, workdir):
    job = vaspjob.Job(vasp_input=vasp_input,
                      workdir=workdir,
                      command_list=["ml_train_md"]
                      )
    job.start()
    poscar = job.result.get_contcar()
    _ml_ab = job.result.get_mlabn()

    if poscar == None or _ml_ab == None:
        raise Exception("学習に失敗している")

    return poscar, _ml_ab


if __name__ == "__main__":
    # 計算条件の設定
    initial_dir = os.path.dirname(os.path.abspath(__file__))

    kpoints = Kpoints.gamma_automatic()  # 1x1x1のk点メッシュ
    incar = Incar.from_file("INCAR")  # INCARファイルの読み込み

    potcar_dict = {
        "H": "H",
        "O": "O"
    }
    potcar = Potcar(
        symbols=[potcar_dict[key] for key in initial_poscar.site_symbols]
    )
    kpoints = make_kpoints(poscar=initial_poscar, a_factor=40,
                           force_odd_or_even=OddOrEven.Even)

    if os.path.exists(os.path.join(initial_dir, "ML_AB")):
        ml_ab = ML_AB.from_file(os.path.join(initial_dir, "ML_AB"))
        shutil.copy(os.path.join(initial_dir, "ML_AB"), os.path.join(
            initial_dir, f"ML_ABO_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"))
    else:
        ml_ab=None

    structure_file_list = glob.glob(os.path.join(initial_dir, "*.cif"))
    for structure_file in structure_file_list:
        initial_structure = Structure.from_file(structure_file)
        initial_poscar = Poscar(initial_structure)
        
        structure_name = os.path.basename(structure_file).replace(".cif", "")
        structure_dir = os.path.join(initial_dir, structure_name)
        for temperature in [100, 200, 250, 300, 350]:
            poscar = Poscar(initial_structure)
            incar["TEBEG"] = temperature
            for volume_scale in [1, 0.9, 0.8]:

                poscar.structure.scale_lattice(initial_structure.volume*volume_scale)
                vasp_input = VaspInput(incar, kpoints, poscar, potcar)

                if ml_ab is not None:
                    vasp_input["ML_AB"] = ml_ab

                workdir = os.path.join(
                    structure_dir, f"T{temperature}K", f"volume_scale_{volume_scale}")
                poscar, _ml_ab = md_calc(vasp_input, workdir)
                
                if _ml_ab == None:
                    raise Exception("ML_ABが空. 計算失敗")
                _ml_ab.write_file(os.path.join(initial_dir, "ML_AB"))

                if ml_ab is not None and _ml_ab.header.num_config.data > ml_ab.header.num_config.data:
                    ml_ab = _ml_ab
                elif ml_ab is None:
                    ml_ab = _ml_ab
                    
                    
            poscar = Poscar(initial_structure)
            for volume_scale in [1, 1.1, 1.2]:

                poscar.structure.scale_lattice(initial_structure.volume*volume_scale)
                vasp_input = VaspInput(incar, kpoints, poscar, potcar)

                if ml_ab is not None:
                    vasp_input["ML_AB"] = ml_ab

                workdir = os.path.join(
                    structure_dir, f"T{temperature}K", f"volume_scale_{volume_scale}")
                poscar, _ml_ab = md_calc(vasp_input, workdir)
                
                if _ml_ab == None:
                    raise Exception("ML_ABが空. 計算失敗")
                _ml_ab.write_file(os.path.join(initial_dir, "ML_AB"))

                if ml_ab is not None and _ml_ab.header.num_config.data > ml_ab.header.num_config.data:
                    ml_ab = _ml_ab
                elif ml_ab is None:
                    ml_ab = _ml_ab
