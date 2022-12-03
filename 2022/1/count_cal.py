file = open("input.txt", "r")

# Parse file
calories = file.read().splitlines()

# Find max
total_cals = []
cal = 0
for i in calories:
    if i == "":
        if cal > 0:
            total_cals.append(cal)
        cal = 0
    else:
        cal += int(i)
max_cal = max(total_cals)

# Find top 3
total_cals.sort()
top_3_total = sum([total_cals[i] for i in range(-1, -4, -1)])

print(max_cal)
print(top_3_total)
