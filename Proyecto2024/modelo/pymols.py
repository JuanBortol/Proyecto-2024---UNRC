import os
import pymol
from pymol import cmd


# Función para convertir .ent a .pdb
def convert_ent_to_pdb(ent_file, output_folder):
    # Cargar el archivo .ent en PyMOL
    cmd.load(ent_file)

    # Obtener el nombre base del archivo sin extensión
    base_name = os.path.basename(ent_file).replace('.ent', '')

    # Definir la ruta de salida con extensión .pdb
    pdb_output_path = os.path.join(output_folder, f"{base_name}.pdb")

    # Guardar el archivo en formato .pdb
    cmd.save(pdb_output_path)

    # Limpiar la sesión de PyMOL para cargar el siguiente archivo
    cmd.reinitialize()


# Función para procesar todos los archivos .ent en una carpeta
def process_ent_files(input_folder, output_folder):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer todos los archivos en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        # Solo procesar archivos con extensión .ent
        if file_name.endswith('.ent'):
            ent_file_path = os.path.join(input_folder, file_name)
            print(f"Convirtiendo: {ent_file_path}")
            convert_ent_to_pdb(ent_file_path, output_folder)


# Ruta de la carpeta de entrada y salida
input_folder = "/home/macros/Desktop/New Folder/Proyecto-2024---UNRC/Proyecto2024/modelo/conv"
output_folder = "/home/macros/Desktop/New Folder/Proyecto-2024---UNRC/Proyecto2024/modelo/conv2"

# Inicializar PyMOL
pymol.finish_launching(['pymol', '-qc'])  # -qc para no cargar la GUI

# Procesar los archivos
process_ent_files(input_folder, output_folder)

# Salir de PyMOL
cmd.quit()
