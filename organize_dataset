import json
import os
import re
import shutil
from pathlib import Path


SOURCE_DIR = Path.home() / "projetos" / "cardio-nnunet" / "data_raw_ct_train"
NNUNET_RAW = Path(os.environ.get("nnUNet_raw", Path.home() / "projetos" / "cardio-nnunet" / "nnUNet_raw"))
DATASET_NAME = "Dataset001_Heart"


dataset_dir = NNUNET_RAW / DATASET_NAME
images_tr = dataset_dir / "imagesTr"
labels_tr = dataset_dir / "labelsTr"

images_tr.mkdir(parents=True, exist_ok=True)
labels_tr.mkdir(parents=True, exist_ok=True)


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
# Valores confirmados nos ficheiros de label do MM-WHS (7 estruturas + fundo)
dataset_json = {
    "channel_names": {
        "0": "CT"
    },
    "labels": {
        "background": 0,
        "myocardium_lv": 205,
        "left_atrium": 420,
        "left_ventricle": 500,
        "right_atrium": 550,
        "right_ventricle": 600,
        "ascending_aorta": 820,
        "pulmonary_artery": 850
    },
    "numTraining": len(complete_cases),
    "file_ending": ".nii.gz"
}

with open(dataset_dir / "dataset.json", "w") as f:
    json.dump(dataset_json, f, indent=4)

print(f"\ndataset.json criado em: {dataset_dir / 'dataset.json'}")
print(f"Estrutura pronta em: {dataset_dir}")
print("\nATENÇÃO: revê o campo 'labels' no dataset.json — o MM-WHS pode ter múltiplas")
print("estruturas anotadas (aorta, ventrículo esquerdo, etc.) com valores diferentes de 1.")
print("Verifica com um visualizador (3D Slicer) ou com numpy/SimpleITK quais os valores")
print("presentes num ficheiro de label antes de correres o pré-processamento do nnU-Net.")
