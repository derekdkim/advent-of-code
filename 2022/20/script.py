def parse():
    return [int(n) for n in open("input.txt", "r").readlines()]


def update_key_indexes(new_nums, key_to_i):
    # Update the key indexes of all indexes affected in the hash table
    for i, num in enumerate(new_nums):
        key_to_i[num[1]] = i


def solve(mix_count=1, hash_key=1):
    nums = parse()

    # Rearrange numbers in a copy of the list
    # numbers are not unique so they need to be kept track of using keys indexed in their original order
    new_nums = [(num * hash_key, i) for i, num in enumerate(nums)]
    # Maps keys to index
    # key: original index, val: current index
    key_to_i = {i[1]: i[1] for i in new_nums}
    n = len(nums)

    # Iterate through i -- initial order, saved as keys in key_to_i
    for t in range(mix_count):
        # Just because it takes a while
        print(f"Mix round {t}")
        # Iterate numbers according to their original indices
        for i in range(n):
            # Find index of this number on the current array
            # 0 -> 1; x was originally at index 0, now it's at index 1
            x_index = key_to_i[i]
            # Find actual number then remove it from the array
            # After this, the hashed numbers are no longer accurate; the index hash map needs to be updated
            x = new_nums[x_index]
            new_nums.pop(x_index)

            # Edge condition
            # the index and shift being an additive inverse means it will end up at position 0
            # but because the shift happens to occur in between 2 numbers, adding it to position 0 will
            # throw off the orientation of the array
            # This can be avoided if it gets appended to the end
            if x[0] == -x_index:
                new_nums.append(x)
            else:
                # Cull numbers and shift by remainder
                # needs n - 1 to avoid off by one error; shifts the entire array
                shift = (x_index + x[0]) % (n - 1)
                new_nums.insert(shift, x)
            # The hash needs to be updated at the end of every movement
            # [x_index, n) is insufficient because the newly inserted position could be ahead or behind x_index
            # Safer to just update everything
            update_key_indexes(new_nums, key_to_i)

    # Index of zero
    i_origin = [i for i, j in enumerate(new_nums) if j[0] == 0][0]
    return sum(new_nums[(k + i_origin) % n][0] for k in (1000, 2000, 3000))


print("Part 1: ")
print(solve())
print("Part 2: ")
print(solve(10, 811589153))
