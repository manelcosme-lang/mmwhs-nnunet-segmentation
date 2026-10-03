# cardio-nnunet

Segmentação de estruturas cardíacas em CT com o [nnU-Net v2](https://github.com/MIC-DKFZ/nnUNet), usando os dados de treino de CT do MM-WHS (20 casos).

A rede aprende a distinguir 7 estruturas:

| Valor no MM-WHS | Classe no nnU-Net | Estrutura |
|---|---|---|
| 0 | 0 | fundo |
| 205 | 1 | miocárdio do ventrículo esquerdo |
| 420 | 2 | aurícula esquerda |
| 500 | 3 | ventrículo esquerdo |
| 550 | 4 | aurícula direita |
| 600 | 5 | ventrículo direito |
| 820 | 6 | aorta ascendente |
| 850 | 7 | artéria pulmonar |

## Conteúdo do repositório

| Ficheiro | O que faz |
|---|---|
| `organize_dataset.py` | Copia e renomeia os dados originais para a estrutura que o nnU-Net exige e cria o `dataset.json` |
| `remap_labels.py` | Converte os valores dos labels do MM-WHS (205, 420, ...) em inteiros consecutivos (1 a 7) |
| `nnUNetTrainer_quicktest.py` | Trainer curto (5 épocas de 10 iterações) para verificar que o pipeline corre de ponta a ponta. Corrido diretamente, instala-se dentro do pacote `nnunetv2` |
| `requirements.txt` | Dependências Python |

Os dados e as pastas geradas pelo nnU-Net não estão no repositório (ver `.gitignore`).

## Como reproduzir

Todos os comandos são corridos a partir da raiz do repositório.

### 1. Ambiente

Testado com Python 3.13, nnU-Net 2.8.1 e PyTorch 2.14.0, num MacBook Air M1.

```bash
git clone <URL_DO_REPOSITORIO>
cd cardio-nnunet
python3 -m venv nnunet-env
source nnunet-env/bin/activate
pip install -r requirements.txt
```

### 2. Onde pôr os dados

Cria a pasta `data_raw_ct_train/` na raiz do repositório e põe lá os 40 ficheiros de treino de CT do MM-WHS, com os nomes originais:

```
cardio-nnunet/
└── data_raw_ct_train/
    ├── ct_train_1001_image.nii.gz
    ├── ct_train_1001_label.nii.gz
    ├── ...
    ├── ct_train_1020_image.nii.gz
    └── ct_train_1020_label.nii.gz
```

### 3. Variáveis de ambiente do nnU-Net

```bash
export nnUNet_raw="$(pwd)/nnUNet_raw"
export nnUNet_preprocessed="$(pwd)/nnUNet_preprocessed"
export nnUNet_results="$(pwd)/nnUNet_results"
```

Têm de ser definidas em cada terminal novo.

### 4. Organizar os dados

```bash
python organize_dataset.py
```

Cria `nnUNet_raw/Dataset001_Heart/` com `imagesTr/`, `labelsTr/` e `dataset.json`.

### 5. Remapear os labels

```bash
python remap_labels.py
```

Reescreve os ficheiros de `labelsTr/` com os valores 0 a 7. Pode ser corrido mais do que uma vez: os ficheiros já remapeados são ignorados.

### 6. Planeamento e pré-processamento

```bash
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity
```

### 7. Instalar o trainer

```bash
python nnUNetTrainer_quicktest.py
```

O nnU-Net só encontra trainers que estejam dentro do pacote `nnunetv2` instalado; este comando copia o ficheiro para lá.

### 8. Treinar

```bash
nnUNetv2_train 1 2d 0 -tr nnUNetTrainer_quicktest -device mps
```

`-device mps` é para Macs com Apple Silicon. Com uma GPU NVIDIA usa-se `-device cuda`; sem GPU, `-device cpu`.

### 9. Resultados

No fim do treino, o nnU-Net prevê automaticamente os 4 casos de validação do fold 0, que a rede não usou para aprender. Tudo fica em:

```
nnUNet_results/Dataset001_Heart/nnUNetTrainer_quicktest__nnUNetPlans__2d/fold_0/
├── checkpoint_final.pth     # a rede treinada
├── progress.png             # curvas de treino
└── validation/
    ├── heart_XXXX.nii.gz    # segmentações previstas
    └── summary.json         # Dice por classe e por caso
```

O trainer `quicktest` faz só 50 iterações no total, por isso serve para mostrar que o pipeline funciona e não para obter segmentações de qualidade.

### 10. Prever em imagens novas

As imagens têm de estar numa pasta própria, com o sufixo `_0000` (por exemplo `heart_2001_0000.nii.gz`).

```bash
nnUNetv2_predict -i PASTA_IMAGENS -o PASTA_PREDICOES -d 1 -c 2d -f 0 -tr nnUNetTrainer_quicktest -device mps --disable_tta
```

As predições têm os valores 0 a 7 da tabela acima.
