import re


def parse():
    content = open("input.txt").read().splitlines()
    pattern = "-?\d+"

    return [[int(x) for x in re.findall(pattern, line)] for line in content]


def find_diff(coords):
    x, y, b_x, b_y = coords
    diff_x = abs(x - b_x)
    diff_y = abs(y - b_y)
    return diff_x + diff_y


def find_exclusion_zone_range(coords, diff, y, constraint=None):
    # Exc zone at x = 0 including the sensor
    # exclusion_zone = diff * 2 + 1
    dist_y = abs(y - coords[1])
    start = coords[0] - (diff - dist_y)
    end = coords[0] + (diff - dist_y)
    if constraint is not None:
        start = 0 if start < 0 else constraint if start > constraint else start
        end = constraint if end > constraint else end
    return start, end


def merge_intervals(intervals):
    result = []
    (start_candidate, stop_candidate) = intervals[0]
    for (start, stop) in intervals[1:]:
        if start <= stop_candidate:
            stop_candidate = max(stop, stop_candidate)
        else:
            result.append((start_candidate, stop_candidate))
            (start_candidate, stop_candidate) = (start, stop)
    result.append((start_candidate, stop_candidate))
    return result


def find_sensors_in_range(sensors, diffs, y):
    sensors_in_range = []
    for i in range(len(sensors)):
        s_x, s_y = sensors[i][0], sensors[i][1]
        diff = diffs[i]

        # y = 10, S_y = 7, B_y = 10, diff = 9
        if abs(y - s_y) <= diff:
            # Find the range of exclusion zone at y
            exc_zone = find_exclusion_zone_range(sensors[i], diff, y)
            sensors_in_range.append((sensors[i], diff, exc_zone))
    return sensors_in_range


def p1(y):
    sensors = parse()
    diffs = [find_diff(sensor) for sensor in sensors]
    # Find all sensors that will have an exclusion zone in y
    # The radius of the exclusion zone is diff_x + diff_y on the same y plane
    # for each increasing y + 1, the radius shrinks by 1 (total zone decreases by 2)
    # total zone is 1 at sensor_y +- diff
    # Thus, each sensor only affects row y when y <= sensor_y + diff or y >= sensor_y - diff
    sensors_in_range = find_sensors_in_range(sensors, diffs, y)

    # Find the union of all exclusion zones
    ranges = sorted([x[2] for x in sensors_in_range])
    exc_zones = merge_intervals(ranges)

    return sum([zone[1] - zone[0] for zone in exc_zones])


def p2(end):
    sensors = parse()
    diffs = [find_diff(sensor) for sensor in sensors]
    # Find a space not in exclusion zone within (0, 400000),(0, 400000)
    for y in range(end + 1):
        # Find all sensors that will have an exclusion zone in y
        # The radius of the exclusion zone is diff_x + diff_y on the same y plane
        # for each increasing y + 1, the radius shrinks by 1 (total zone decreases by 2)
        # total zone is 1 at sensor_y +- diff
        # Thus, each sensor only affects row y when y <= sensor_y + diff or y >= sensor_y - diff
        sensors_in_range = find_sensors_in_range(sensors, diffs, y)

        # Find the union of all exclusion zones
        if len(sensors_in_range) > 0:
            ranges = sorted([x[2] for x in sensors_in_range])
            exc_zones = merge_intervals(ranges)
            if len(exc_zones) == 2:
                r1, r2 = exc_zones
                if r2[0] - r1[1] == 2:
                    x = r1[1] + 1
                    return end * x + y


print("Part 1: ", end="")
print(p1(2000000))
print("Part 2: ", end="")
print(p2(4000000))
