import os
from pathlib import Path

import numpy as np
import SimpleITK as sitk

PROJECT_DIR = Path(__file__).resolve().parent
NNUNET_RAW = Path(os.environ.get("nnUNet_raw", PROJECT_DIR / "nnUNet_raw"))
DATASET_NAME = "Dataset001_Heart"
labels_dir = NNUNET_RAW / DATASET_NAME / "labelsTr"

MAPPING = {0: 0, 205: 1, 420: 2, 500: 3, 550: 4, 600: 5, 820: 6, 850: 7}
NEW_VALUES = set(MAPPING.values())

label_files = sorted(labels_dir.glob("*.nii.gz"))
print(f"Encontrados {len(label_files)} ficheiros de label em {labels_dir}\n")

for f in label_files:
    img = sitk.ReadImage(str(f))
    arr = sitk.GetArrayFromImage(img)
    values = set(np.unique(arr).tolist())

    if values <= NEW_VALUES:
        print(f"  {f.name} -> já remapeado, ignorado")
        continue

    remapped = np.zeros_like(arr, dtype=np.uint8)
    for old_val, new_val in MAPPING.items():
        remapped[arr == old_val] = new_val
    unmapped = values - set(MAPPING.keys())
    if unmapped:
        print(f"[AVISO] {f.name}: valores nao mapeados (ficam como fundo): {unmapped}")
    new_img = sitk.GetImageFromArray(remapped)
    new_img.CopyInformation(img)
    sitk.WriteImage(new_img, str(f))
    print(f"  {f.name} -> remapeado")

print("\nConcluido.")
