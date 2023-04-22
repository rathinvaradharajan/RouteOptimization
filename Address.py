class Address:
    def __init__(self, street, apt, city, state, zip_code):
        self.street = street
        self.apt = apt
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.id = str(street) + " " + str(zip_code)

    def to_address_str(self):
        if self.apt != '':
            return f"{self.street}, Apt: {self.apt}, {self.city}, {self.state} {self.zip_code}"
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
