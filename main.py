# C950 Performance Assessment
# Martin Antilley
# ID 010353070


from Package import Package
from TruckRoute import TruckRoute
from Data import Data
import datetime

# important times
# makes the main thread easier to read
eight_am = datetime.datetime(2022, 1, 1, 8, 0)
nine_am = datetime.datetime(2022, 1, 1, 9, 0)
nine_o_five_am = datetime.datetime(2022, 1, 1, 9, 5)
ten_twenty_am = datetime.datetime(2022, 1, 1, 10, 20)
five_pm = datetime.datetime(2022, 1, 1, 18, 0)

# the start of the day
time = eight_am

# flags used to print different data for debugging
print_route = False
print_packages = True
annotate_route = False
input_mode = True
print_all = False
input_ID_int = None

# O(N^2)
if __name__ == '__main__':

    Data = Data()

    Data.lookup_package(9).status = "on hold"

    # Sorts the packages into multiple lists to be given to trucks
    # the order of the route is determined later
    Data.determine_package_lists()  # O(N^2)

    # placeholders for objects used in while loop below
    truck_route1 = None
    truck_route2 = None
    truck_route3 = None
    truck_route4 = None
    list1 = None
    list2 = None
    list3 = None
    list4 = None
    total_distance = 0.0

    if input_mode:
        display_str = "Please enter a package ID (or 'ALL' to view all packages): "
        input_ID = input(display_str)
        if input_ID == "ALL":
            print_all = True
            # print(input_time)
        else:
            if input_ID.isdigit():
                input_ID_int = int(input_ID)
            else:
                print("Invalid entry")
                print_all = False

        input_time = datetime.datetime.strptime(input('specify time in 24-hour HHMM format: '), "%H%M")
        input_time += datetime.timedelta(365 * 122 + 30)
    else:
        input_time = five_pm

    # the main thread that runs until the end of the day
    while time <= five_pm:
        p9: Package = Data.lookup_package(9)

        # at 8 am Truck 1 is sent
        if time == eight_am:
            if annotate_route:
                print(datetime.datetime.strftime(time, "%H:%M"), end=": ")
                print("Send truck 1")
            list1 = Data.package_list1.copy()
            truck_route1 = TruckRoute(1, Data, Data.package_list1)

        # at 9:05 truck 3 is sent
        if time == nine_o_five_am:
            if annotate_route:
                print(datetime.datetime.strftime(time, "%H:%M"), end=": ")
                print("Send truck 3")
            list3 = Data.package_list3.copy()
            truck_route3 = TruckRoute(3, Data, Data.package_list3)

        # if truck 1 has returned and truck 2 hasn't been initialized yet,
        # truck 2 is sent
        if truck_route1.at_hub and truck_route2 is None:
            if annotate_route:
                print(datetime.datetime.strftime(time, "%H:%M"), end=": ")
                print("Send truck 2")
            list2 = Data.package_list2.copy()
            truck_route2 = TruckRoute(2, Data, Data.package_list2)

        # at 10:20 the address for package 9 is corrected and loaded into a package list
        if time == ten_twenty_am:
            if annotate_route:
                print(datetime.datetime.strftime(time, "%H:%M"), end=": ")
                print("Package 9 address updated")
            p9.set_address("410 S State St")
            Data.load_package(p9, Data.package_list3)
            list4 = Data.package_list3.copy()

        # if truck 3 has returned to hub,
        # it will deliver package 9
        if truck_route3:
            if truck_route3.at_hub and p9.status == "At hub":
                if annotate_route:
                    print(datetime.datetime.strftime(time, "%H:%M"), end=": ")
                    print("Send truck 3 again")
                truck_route4 = TruckRoute(3, Data, Data.package_list3)

        # once all trucks have returned, the day is over
        if truck_route4:
            if truck_route1.at_hub and truck_route2.at_hub and truck_route3.at_hub and truck_route4.at_hub:
                print("Every package delivered and truck returned to hub at", datetime.datetime.strftime(time, "%H:%M"))
                break

        # update truck statuses before incrementing time or breaking out of while loop
        # determine truck distance to next location
        # decrement distance per 1 minute
        # if distance reaches 0
        # unload package and subtract remaining distance decrement to next trip
        if truck_route1:
            truck_route1.increment(time)
        if truck_route2:
            truck_route2.increment(time)
        if truck_route3:
            truck_route3.increment(time)
        if truck_route4:
            truck_route4.increment(time)
        if time == input_time:
            # print(datetime.datetime.strftime(time, "%H: %M"))
            break
        # increment time of day
        time += datetime.timedelta(0, 60)
        # print(time)

    if print_packages:
        if print_all:
            Data.print_all()
        else:
            if input_ID_int:
                Data.print_package(input_ID_int)
    if print_route:
        if list1:
            print("truck 1")
            for package in list1:
                print(package.get_id(), "|", end=" ")
                print(datetime.datetime.strftime(package.delivery_time, "%H:%M"), end=" ")
                print("|", package.deadline, end=" ")
                print("|", package.note)
            print("----------")
        if list2:
            print("truck 2")
            for package in list2:
                print(package.get_id(), "|", end=" ")
                print(datetime.datetime.strftime(package.delivery_time, "%H:%M"), end=" ")
                print("|", package.deadline, end=" ")
                print("|", package.note)
            print("----------")
        if list3:
            print("truck 3")
            for package in list3:
                print(package.get_id(), "|", end=" ")
                print(datetime.datetime.strftime(package.delivery_time, "%H:%M"), end=" ")
                print("|", package.deadline, end=" ")
                print("|", package.note)
            print("----------")
        if list4:
            print("truck 3")
            for package in list4:
                print(package.get_id(), "|", end=" ")
                if package.delivery_time != -1:
                    print(datetime.datetime.strftime(package.delivery_time, "%H:%M"), end=" ")
                print("|", package.deadline, end=" ")
                print("|", package.note)
            print("----------")
    print("Distance:")

    if truck_route1:
        total_distance += truck_route1.route.sum_length()
    if truck_route2:
        total_distance += truck_route2.route.sum_length()
    if truck_route3:
        total_distance += truck_route3.route.sum_length()
    if truck_route4:
        total_distance += truck_route4.route.sum_length()
    print(total_distance)
