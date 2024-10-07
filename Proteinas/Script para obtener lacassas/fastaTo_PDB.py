import requests
import os

def download_pdb(protein_id, output_dir='downloaded_proteins'):
    url = f'https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{protein_id.lower()}.ent'
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
        print(f'Respuesta del servidor: {response.text}')

def extract_protein_ids(fasta_file):
    protein_ids = []
    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                protein_id = line.split('|')[1]  # Ajusta esto según el formato de tu archivo FASTA
                protein_ids.append(protein_id)
    return protein_ids

def main():
    fasta_file = 'Sec de proteinas de Lacasas de varias especies.fasta'
    protein_ids = extract_protein_ids(fasta_file)

    for protein_id in protein_ids:
        download_pdb(protein_id)

if __name__ == '__main__':
    main()
