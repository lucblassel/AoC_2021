import array

input_ = "./data.txt"

max_days = 256

def main():
    counter = [0 for x in range(9)]

    with open(input_, "r") as file:
        for x in file.readlines()[0].split(","):
            counter[int(x)] += 1

    for day in range(max_days):
        to_add = counter[0]
        counter = counter[1:] + counter[0:1]
        counter[6] += to_add

    print(sum(counter))

if __name__ == "__main__":
    main()

