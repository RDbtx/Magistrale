import json
import logging
import os
import shutil
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from .config import Configuration


def prepare_images():
    """
    Downloads a subset of the ImageNet Dataset if not already present.

    This function checks if the specified image folder exists. If not, it downloads a ZIP
    file containing a subset of the ImageNet dataset from a given URL. The ZIP file is
    extracted, and the images are stored in the configured image folder.

    Raises
    ------
    URLError
        If there is an issue downloading the dataset.
    IOError
        If there is an issue extracting or moving files.
    """
    img_folder = Configuration().image_folder_path
    if not os.path.exists(img_folder):
        zip_url = (
            "https://github.com/EliSchwartz/imagenet-sample-images/archive/master.zip"
        )
        try:
            with urlopen(zip_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(img_folder)
        except Exception as e:
            logging.error(f"Error downloading dataset: {e}")
            raise

    sub_dir = os.path.join(img_folder, "imagenet-sample-images-master")
    if os.path.exists(sub_dir):
        files = os.listdir(sub_dir)
        for f in files:
            shutil.move(os.path.join(sub_dir, f), img_folder)
        shutil.rmtree(sub_dir)

    logging.info(f"Images downloaded and stored in {img_folder}.")


def prepare_labels():
    """
    Saves a JSON file containing ImageNet labels as a list where
    the index is the label ID of the class.

    This function retrieves a JSON file containing simplified ImageNet labels,
    where the index of the list corresponds to the label ID of the class.
    The labels are downloaded from a public URL and saved to the specified
    image folder as "imagenet_labels.json".

    Raises
    ------
    requests.exceptions.RequestException
        If there is an issue retrieving the label file.
    IOError
        If there is an issue saving the JSON file.
    """
    img_folder = Configuration().image_folder_path
    labels_path = os.path.join(img_folder, "imagenet_labels.json")
    imagenet_labels_url = (
        "https://raw.githubusercontent.com/"
        "anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    )

    try:
        r = requests.get(imagenet_labels_url)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading labels: {e}")
        raise

    try:
        with open(labels_path, "w") as f:
            json.dump(data, f)
    except IOError as e:
        logging.error(f"Error saving labels: {e}")
        raise

    logging.info(f"Labels downloaded and stored in {labels_path}.")


if __name__ == "__main__":
    prepare_images()
    prepare_labels()
