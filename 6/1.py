import array

input_ = "./test.txt"

max_days = 80

def main():

    with open(input_, "r") as file:
        ages = array.array("B",(int(x) for x in file.readlines()[0].split(",")))

    for day in range(max_days):
        to_add = 0
        for i, age in enumerate(ages):
            if age == 0:
                to_add += 1
                ages[i] = 6
            else:
                ages[i] -= 1
        for _ in range(to_add):
            ages.append(8)

    print(len(ages))


if __name__ == "__main__":
    main()

