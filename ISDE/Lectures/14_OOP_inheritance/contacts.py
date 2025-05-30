class contact:

    def __init__(self, first_name, email):
        self._first_name = first_name
        self._email = email

    def who_am_i(self):
        phone = getattr(self, '_phone_number', "N/A")
        print("\nNAME:", self._first_name, "\nPHONE:", phone, "\nEMAIL:", self._email, "\n")

    @property
    def name(self):
        return self._first_name

    @property
    def email(self):
        return self._email

    @name.setter
    def name(self, new_name):
        self._first_name = new_name

    @email.setter
    def email(self, new_email):
        self._email = new_email


class supplier(contact):
    def __init__(self, first_name, email):
        super().__init__(first_name, email)

    def order(self):
        print("an order has been made")


class friend(contact):

    def __init__(self, name, email, phone_number):
        super().__init__(name, email)
        self._phone_number = phone_number

    @property
    def phone(self):
        return self._phone_number

    @phone.setter
    def phone(self, new_phone):
        self._phone_number = new_phone


c = contact("pippo", "pippo@gmail.com")
c.who_am_i()
s = supplier("Angelo", "angelogreco@gmail.com")
s.who_am_i()
s.order()
f = friend("gianni", "giannisperti@gmail.com", "3425763028")
f.who_am_i()
