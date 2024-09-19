
from io import TextIOWrapper
from typing import TextIO

from gradio_client import Client, file
import glob

client = Client("https://5b8add2a5d98b1a652ea7fd72d942dac.app-space.dplink.cc/")

receptor_files = glob.glob('*.ent')

resultPocket = client.predict(
    ligand_file=file('1G9V_ligand.sdf'),
    expand_size=10,
    api_name="/get_pocket_by_ligand"
)

for receptor_file in receptor_files:
    print(receptor_file)
    resultDocking = client.predict(
        receptor_pdb=file(receptor_file),
        ligand_sdf=file('AFB1_ligand.sdf'),
        center_x=resultPocket[0],
        center_y=resultPocket[1],
        center_z=resultPocket[2],
        size_x=resultPocket[3],
        size_y=resultPocket[4],
        size_z=resultPocket[5],
        model_version="Pocket Augmentated (Model which is more robust when the pocket is not well defined.)",
        use_unidock=True,
        task_name="Hello!!",
        api_name="/_unimol_docking_wrapper"
    )

    a, b, c, d = resultDocking

    try:
        file_path = b['value']
    except (TypeError, KeyError):
        print('la proteina ' + receptor_file + ' no hace docking')
        continue

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(">  <docking_score>"):
                docking_score = file.readline().strip()
                print('la proteina ' + receptor_file + docking_score)