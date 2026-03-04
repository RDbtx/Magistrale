from autoattack import AutoAttack
from src.setup_utils import *
from src.results_processing_utils import *
import time
import torch


def robust_acc_autoattack(model, x, y, eps: float, device: str, mode: str = "standard", bs: int = 50,
                          verbose: bool = True) -> float:
    """
    Compute robust accuracy of a model under AutoAttack for a given epsilon.
    The function generates adversarial examples using AutoAttack (or a custom
    subset of attacks depending on `mode`) and then measures the fraction of
    correctly classified adversarial samples.

    Inputs:
    - model: the model to evaluate.
    - x: input samples tensor.
    - y: labels tensor.
    - eps: perturbation budget for Linf attacks.
    - device: the device used by AutoAttack.
    - mode: attack configuration mode. One of:
        - "fast": runs APGD-CE only.
        - "untargeted": runs APGD-CE and SQUARE.
        - "targeted": runs APGD-T and FAB-T.
        - "standard": runs AutoAttack standard suite.
    - bs: batch size used during AutoAttack evaluation.
    - verbose: whether AutoAttack should print progress/details.

    Output:
    - robust_acc: robust accuracy measured.

    """
    if mode == "fast untargeted":
        print("Fast mode selected [APGD-CE only]!")
        adversary = AutoAttack(model, norm="Linf", eps=eps, version="custom", device=device, verbose=verbose)
        adversary.attacks_to_run = ["apgd-ce"]

    elif mode == "fast targeted":
        print("Fast mode selected [APGD-T only]!")
        adversary = AutoAttack(model, norm="Linf", eps=eps, version="custom", device=device, verbose=verbose)
        adversary.attacks_to_run = ["apgd-t"]

    elif mode == "untargeted":
        print("Untargeted mode selected [APGD-CE, SQUARE]!")
        adversary = AutoAttack(model, norm="Linf", eps=eps, version="custom", device=device, verbose=verbose)
        adversary.attacks_to_run = ["apgd-ce", "square"]

    elif mode == "targeted":
        print("Targeted mode selected [APGD-T, FAB-T]!")
        adversary = AutoAttack(model, norm="Linf", eps=eps, version="custom", device=device, verbose=verbose)
        adversary.attacks_to_run = ["apgd-t", "fab-t"]

    elif mode == "standard":
        print("Running standard mode!")
        adversary = AutoAttack(model, norm="Linf", eps=eps, version="standard", device=device, verbose=verbose)

    else:
        raise ValueError("Unknown mode. Use one of: fast, untargeted, targeted, standard")

    x_adv = adversary.run_standard_evaluation(x, y, bs=bs)

    with torch.no_grad():
        pred = model(x_adv).argmax(1)
        robust_acc = (pred == y).float().mean().item()
        return robust_acc


def autoattack_models(models: dict, x_test_cpu, y_test_cpu, batch_size: int, mode: str = "standard",
                      steps: list = None, verbose: bool = True) -> dict:
    """
    Run AutoAttack over multiple models and multiple epsilon values.
    The function evaluates each model in `models` across a fixed set of Linf
    epsilon values (1/255, 4/255, 8/255, 12/255, 16/255). For each model, it:
    - selects a device using `device_for_model`,
    - moves the model to that device and switches to eval mode,
    - moves any model-side tensors/operations needed for evaluation,
    - transfers the test data to the device,
    - runs AutoAttack and records robust accuracy and timing.

    Inputs:
    - models: dictionary containing the model and its RobustBench accuracy
    - x_test_cpu: test samples.
    - y_test_cpu: test labels.
    - batch_size: batch size used during AutoAttack evaluation.
    - mode: AutoAttack mode (fast, untargeted, targeted, standard).
    - verbose: whether AutoAttack should print progress/details.

    Output:
    - results: nested dictionary containing:
        results[eps_key][model_name] = {
            "robust_acc": float,
            "device": str,
            "time_s": float,
            "mode": str,
            "bs": int
        }

    """
    print("\n---- STARTING AUTOATTACK ----")
    results = {}

    if steps is None:
        steps = [1, 4, 8, 12, 16]

    eps_list = [e / 255 for e in steps]

    for step, eps in zip(steps, eps_list):
        print(f"\nCURRENT EPSILON: {step}/255")
        eps_key = f"{step}/255"
        results[eps_key] = {}

        x_cache = {}
        y_cache = {}

        for name, model in models.items():
            dev = device_for_model(name)

            # move model to correct device
            model = model.to(dev).eval()
            move_operations_to_device(model, dev)

            # move data on device
            if dev not in x_cache:
                x_cache[dev] = x_test_cpu.to(dev)
                y_cache[dev] = y_test_cpu.to(dev)
            x = x_cache[dev]
            y = y_cache[dev]

            print(f"\ntesting {name} on {dev}")
            start = time.perf_counter()

            acc = robust_acc_autoattack(
                model, x, y, eps,
                device=dev,
                mode=mode,
                bs=batch_size,
                verbose=verbose
            )

            end = time.perf_counter()
            h, m, s = compute_elapsed_time(start, end)

            results[eps_key][name] = {
                "robust_acc": acc,
                "device": dev,
                "time_s": float(end - start),
                "mode": mode,
                "bs": batch_size
            }

            print(f"eps={step:>2d}/255  {name}: {acc:.3f}")
            print(f"elapsed time for {name}: {h:02d}:{m:02d}:{s:02d}")

    return results


def compute_autoattacks(models: dict, samples: int = 200, seeds: int = 0, batch_size: int = 50, mode: str = "standard",
                        steps: list = None, verbose: bool = True, out_file_name: str = "results") -> dict:
    """
    Wrapper for computing AutoAttack over the selected models and saving results.
    This function loads the models and a subset of tje CIFAR-10 dataset. Runs Auto attack
    for different epsilon values (1/255, 4/255, 8/255, 12/255, 16/255) amd saves tje resulting metrics
    in .json and csv format.

    Inputs:
    - models: dictionary whose keys are RobustBench model names. (Values are not used.)
    - samples: number of CIFAR-10 test samples to evaluate.
    - seeds: random seed for selecting the dataset subset.
    - batch_size: batch size used during AutoAttack evaluation.
    - mode: AutoAttack mode (fast, untargeted, targeted, standard).
    - verbose: whether AutoAttack should print progress/details.
    - out_file_name: base name/path used by `save_results` when writing outputs.

    Output:
    - results: nested dictionary returned by `autoattack_models` containing robust accuracy
      and timing information for each (epsilon, model) pair.

    """
    model_names = [name for name in models.keys()]
    models = load_models(model_names)
    x_test, y_test = load_data(dataset_samples=samples, seed=seeds, batch_size=batch_size)
    results = autoattack_models(
        models,
        x_test_cpu=x_test,
        y_test_cpu=y_test,
        batch_size=batch_size,
        mode=mode,
        steps=steps,
        verbose=verbose
    )

    save_results(results, out_file_name)
    return results
