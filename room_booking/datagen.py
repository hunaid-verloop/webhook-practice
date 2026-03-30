import random
import pandas as pd



def gen_name():
    chs = "abcdefghijklmnopqrstuvwxyz"
    k = random.randint(7,14)
    return "".join(random.choices(chs, k = k))

def gen_phone():
    d = "1234567890"
    first_d = random.choice(d[:-1])
    remaining = "".join(random.choices(d, k = 9))
    return first_d + remaining

def gen_price():
    prices = [1000, 1500, 2000, 2500]
    return random.choice(prices)

def main():
    cities, areas, rooms = [], [], []
    # iterating over cities
    for i in range(25):
        # iterating over areas in the city i
        for j in range(10):
            no_of_rooms = random.randint(1, 10)
            for k in range(no_of_rooms):
                cities.append(f"city-{i}")
                areas.append(f"area-{j}")
                rooms.append({"name": gen_name(), "phone": gen_phone(), "price":gen_price()})
                df = pd.DataFrame({"cities": cities, "areas": areas, "rooms": rooms})
                df.to_csv("rrms.csv")


if __name__ == '__main__':
    main()