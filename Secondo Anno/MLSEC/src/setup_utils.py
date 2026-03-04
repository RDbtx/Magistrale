import json

import os
import robustbench as rob
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import numpy as np


def move_operations_to_device(model: torch.nn.Module, device: str) -> torch.nn.Module:
    """
    Move model attributes such as mean and standard deviation, used by the model during
    AutoAttack, to the selected device.

    Inputs:
    - model: the given model.
    - device: the device (such as CPU or GPU) to move the selected attributes to.

    Output:
    - model: the modified model.

    """
    for attr in ("mean", "std"):
        if hasattr(model, attr):
            t = getattr(model, attr)
            if torch.is_tensor(t):
                setattr(model, attr, t.to(device))
    return model


def device_for_model(name: str) -> str:
    """
    Select the most suitable device to run a model on this machine.
    The function prefers CUDA when available. If CUDA is not available, it
    falls back to Apple MPS. Otherwise, it uses CPU.

    Input:
    - name: name of the model

    Output:
    - device: the chosen device.

    """
    if torch.cuda.is_available():
        print(f"CUDA available for {name}")
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print(f"MPS is available for {name}")
        return "mps"

    print(f"no MPS or CUDA for {name}. Fallback to CPU")
    return "cpu"


def compute_elapsed_time(start: float, end: float) -> list:
    """
    Compute the elapsed time between `start` and `end` in hours:minutes:seconds format.

    Inputs:
    - start: the start time
    - end: the end time

    Output:
    - a list containing the elapsed time as [hours, minutes, seconds].

    """
    elapsed = end - start
    hours, resto = elapsed // 3600, (elapsed % 3600)
    minutes, seconds = resto // 60, resto % 60
    return [int(hours), int(minutes), int(seconds)]


def load_data(dataset_samples: int, seed: int, batch_size: int) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Load a subset of CIFAR-10 test data into CPU tensors.
    The function downloads (if needed) the CIFAR-10 test set, randomly selects
    `dataset_samples` indices using `seed`, and returns the stacked samples and labels.

    Inputs:
    - dataset_samples: the number of samples to load.
    - seed: the random seed used to select a subset.
    - batch_size: the batch size used by the DataLoader while loading tensors.

    Outputs:
    - x: samples tensor.
    - y: labels tensor.

    """
    print("\n---- LOADING DATA ----")
    transform = transforms.ToTensor()
    print("Loading CIFAR10 dataset...")
    testset = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)

    rng = np.random.default_rng(seed)
    idx = rng.choice(len(testset), dataset_samples, replace=False)

    print(
        f"Generating Subset with:\n"
        f" - samples: {dataset_samples}\n"
        f" - seed: {seed}\n"
        f" - batch_size: {batch_size}"
    )
    subset = Subset(testset, idx)
    loader = DataLoader(subset, batch_size=batch_size, shuffle=False, num_workers=2)

    x_list = []
    y_list = []
    for x, y in loader:
        x_list.append(x)
        y_list.append(y)

    x = torch.cat(x_list, dim=0)
    y = torch.cat(y_list, dim=0)
    print("Dataset loaded on CPU!")
    return x, y


def load_models(model_names: list) -> dict:
    """
    This function takes as input a list of RobustBench model names, loads each model configured
    for CIFAR-10, and returns a dictionary mapping names to model instances.

    Inputs:
    - model_names: a list of model names.

    Output:
    - models: a dictionary with the model names as keys and the loaded models as values.

    """
    print("\n---- LOADING MODELS ----")
    models = {}
    for name in model_names:
        print(f"Loading {name}...")
        m = rob.load_model(model_name=name, dataset="cifar10", threat_model="Linf")
        m.eval()
        models[name] = m
    print("Models loaded!")
    return models
