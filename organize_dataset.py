import json
import os
import re
import shutil
import sys
from pathlib import Path

# Todos os caminhos são relativos à pasta onde este script está (a raiz do repositório)
PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_DIR / "data_raw_ct_train"
NNUNET_RAW = Path(os.environ.get("nnUNet_raw", PROJECT_DIR / "nnUNet_raw"))
DATASET_NAME = "Dataset001_Heart"

if not SOURCE_DIR.is_dir():
    sys.exit(f"[ERRO] Pasta de dados não encontrada: {SOURCE_DIR}\n"
             "Cria-a e põe lá os ficheiros ct_train_XXXX_image.nii.gz e ct_train_XXXX_label.nii.gz.")

dataset_dir = NNUNET_RAW / DATASET_NAME
images_tr = dataset_dir / "imagesTr"
labels_tr = dataset_dir / "labelsTr"

images_tr.mkdir(parents=True, exist_ok=True)
labels_tr.mkdir(parents=True, exist_ok=True)

# Padrão dos ficheiros originais: ct_train_1001_image.nii.gz / ct_train_1001_label.nii.gz
pattern = re.compile(r"ct_train_(\d+)_(image|label)\.nii\.gz")

cases = {}  # case_id -> {"image": path, "label": path}

for f in SOURCE_DIR.iterdir():
    match = pattern.match(f.name)
    if not match:
        print(f"[AVISO] Ficheiro ignorado (não corresponde ao padrão esperado): {f.name}")
        continue
    case_id, kind = match.groups()
    cases.setdefault(case_id, {})[kind] = f

# Verificar pares completos
complete_cases = []
for case_id, files in sorted(cases.items()):
    if "image" in files and "label" in files:
        complete_cases.append(case_id)
    else:
        print(f"[AVISO] Caso {case_id} incompleto (falta {'image' if 'image' not in files else 'label'}) — ignorado")

print(f"\nTotal de casos completos encontrados: {len(complete_cases)}\n")

# Copiar e renomear
for case_id in complete_cases:
    new_name = f"heart_{case_id}"
    src_image = cases[case_id]["image"]
    src_label = cases[case_id]["label"]

    dst_image = images_tr / f"{new_name}_0000.nii.gz"
    dst_label = labels_tr / f"{new_name}.nii.gz"

    shutil.copy2(src_image, dst_image)
    shutil.copy2(src_label, dst_label)
    print(f"  {src_image.name} -> {dst_image.name}")
    print(f"  {src_label.name} -> {dst_label.name}")

# Criar dataset.json
# As classes correspondem aos valores depois de correr o remap_labels.py
dataset_json = {
    "channel_names": {
        "0": "CT"
    },
    "labels": {
        "background": 0,
        "myocardium_lv": 1,
        "left_atrium": 2,
        "left_ventricle": 3,
        "right_atrium": 4,
        "right_ventricle": 5,
        "ascending_aorta": 6,
        "pulmonary_artery": 7
    },
    "numTraining": len(complete_cases),
    "file_ending": ".nii.gz"
}

with open(dataset_dir / "dataset.json", "w") as f:
    json.dump(dataset_json, f, indent=4)

print(f"\ndataset.json criado em: {dataset_dir / 'dataset.json'}")
print(f"Estrutura pronta em: {dataset_dir}")
print("\nPróximo passo: python remap_labels.py")
