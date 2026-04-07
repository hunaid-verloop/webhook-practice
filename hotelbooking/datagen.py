import random
import csv

MYHOTEL_BOOKINGS = "myhotel.txt"

month_days = {"January":31, "February":28, "March": 31, "April": 30, "May": 31, "June": 30,
              "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31}

month_int = {"January": 1, "February":2, "March": 3, "April": 4, "May": 5, "June": 6,
              "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}


def generate_myhotels_bookings():
    rooms = []
    for i in range(1, 2):
        for j in range(5):
            r = f"{i}0{j}" if j < 10 else f"{i}{j}"
            rooms.append(r)
    hotel_bookings = {r:{} for r in rooms}
    for r in rooms:
        for month, days in month_days.items():
            hotel_bookings[r][month] = [random.randint(0, 1) for _ in range(days)]

    with open(MYHOTEL_BOOKINGS, 'w') as f:
        lines = []
        for room, bookings in hotel_bookings.items():
            for month, days in bookings.items():
                sofar = f"The {room} room in the month of {month} is available for the following dates:\n"
                sofar_ = ""
                for d in range(1, month_days[month]+1):
                    if random.randint(0, 1) == 1:
                        sofar_ += f"{2026}-{'{:02d}'.format(month_int[month])}-{'{:02d}'.format(d)}, "
                sofar += f"{sofar_[:-2]}\n"
                lines.append(sofar)
        f.writelines(lines)


if __name__ == "__main__":
    generate_myhotels_bookings()