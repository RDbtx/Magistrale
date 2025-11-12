import os

project_root = os.path.dirname(os.path.abspath(__file__))


class Configuration:
    """
        Contains the configuration information for the app.

        This class holds the paths and model configurations required by the app
        for image classification and file management. It provides default values
        for the image folder path, upload folder path, and a list of pre-defined
        models used for image classification tasks.

        Attributes
        ----------
        image_folder_path : str
            The file path to the folder containing image datasets.
        upload_folder_path : str
            The file path to the folder where uploaded images are stored.
        models : tuple of str
            A tuple containing the names of the pre-defined models used for
            image classification.
        """

    # classification
    image_folder_path = os.path.join(project_root, "static/imagenet_subset")
    upload_folder_path = os.path.join(project_root, "static/uploads")
    edit_folder_path = os.path.join(project_root, "static/edited")
    models = (
        "resnet18",
        "alexnet",
        "vgg16",
        "inception_v3",
    )
