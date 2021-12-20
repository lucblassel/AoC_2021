from math import sqrt

x_range, y_range = (240, 292), (-90, -57)
test_x, test_y = (20, 30), (-10, -5)


# The maximum x the probe can reach with v0 initial x velocity
def get_xmax(v0):
    return (v0 * (v0 + 1)) // 2


# The minimum value of the initial x velocity to reach the target start
def get_x_vmin(target_x_start):
    return int(1 + (-1 + sqrt(1 + 8 * target_x_start)) // 2)


# The value of x after t steps
def get_x_t(v0, t):
    if t > v0:
        return get_xmax(v0)
    return int((t + 1) * (v0 - t / 2))


# the value of y after t steps
def get_y_t(v0, t):
    return int((t + 1) * (v0 - t / 2))


# get x_vels that will lead to at least one x value inside of the target x range
def get_valid_x_vels(xmin, xmax):
    x_vel_range = range(get_x_vmin(xmin), xmax + 1)
    valid = []
    for vel in x_vel_range:
        x = 0
        t = 0
        while x <= xmax:
            x += vel
            if x >= xmin:
                valid.append((vel, t))
                break
            vel = max(0, vel - 1)
            t += 1
    return valid


def get_valid_vels(xmin, xmax, ymin, ymax):
    valids = []
    for x_vel in range(get_x_vmin(xmin), xmax + 1):
        for y_vel in range(ymin, abs(ymin)):
            traj, valid = get_traj(x_vel, y_vel, xmin, xmax, ymin, ymax)
            if valid:
                valids.append(traj)
            else:
                pass
    return valids


def get_traj(vx, vy, xmin, xmax, ymin, ymax):
    x, y = 0, 0
    traj = []
    while x <= xmax and y >= ymin:
        if x >= xmin and y <= ymax:
            # print(vx, vy, x, y)
            return traj, True
        x += vx
        y += vy
        traj.append((x, y))
        if vx > 0:
            vx -= 1
        vy -= 1

    return traj, False


def main():
    vels = get_valid_vels(*x_range, *y_range)
    max_ys = [(x[0], max(v[1] for v in x)) for x in vels]
    print(max(max_ys, key=lambda x: x[1]))


if __name__ == "__main__":
    main()
