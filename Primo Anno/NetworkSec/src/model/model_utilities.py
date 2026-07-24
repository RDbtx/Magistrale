import time
import os
import joblib
import numpy as np
import pandas as pd
from performances import model_performances_multiclass, model_performances_report_generation
from sklearn.preprocessing import LabelEncoder

# =====================================
# ---         Configuration         ---
# =====================================

LABELS = [
    "Normal",
    "http-flood",
    "fuzzing",
    "http-loris",
    "quic-flood",
    "quic-loris",
    "quic-enc",
    "http-smuggle",
    "http2-concurrent",
    "http2-pause"
]


# =====================================
# ---    Dual Model Architecture    ---
# =====================================

# Dual-model architecture: one model per protocol family.
#
# Root cause of previous failures: each attack label contained packets from
# both QUIC-capable servers (caddy, h2o, litespeed, cloudflare — pure QUIC)
# and TCP-only servers (nginx, windows — pure TCP). After MinMax scaling these
# two groups land in completely different regions of the feature space, so a
# single model cannot learn a clean boundary for any mixed-protocol class.
#
# Solution: split the dataset by protocol BEFORE training.
# Routing at inference time: quic.packet_length > 0 → QUIC model, else TCP model.

def split_by_protocol(df: pd.DataFrame) -> tuple:
    """
    Splits the DataFrame into QUIC and TCP subsets by checking whether any of the
    core QUIC indicator columns contain a non-null, positive value.
    A row is considered QUIC only if at least one core indicator is present and greater than 0.

    Input:
    - df: Full dataset DataFrame containing both QUIC and TCP rows.

    Outputs:
    - quic_df: DataFrame containing only QUIC rows.
    - tcp_df: DataFrame containing only TCP rows.

    """
    core_quic_indicators = [
        'quic.packet_length',
        'quic.length',
        'quic.nci.connection_id.length'
    ]

    available_indicators = [c for c in core_quic_indicators if c in df.columns]
    quic_mask = (df[available_indicators].fillna(0) > 0).any(axis=1)

    quic_df = df[quic_mask].copy().reset_index(drop=True)
    tcp_df = df[~quic_mask].copy().reset_index(drop=True)

    print(f"Protocol split → QUIC: {len(quic_df):,} rows  |  TCP: {len(tcp_df):,} rows")
    return quic_df, tcp_df


def extract_data(df: pd.DataFrame) -> tuple:
    """
    Splits the full dataset by protocol, then fits a LabelEncoder on each subset
    and encodes the Label column in place.

    Input:
    - df: Full dataset DataFrame containing a Label column and both QUIC and TCP rows.

    Outputs:
    - quic_df: QUIC subset with encoded Label column.
    - tcp_df: TCP subset with encoded Label column.
    - quic_encoder: Fitted LabelEncoder for the QUIC branch.
    - tcp_encoder: Fitted LabelEncoder for the TCP branch.
    - quic_labels_names: Ordered list of class names for the QUIC branch.
    - tcp_labels_names: Ordered list of class names for the TCP branch.

    """
    quic_df, tcp_df = split_by_protocol(df)

    quic_encoder = LabelEncoder()
    tcp_encoder = LabelEncoder()

    quic_df["Label"] = quic_encoder.fit_transform(quic_df["Label"])
    quic_labels_names = list(quic_encoder.classes_)

    tcp_df["Label"] = tcp_encoder.fit_transform(tcp_df["Label"])
    tcp_labels_names = list(tcp_encoder.classes_)

    print(f"[QUIC-model] Classes ({len(quic_labels_names)}): {quic_labels_names}")
    print(f"[TCP-model] Classes ({len(tcp_labels_names)}): {tcp_labels_names}")

    return quic_df, tcp_df, quic_encoder, tcp_encoder, quic_labels_names, tcp_labels_names


# =====================================
# ---    Main Utility Functions     ---
# =====================================

def load_df(csv_file: str) -> pd.DataFrame:
    """
    Loads a CSV file and returns it as a raw DataFrame.

    Inputs:
    - csv_file: Path to the CSV file to load.

    Output:
    - df: Loaded DataFrame.

    """
    print("Loading dataset...")
    df = pd.read_csv(csv_file, low_memory=False)
    print(f"Total rows loaded: {len(df):,}")
    return df


def save_model(model, encoder: LabelEncoder, model_name: str) -> None:
    """
    Saves a trained model and its associated LabelEncoder to disk as a joblib file
    under the output/saved_models/ directory.

    Inputs:
    - model: Trained classifier instance to save.
    - encoder: Fitted LabelEncoder associated with the model.
    - model_name: Name used to identify the saved file.

    """
    models_dir = "output/saved_models/"
    os.makedirs(models_dir, exist_ok=True)
    save_path = models_dir + f"{model_name}_classifier.joblib"
    joblib.dump({"model": model, "encoder": encoder}, save_path)
    print(f"Model saved to {save_path}")


def model_train(model, labels_names: list, x: np.ndarray, y: np.ndarray, model_name: str) -> tuple:
    """
    Trains the model on the provided data and evaluates performance on the training set.

    Inputs:
    - model: Untrained classifier instance.
    - labels_names: Ordered list of class name strings.
    - x: Feature matrix used for training.
    - y: Label array used for training.
    - model_name: Name of the model, used for reporting.

    Outputs:
    - model: Trained classifier instance.
    - train_predictions: Predicted class indices on the training set.

    """
    print(f"\n----{model_name} TRAINING STARTED----")
    train_time = time.time()
    model.fit(x, y)
    print(f"Training time: {(time.time() - train_time):.1f} s")
    print(f"----{model_name} TRAINING COMPLETED----\n")

    print("Computing training predictions...")
    pred_time = time.time()
    train_predictions = model.predict(x)
    train_probabilities = model.predict_proba(x)
    print(f"Prediction time: {(time.time() - pred_time):.1f} s")

    accuracy, precision, recall, f1_macro, f1_micro, auc, class_report, cm = \
        model_performances_multiclass(labels_names, y, train_predictions,
                                      train_probabilities, "TRAINING", model_name)
    model_performances_report_generation(accuracy, precision, recall, f1_macro, f1_micro,
                                         auc, class_report, cm, "TRAINING", model_name)
    return model, train_predictions


def model_test(model, labels_names: list, x: np.ndarray, y: np.ndarray, model_name: str) -> np.ndarray:
    """
    Evaluates a trained model on the test set and saves a performance report.

    Inputs:
    - model: Trained classifier instance.
    - labels_names: Ordered list of class name strings.
    - x: Feature matrix used for testing.
    - y: Label array used for testing.
    - model_name: Name of the model, used for reporting.

    Output:
    - test_predictions: Predicted class indices on the test set.

    """
    print(f"\n----{model_name} TESTING----")
    test_time = time.time()
    test_predictions = model.predict(x)
    test_probabilities = model.predict_proba(x)
    print(f"Test time: {(time.time() - test_time):.1f} s")
    print(f"----{model_name} TESTING COMPLETED----\n")

    accuracy, precision, recall, f1_macro, f1_micro, auc, class_report, cm = \
        model_performances_multiclass(labels_names, y, test_predictions,
                                      test_probabilities, "TESTING", model_name)
    model_performances_report_generation(accuracy, precision, recall, f1_macro, f1_micro,
                                         auc, class_report, cm, "TESTING", model_name)
    return test_predictions
