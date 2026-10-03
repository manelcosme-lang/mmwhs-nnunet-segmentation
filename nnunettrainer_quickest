from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer
import torch


class nnUNetTrainer_quicktest(nnUNetTrainer):

    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans, configuration, fold, dataset_json, device=device)
        self.num_epochs = 5
        self.num_iterations_per_epoch = 10
        self.num_val_iterations_per_epoch = 5


if __name__ == "__main__":
    import shutil
    from pathlib import Path

    import nnunetv2

    src = Path(__file__).resolve()
    dst = Path(nnunetv2.__path__[0]) / "training" / "nnUNetTrainer" / src.name

    if src == dst:
        print(f"O trainer já está instalado em: {dst}")
    else:
        shutil.copy2(src, dst)
        print(f"Trainer instalado em: {dst}")
