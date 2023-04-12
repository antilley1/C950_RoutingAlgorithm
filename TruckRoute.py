from Package import Package
from Data import Data


# TruckRoute class keeps track and determines the routes the trucks will take
class TruckRoute:
    def __init__(self, truck_id, data: Data, package_list):

        self.packages_loaded = 0
        self.MAX_PACKAGES = 16
        self.MPH = 18
        self.MILES_PER_MINUTE = self.MPH / 60
        self.data = data
        self.at_hub = False
        self.truck_id = truck_id
        self.route = Route(self.data)
        self.package_list = package_list

        # upon initialization, truck determines route from package_list
        self.determine_route()
        self.distance_traveled = 0.0
        self.distance_to_next_address = data.get_distance_between("HUB", self.route.head.address)

    # returns distance traveled on this route
    # O(1)
    def get_distance_traveled(self):
        return self.distance_traveled

    # returns distance to next address
    # O(1)
    def get_distance_to_next_address(self):
        return self.distance_to_next_address

    # keeps track of where the truck is and if it has reached its next destination
    # if the destination is reached, the truck will have a new address to go to
    # if the truck reaches the end of the route, the at_bub attribute is updated accordingly
    # O(N)
    def increment(self, current_time):
        # increment distance
        self.distance_to_next_address -= self.MILES_PER_MINUTE
        self.distance_traveled += self.MILES_PER_MINUTE

        if not self.at_hub and not self.route.tail.visited:
            if self.distance_to_next_address <= 0.0:
                self.route.visit_next(current_time)
                if self.route.curr is not self.route.tail:
                    next_address = self.route.curr.next.address
                else:
                    next_address = "HUB"
                current_address = self.route.curr.address
                self.distance_to_next_address += self.data.get_distance_between(current_address, next_address)  # O(N)
        elif self.route.tail.visited and self.distance_to_next_address <= 0.0 and not self.at_hub:
            self.at_hub = True
            # print("Truck", self.id, "at HUB at", current_time)

    # dynamically determines route based on given package list using nearest neighbor algorithm
    # O(N)
    def determine_route(self):
        p: Package
        p = self.route.append(self.data.find_nearest_to_hub(self.package_list))  # O(N)
        self.package_list.pop(self.package_list.index(p))
        while self.package_list:  # O(16N)
            p_address = p.get_address()
            p = self.route.append(self.data.find_nearest_in(p_address, self.package_list))  # O(N)
            self.package_list.pop(self.package_list.index(p))

        self.route.curr = self.route.head


# RouteNode contains relational data for each package along the Route
class RouteNode:
    def __init__(self, package: Package):
        self.route_id = None
        self.package_id = package.get_id()
        self.address = package.get_address()
        self.next = None
        self.prev = None
        self.visited = False
        package.status = "En Route"


# Route is a linked list to keep track of the route the truck will take
class Route:
    def __init__(self, data: Data, head_node: RouteNode = None):
        self.head: RouteNode = head_node
        self.tail: RouteNode = head_node
        self.curr = None
        self.length = 0.0
        self.data = data
        self.finished = False

    # O(1)
    def print(self):
        print("Truck Route:")
        curr_node = self.head
        while curr_node:
            print("[", curr_node.package_id, ",", curr_node.address, "]")
            curr_node = curr_node.next

    # appends new node to tail
    # points tail to new node
    # O(1)
    def append(self, package: Package):
        new_node = RouteNode(package)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return package

    # sets curr to the next unvisited node
    # marks that node as visited
    # O(N)
    def visit_next(self, current_time):
        if self.curr.visited and self.curr.next:
            self.curr = self.curr.next
        self.curr.visited = True
        p: Package = self.data.lookup_package(self.curr.package_id)  # O(N)
        p.unload_package(current_time)
        return self.curr.package_id

    # returns length of route
    # O(N)
    def sum_length(self):
        if self.length == 0.0:
            curr_node = self.head
            self.length += self.data.get_distance_between("HUB", self.head.address)  # O(N)
            while curr_node.next:
                self.length += self.data.get_distance_between(curr_node.address, curr_node.next.address)
                curr_node = curr_node.next
            self.length += self.data.get_distance_between(curr_node.address, "HUB")
        return self.length
