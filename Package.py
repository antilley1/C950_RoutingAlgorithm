import datetime


# Package class holds all data retrieved from package_data.csv
class Package:
    def __init__(
            self,
            package_id=0,
            address='',
            city='',
            state='',
            zipcode='00000',
            deadline='',
            weight=0,
            note='',
            status='At Hub',
            delivery_time= -1):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.delivery_time = delivery_time

    def get_address(self): return self.address

    def set_address(self, new_address): self.address = new_address

    def get_id(self): return self.id

    def get_note(self): return self.note

    def get_delivery_time(self): return self.delivery_time

    def get_status(self): return self.status

    def get_deadline(self): return self.deadline

    def load_package(self): self.status = "At hub"

    # marks package as delivered at the time given
    def unload_package(self, delivery_time: datetime.datetime):
        self.status = "Delivered at " + datetime.datetime.strftime(delivery_time, "%H:%M")
        self.delivery_time = delivery_time

    # when truck is initialized, the status is set as seen below
    def takeoff(self, truck_num): self.status = "En route on Truck " + str(truck_num)
