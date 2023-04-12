import csv
import datetime

from Package import Package


# populate address list with data from address_list.csv
# O(N)
def populate_address_list(address_list):
    with open('address_list.csv', mode='r', encoding='utf-8-sig') as address_file:
        address_reader = csv.reader(address_file, delimiter=',')
        for row in address_reader:
            address_list.append(row[0])


# populate distance table with data from distance_data.csv
# O(N)
def populate_distance_table(distance_table):
    with open('distance_data.csv', mode='r', encoding='utf-8-sig') as distance_file:
        distance_reader = csv.reader(distance_file, delimiter=',')
        for row in distance_reader:
            distance_table.append(row)


# populate hash table with data from package_data.csv
# O(N)
def populate_hash_table(hash_table):
    with open('package_data.csv', mode='r', encoding='utf-8-sig') as package_file:
        package_reader = csv.reader(package_file, delimiter=',')
        for row in package_reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = int(row[6])
            note = row[7]
            p = Package(package_id, address, city, state, zipcode, deadline, weight, note)
            insert_package_into_hash_table(p, hash_table)


# inserts Package object into hash_table
# O(N)
def insert_package_into_hash_table(package: Package, hash_table):
    # determine bucket
    bucket = hash(package.get_id()) % len(hash_table)
    bucket_list = hash_table[bucket]

    # insert
    bucket_list.append([package.get_id(), package])


# Data class handles all data about packages, locations, and distances
class Data:
    # initializes Data class
    # O(N)
    def __init__(self):
        self.address_list = []
        self.distance_table = []
        self.hash_table = []

        for i in range(10):
            self.hash_table.append([])
        populate_address_list(self.address_list)
        populate_distance_table(self.distance_table)
        populate_hash_table(self.hash_table)

        self.package_list1 = []
        self.package_list2 = []
        self.package_list3 = []

    # Given a package ID, return that package
    # O(N)
    def lookup_package(self, package_id) -> Package or None:
        # get bucket
        package_id = int(package_id)
        bucket = hash(package_id) % len(self.hash_table)
        bucket_list = self.hash_table[bucket]

        # search for key_value in bucket list
        # key_value is [package_id, package]
        for key_value in bucket_list:
            if key_value[0] == package_id:
                return key_value[1]
        return None

    # returns the list of all addresses
    # O(1)
    def get_address_list(self): return self.address_list

    # given two packages, returns the distance between them
    # O(N)
    def get_distance_between_packages(self, package1: Package, package2: Package):

        address1 = package1.get_address()  # O(1)
        address2 = package2.get_address()
        address1_index = self.address_list.index(address1)  # O(N)
        address2_index = self.address_list.index(address2)

        # O(1)
        if self.distance_table[address1_index][address2_index]:
            return float(self.distance_table[address1_index][address2_index])
        else:
            return float(self.distance_table[address2_index][address1_index])

    # given two address, returns the distannce between them
    # O(N)
    def get_distance_between(self, address1, address2):
        address1_index = self.address_list.index(address1)  # O(N)
        address2_index = self.address_list.index(address2)

        # O(1)
        if self.distance_table[address1_index][address2_index]:
            return float(self.distance_table[address1_index][address2_index])
        else:
            return float(self.distance_table[address2_index][address1_index])

    # given a package, returns the distance between it and the HUB
    # O(N)
    def get_distance_from_hub(self, package: Package):
        return self.get_distance_between("HUB", package.get_address())

    # given a package, it searches the hash_table for that package and removes it
    # O(N)
    def remove_package_from_hash_table(self, package: Package):
        # get bucket
        package_id = int(package.get_id())
        bucket = hash(package_id) % len(self.hash_table)
        bucket_list = self.hash_table[bucket]

        # remove item from bucket if present
        for key_value in bucket_list:
            if key_value[0] == package_id:
                bucket_list.remove(key_value)

    # given an address and a list of packages,
    # returns the nearest package
    # O(N)
    def find_nearest_in(self, current_address, package_list: {Package}) -> Package:
        current_index = self.get_address_list().index(current_address)  # O(N)

        nearest_package: Package() = None
        smallest_distance = 1000
        for package in package_list:
            address = package.get_address()
            address_index = self.get_address_list().index(address)  # O(N)
            if int(address_index) < current_index:
                if float(self.distance_table[current_index][address_index]) < smallest_distance:
                    nearest_package = package
                    smallest_distance = float(self.distance_table[current_index][address_index])
            elif int(address_index) > current_index:
                if float(self.distance_table[address_index][current_index]) < smallest_distance:
                    nearest_package = package
                    smallest_distance = float(self.distance_table[address_index][current_index])
            elif int(address_index) == current_index:
                nearest_package = package
                smallest_distance = 0

        return nearest_package

    # given a list of packages,
    # returns the package nearest to the HUB
    # O(N)
    def find_nearest_to_hub(self, package_list: [Package]):
        return self.find_nearest_in("HUB", package_list)

    # given a package and a package list,
    # calls load_package for packages at the same address as the given package
    # O(N)
    # this method and load_package call each other,
    # but the calls are limited to the number of packages,
    # so the methods scale linearly with the number of packages
    def get_packages_at_same_address(self, package: Package, package_list):
        package_address = package.get_address()
        for bucket in self.hash_table:
            for key_value in bucket:
                _package: Package = key_value[1]
                _package_address = _package.get_address()
                _package_status = _package.get_status()
                if package_address == _package_address and _package_status == "At Hub":
                    self.load_package(_package, package_list)

    # given a package and a package_list, the package is appended to the package list, if not already in it
    # the package status is updated with the load_package method
    # O(N)
    # this method and get_packages_at_same_address call each other,
    # but the calls are limited to the number of packages,
    # so the methods scale linearly with the number of packages
    def load_package(self, package: Package, package_list):
        if len(package_list) >= 16:
            pass
        elif package_list is self.package_list1 and package not in self.package_list1:
            package.load_package()
            self.package_list1.append(package)
            self.get_packages_at_same_address(package, self.package_list1)
        elif package_list is self.package_list2:
            package.load_package()
            self.package_list2.append(package)
            self.get_packages_at_same_address(package, self.package_list2)
        elif package_list is self.package_list3:
            package.load_package()
            self.package_list3.append(package)
            self.get_packages_at_same_address(package, self.package_list3)

    # called in main.py
    # creates the package lists for the trucks by calling their respective function
    # O(N^2)
    def determine_package_lists(self):
        # O(N)
        self.determine_first_package_list()
        self.determine_third_package_list()
        self.determine_second_package_list()

        # O(N^2)
        self.package_list1 = self.fill_route(self.package_list1, "HUB")
        self.package_list3 = self.fill_route(self.package_list3, "HUB")
        self.package_list2 = self.fill_route(self.package_list2, "HUB")

    # appends packages into package_list1
    # packages that must be delivered together
    # O(N)
    def determine_first_package_list(self):
        # print("Determining first list")
        for bucket in self.hash_table:
            for key_value in bucket:
                _package: Package = key_value[1]
                _package_note = _package.get_note()
                must_be_id_list = [13, 15, 19]
                _package_id = _package.get_id()
                if ("Must be" in _package_note) or (_package_id in must_be_id_list):
                    self.load_package(_package, self.package_list1)

    # appends packages into package_list2
    # packages that must be on truck 2
    # O(N)
    def determine_second_package_list(self):
        # print("Determining third list")
        for bucket in self.hash_table:
            for key_value in bucket:
                _package: Package = key_value[1]
                _package_id = _package.get_id()
                _package_note = _package.get_note()
                if "truck 2" in _package_note:
                    self.load_package(_package, self.package_list2)

    # appends packages into package_list3
    # packages that have been delayed
    # O(N)
    def determine_third_package_list(self):
        # print("Determining second list")
        for bucket in self.hash_table:
            for key_value in bucket:
                _package: Package = key_value[1]
                _package_note = _package.get_note()
                _package_id = _package.get_id()
                _package_deadline = _package.get_deadline()
                if "Delayed" in _package_note:
                    # self.package_list2.append(_package_id)
                    self.load_package(_package, self.package_list3)

    # given a package list and a starting address
    # appends the closest packages to the package list
    # until the package list has 16 packages or there are no more packages
    # O(N^2)
    def fill_route(self, package_list, starting_address):
        current_index = self.address_list.index(starting_address)

        while len(package_list) < 16:
            nearest_index = -1
            nearest_distance = 100
            closest_package_id = -1

            # O(N)
            for bucket in self.hash_table:
                for key_value in bucket:
                    _package: Package = key_value[1]
                    _package_address = _package.get_address()
                    _package_address_index = self.address_list.index(_package_address)
                    _package_id = _package.get_id()
                    _package_status = _package.get_status()
                    _package_note = _package.get_note()
                    _package_deadline = _package.get_deadline()
                    if _package_id not in package_list and _package_status == "At Hub":
                        if package_list is self.package_list1:
                            if "10:30" in _package_deadline:
                                if int(_package_address_index) < current_index:
                                    if float(self.distance_table[current_index][
                                                 _package_address_index]) < nearest_distance:
                                        nearest_index = _package_address_index
                                        nearest_distance = float(
                                            self.distance_table[current_index][_package_address_index])
                                        closest_package_id = _package_id
                                elif int(_package_address_index) > current_index:
                                    if float(self.distance_table[_package_address_index][
                                                 current_index]) < nearest_distance:
                                        nearest_index = _package_address_index
                                        nearest_distance = float(
                                            self.distance_table[_package_address_index][current_index])
                                        closest_package_id = _package_id
                        else:
                            if int(_package_address_index) < current_index:
                                if float(self.distance_table[current_index][_package_address_index]) < nearest_distance:
                                    nearest_index = _package_address_index
                                    nearest_distance = float(self.distance_table[current_index][_package_address_index])
                                    closest_package_id = _package_id
                            elif int(_package_address_index) > current_index:
                                if float(self.distance_table[_package_address_index][current_index]) < nearest_distance:
                                    nearest_index = _package_address_index
                                    nearest_distance = float(self.distance_table[_package_address_index][current_index])
                                    closest_package_id = _package_id
                        # print(closest_package_id)
                        # print(nearest_distance)
            # print(self.package_list1)
            if closest_package_id == -1:
                break

            # O(N^2)
            if self.lookup_package(closest_package_id):  # O(N)
                self.load_package(self.lookup_package(closest_package_id), package_list)  # O(N)
                # print(self.package_list1)
                # package_list.append(closest_package_id)
                closest_package: Package = self.lookup_package(closest_package_id)
                closest_package.load_package()
                current_index = nearest_index

        return package_list

    # prints package info in package ID order
    # O(N^2)
    def print_all(self):
        p_id = 1
        while self.lookup_package(p_id):  # O(N)
            p: Package = self.lookup_package(p_id)
            p_address = p.get_address()
            p_city = p.city
            p_state = p.state
            p_zip = p.zipcode
            p_deadline = p.get_deadline()
            p_weight = p.weight
            p_note = p.get_note()
            p_delivery = p.get_delivery_time()
            p_status = p.get_status()
            print("ID:", p_id, end="   |   ")
            print("Address:", p_address + ",", p_city + ",", p_state, p_zip, end="   |   ")
            print("Deadline:", p_deadline, end="   |   ")
            print("Weight:", p_weight, end="   |   ")
            print("Note:", p_note, end="   |   ")
            # if p_delivery != -1:
            #     print("Delivery:", datetime.datetime.strftime(p_delivery, "%H:%M"), end=" | ")
            # else:
            #     print("Delivery: Not Delivered", end="   |   ")
            print("Status:", p_status)
            p_id += 1

    # prints package info by bucket
    # O(N)
    def print_all_by_bucket(self):
        for bucket in self.hash_table:
            for key_value in bucket:
                p: Package = key_value[1]
                p_id = p.get_id()
                p_address = p.get_address()
                p_city = p.city
                p_state = p.state
                p_zip = p.zipcode
                p_deadline = p.get_deadline()
                p_weight = p.weight
                p_note = p.get_note()
                p_delivery = p.get_delivery_time()
                p_status = p.get_status()
                print("ID:", p_id, end="   |   ")
                print("Address:", p_address + ",", p_city + ",", p_state, p_zip, end="   |   ")
                print("Deadline:", p_deadline, end="   |   ")
                print("Weight:", p_weight, end="   |   ")
                print("Note:", p_note, end="   |   ")
                # if p_delivery != -1:
                #     print("Delivery:", datetime.datetime.strftime(p_delivery, "%H:%M"), end=" | ")
                # else:
                #     print("Delivery: Not Delivered", end=" | ")
                print("Status:", p_status)

    # prints specific package info
    # O(N)
    def print_package(self, p_id):
        if self.lookup_package(p_id):
            p = self.lookup_package(p_id)  # O(N)
            p_address = p.get_address()
            p_city = p.city
            p_state = p.state
            p_zip = p.zipcode
            p_deadline = p.get_deadline()
            p_weight = p.weight
            p_note = p.get_note()
            p_delivery = p.get_delivery_time()
            p_status = p.get_status()
            print("ID:", p_id, end="   |   ")
            print("Address:", p_address + ",", p_city + ",", p_state, p_zip, end="   |   ")
            print("Deadline:", p_deadline, end="   |   ")
            print("Weight:", p_weight, end="   |   ")
            print("Note:", p_note, end="   |   ")
            # if p_delivery != -1:
            #     print("Delivery:", datetime.datetime.strftime(p_delivery, "%H:%M"), end=" | ")
            # else:
            #     print("Delivery: Not Delivered", end="   |   ")
            print("Status:", p_status)
        else:
            print("Requested package ID does not exist")
