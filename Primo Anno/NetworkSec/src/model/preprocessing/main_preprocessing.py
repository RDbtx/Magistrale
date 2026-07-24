from filtering import filtering
from scaling import scaling
from labeling import labeling
from dataset_regenerator import dataset_regenerator
import pathlib
import os

# =====================================
# ---         Configuration         ---
# =====================================

ROOT_DIR = pathlib.Path(__file__).parent.parent
ORIGINAL_DATASET_DIR = os.path.join(ROOT_DIR, "dataset")
REGENERATED_DATASET_DIR = os.path.join(ROOT_DIR, "new_dataset")

# =====================================
# ---       Main Execution          ---
# =====================================

if __name__ == "__main__":
    print("Starting dataset regeneration")
    dataset_regenerator()  # directly extracts data from the pcap file using the same extractor as the firewall

    print("\nStarting preprocessing...\n")
    labeling(REGENERATED_DATASET_DIR)  # adds Label to raw CSVs
    output = filtering(REGENERATED_DATASET_DIR)  # merges labeled CSVs, returns path
    scaling(output)  # scales and encodes, saves final CSV
    print("\nFinished!")
