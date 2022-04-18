# #Zad 1

# nums = [11,8,11]
# target = 22


# found = {}
# for index, num in enumerate(nums):
#     if num in found: print( [index, found[num]])
#     found[target-num] = index

#####################################################################################

# # #Zad 9

# num = 0
# if num >= 0:
#     new_num = 0
#     old_num = num
#     while (num):        
#         last = num % 10
#         new_num = new_num*10 + num % 10 
#         num = num // 10
#     if old_num == new_num:
#         print(new_num, old_num)

#####################################################################################

# # Wlasne zadanko

# word = "AASWABBBCDW"
# last = word[0]

# counter = 0

# for i, letter in enumerate(word):

#     if len(word)-1 == i:
#         print(letter,counter)

#     elif last == letter:
#         counter += 1

#     elif last != letter:
#         print(last,counter)
#         counter = 1

#     last = letter

#####################################################################################

# # Zadanko 13

# s = "MMDXCIX"       #2599

# VALUES = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}

# total = 0


# s = s.replace("IV", "IIII")
# s = s.replace("XL", "XXXX")
# s = s.replace("CD", "CCCC")

# s = s.replace("CM", "DCCCC")
# s = s.replace("XC", "LXXXX")
# s = s.replace("IX", "VIIII")

# print(s)
# for char in s:
#     total += VALUES[char]

# print(total)


#####################################################################################

# # Zadanko 14

# strs = ["flower", "flow", "flight"]
# prefix = ""

# l = zip(*strs)      # [('f', 'f', 'f'), ('l', 'l', 'l'), ('o', 'o', 'i'), ('w', 'w', 'g')]

# for i in l:
#     if len(set(i)) == 1:
#         prefix += i[0]
#     else:
#         break
# print(prefix)


#####################################################################################

# # Zad 23?
# list1 = [1,2,4,5,7,9,22,23]
# list2 = [1,3,4,5,6,10,11,24]

# l1 = iter(list1)
# l2 = iter(list2)

# x1 = next(l1)
# x2 = next(l2)

# lista3 = []
# for i in range(len(list1) + len(list2)): 
#     if x1 < x2:
#         lista3.append(x1)
#         x1 = next(l1,float("inf"))
#     else:
#         lista3.append(x2)
#         x2 = next(l2,float("inf"))
#     print(lista3)


#####################################################################################

nums = [0,0,1,1,1,2,2,3,3,4]

print(len(set(nums)), list(set(nums)))