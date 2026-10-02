import os
from pathlib import Path
import numpy as np
import SimpleITK as sitk

NNUNET_RAW = Path(os.environ.get("nnUNet_raw"))
DATASET_NAME = "Dataset001_Heart"
labels_dir = NNUNET_RAW / DATASET_NAME / "labelsTr"

MAPPING = {0: 0, 205: 1, 420: 2, 500: 3, 550: 4, 600: 5, 820: 6, 850: 7}

label_files = sorted(labels_dir.glob("*.nii.gz"))
print(f"Encontrados {len(label_files)} ficheiros de label em {labels_dir}\n")

for f in label_files:
    img = sitk.ReadImage(str(f))
    arr = sitk.GetArrayFromImage(img)
    remapped = np.zeros_like(arr, dtype=np.uint8)
    for old_val, new_val in MAPPING.items():
        remapped[arr == old_val] = new_val
    unmapped = set(np.unique(arr)) - set(MAPPING.keys())
    if unmapped:
        print(f"[AVISO] {f.name}: valores nao mapeados: {unmapped}")
    new_img = sitk.GetImageFromArray(remapped)
    new_img.CopyInformation(img)
    sitk.WriteImage(new_img, str(f))
    print(f"  {f.name} -> remapeado")

print("\nConcluido.")
