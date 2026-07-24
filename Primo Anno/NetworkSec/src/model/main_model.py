import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
import pathlib
import os

from model_utilities import (
    model_train, model_test, save_model,
    extract_data, load_df, LABELS
)

# =====================================
# ---         Configuration         ---
# =====================================

MODEL_DIR = pathlib.Path(__file__).parent
ORIGINAL_DATASET = os.path.join(MODEL_DIR, "dataset/pcap-all-final.csv")
REGENERATED_DATASET = os.path.join(MODEL_DIR, "new_dataset/pcap-all-final.csv")


# =====================================
# ---    Model Factory Functions    ---
# =====================================

def make_xgboost(num_class: int) -> xgb.XGBClassifier:
    return xgb.XGBClassifier(
        objective="multi:softmax",
        num_class=num_class,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=7,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        n_jobs=-1,
        random_state=42,
    )


def make_lgbm(num_class: int) -> lgb.LGBMClassifier:
    return lgb.LGBMClassifier(
        objective='multiclass',
        num_class=num_class,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=7,
        num_leaves=63,
        subsample=0.8,
        colsample_bytree=0.8,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1,
        verbose=0,
    )


def make_random_forest() -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=500,
        max_depth=7,
        min_samples_split=20,
        min_samples_leaf=10,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )


# =====================================
# ---    Train One Model Branch     ---
# =====================================

def train_branch(df: pd.DataFrame, encoder: LabelEncoder, labels_names: list, model_name: str) -> None:
    """
    Splits the data into train/test sets, trains an XGBoost model, evaluates it,
    and saves the model and encoder to disk.

    Inputs:
    - df: Preprocessed DataFrame with an encoded Label column.
    - encoder: Fitted LabelEncoder for this protocol branch.
    - labels_names: Ordered list of decoded class name strings.
    - model_name: Identifier for this branch, e.g. 'XGB_Blackwall_TCP'.

    """
    X = df.drop("Label", axis=1).values
    Y = df["Label"].values

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.4, stratify=Y, random_state=42
    )

    print(f"\n{'=' * 50}")
    print(f"  {model_name}")
    print(f"  Classes ({len(labels_names)}): {labels_names}")
    print(f"  x_train: {x_train.shape}  |  x_test: {x_test.shape}")
    print(f"{'=' * 50}")

    num_class = len(labels_names)
    model = make_xgboost(num_class)
    # Uncomment to use LightGBM or Random Forest instead:
    # model = make_lgbm(num_class)
    # model = make_random_forest()

    trained_model, _ = model_train(model, labels_names, x_train, y_train, model_name)
    model_test(trained_model, labels_names, x_test, y_test, model_name)
    save_model(trained_model, encoder, model_name)


# =====================================
# ---       Training Pipelines      ---
# =====================================

def single_model_training(dataset: str) -> None:
    """
    Trains a single model on the entire dataset without protocol splitting.

    Inputs:
    - dataset: Path to the preprocessed CSV file.
    """
    print("\n" + "=" * 60)
    print("  BLACKWALL — Single-Model Training")
    print("=" * 60)

    dataframe = load_df(dataset)

    encoder = LabelEncoder()
    dataframe["Label"] = encoder.fit_transform(dataframe["Label"])
    labels_names = list(encoder.classes_)

    train_branch(dataframe, encoder, labels_names, "XGB_Blackwall")
    print("\n\nDone. Models saved to output/saved_models/")


def double_model_training(dataset: str) -> None:
    """
    Trains two separate models using the dual-model architecture:
    one for TCP traffic and one for QUIC traffic.

    Inputs:
    - dataset: Path to the preprocessed CSV file.
    """
    print("\n" + "=" * 60)
    print("  BLACKWALL — Dual-Model Training")
    print("  TCP model  : processes packets with no quic parameters ")
    print("  QUIC model : processes packets with quic parameters ")
    print("=" * 60)

    dataframe = load_df(dataset)
    quic_df, tcp_df, quic_encoder, tcp_encoder, quic_labels, tcp_labels = extract_data(dataframe)

    print("\n>>> BRANCH 1/2 — TCP MODEL")
    train_branch(tcp_df, tcp_encoder, tcp_labels, "XGB_Blackwall_TCP")

    print("\n>>> BRANCH 2/2 — QUIC MODEL")
    train_branch(quic_df, quic_encoder, quic_labels, "XGB_Blackwall_QUIC")
    print("Done. Models saved to output/saved_models/")


# =====================================
# ---       Main Execution          ---
# =====================================

if __name__ == "__main__":
    single_model_training(REGENERATED_DATASET)
