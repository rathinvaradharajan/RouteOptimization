class Address:
    def __init__(self, street, apt, city, state, zip_code):
        self.street = street
        self.apt = apt
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.id = str(street) + " " + str(zip_code)
