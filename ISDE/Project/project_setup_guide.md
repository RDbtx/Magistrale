# Brief Guide to Setting Up the Project

Since I found the project setting process a bit frustrating, I want to give you a brief guide on how to do it.

## 1. Cloning the Repository

The first thing you want to do is to open **PyCharm** and clone this Git repository on your computer. **Do not** create
a project first and then download it inside because PyCharm will create different nested project folders that will
interfere with the original project path.

Since we should focus on the Python code of the original project, I suggest you avoid this mistake.

## 2. Expected Folder Structure

After cloning the repository, you should have a folder structured like this:

```
project_root/
│── .venv
│── app/
│   ├── forms/
│   ├── ml/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── config.py
│   ├── prepare_images.py
│   ├── prepare_models.py
│   ├── utils.py
│── .gitignore
│── main.py
│── README.md
│── requirements.txt
│── External Libraries
│── Scratches and Consoles
```

## 3. Setting Up a Virtual Environment

The professor suggests using **Conda** as a virtual environment, but if you don't want to spend time installing it, the
local one with `venv` should be fine.

If you don’t have a `.venv` folder in your project, you **won’t** be able to install packages or run the project files.
To set up an interpreter, follow these steps:

1. Open **PyCharm** and go to **File** → **Settings** → **Python Interpreter**.
2. Click **Add Interpreter** → **Add Local Interpreter** → **OK**.

Once you do this, a `venv` folder should be created inside your project. **Make sure not to upload it to the Git
repository** whenever you pull changes, as it contains system-specific paths.

## 4. Installing Dependencies

After setting up the virtual environment, install the required dependencies by running:

```
pip install -r requirements.txt
```

Alternatively, **PyCharm might suggest missing packages** with a yellow notification in the top-left corner of the
screen. Just click the **Install** button, and this step won't be necessary.

## 5. Running the Project

Once everything is set up, run the following commands in the terminal:

```
python app/prepare_images.py
python app/prepare_models.py
```

or

```
python -m app.prepare_images.py
python -m app.prepare_models.py
```
Since, for some reason, Sphinx was not satisfied with
the `from config import Configuration` statement in those files,
we had to modify it to `from .config import Configuration`.
However, this change may cause issues when running the previous commands,
so the use of the other two is recommended.

After that, check if `uvicorn` is installed:

```
pip list 
```

If it is not present on the output list, install uvicorn with:

```
pip install uvicorn
```

Since **FastAPI** is already installed, start the project using:

```
uvicorn main:app --reload
```

After this, the project will be hosted locally at:

```
127.0.0.7
```

Just open your web browser and enter this IP to access the project.

## 6. Viewing the Web Interface

You will see the following page:

![image](https://github.com/user-attachments/assets/90653c98-3e9e-40cc-a2c5-2dee562113cf)
The project will be completely written in **JavaScript**, and we **do not** need to modify or run any `.py` files.

Every modification will be reflected on your **localhost**, so if you want to test your code, simply open your web
browser and check your local server.

---

I hope that this guide will be helpful to you!
