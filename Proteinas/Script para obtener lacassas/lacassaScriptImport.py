import requests
import os

def download_pdb(protein_id, output_dir='downloaded_proteins'):
    url = f'https://files.rcsb.org/download/{protein_id}.pdb'
    response = requests.get(url)

    if response.status_code == 200:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, f'{protein_id}.pdb')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Descargado: {file_path}')
    else:
        print(f'Error al descargar {protein_id}: {response.status_code}')

def main():
    input_file = 'lacassaListPdb.txt'
    with open(input_file, 'r') as file:
        protein_ids = [line.strip() for line in file]

    for protein_id in protein_ids:
        download_pdb(protein_id)

if __name__ == '__main__':
    main()
