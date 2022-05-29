from unittest import result
from fuzzywuzzy import fuzz

a = "Chad Vincent Florentino"
b = "Chad Aga Abinguna"
result = fuzz.token_sort_ratio(a, b)
result1 = fuzz.partial_token_sort_ratio(a, b)
result2 = fuzz.partial_token_set_ratio(a, b)

print(f"Result of {a} == {b} is {result1}% Match")