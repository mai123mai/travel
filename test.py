# def s_split(s):
#     l = []
#     temp = ''
#     for i in s:
#         if i != '&':
#             temp += i
#         else:
#             if temp != '':
#                 l.append(temp)
#                 temp = ''
#     l.append(temp)
#     return l
#
# def s_combination(l):
#     s1 = ''
#     for i in l:
#         s1 += i + '&&'
#     return s1[:-2]
#
#
# s = 'ab&&2'
import random

l = []

# def is_prime(num):
#     if num < 2:
#         return False
#     for i in range(2, int(num ** 0.5) + 1):
#         if num % i == 0:
#             return False
#     return True
#
#
# def max_prime(n):
#     for i in range(n, 1, -1):
#         if is_prime(i):
#             return i
#     return None
#
#
# print(max_prime(100))




def search(nums):
    for i in range(len(nums)):
        if nums.count(nums[i]) == 2:
            print("有且只有2个相同的数：", nums[i])
nums = [random.randint(0, 999) for i in range(1000)]
search(nums)
