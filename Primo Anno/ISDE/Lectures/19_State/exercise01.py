def check_for_thirtheen(nums: list, to_remove: int) -> int:
    sum = 0
    last_elem = None
    for elem in nums:
        if elem != to_remove and last_elem != to_remove:
            sum += elem
        last_elem = elem
    return sum



if __name__ == "__main__":
    nums1 = [1, 13, 10, 1, 13, 13, 13, 10, 1, 13]
    nums2 = [1, 13, 10, 1, 13, 13, 13, 10, 1]
    nums3 = [13, 10, 1, 13, 13, 13, 10, 1]
    print(check_for_thirtheen(nums1, 13) == 3)
    print(check_for_thirtheen(nums2, 13) == 3)
    print(check_for_thirtheen(nums3, 13) == 2)
