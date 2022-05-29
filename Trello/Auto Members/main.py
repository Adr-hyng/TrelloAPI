# -*- coding: utf-8 -*-
# This is great for Facebook Members Only

def generate_members(filename: str) -> list[str]:
    """Members Generator from Facebook Messenger

    Args:
        filename (str): Only needs the file name, not including the extension.

    Returns:
        list[str]: Returns the members as list.
    """    
    new_members = []
    with open(filename + ".txt", "r") as r:
        lines = r.readlines()
        members = [line.rstrip() for line in lines]
    
    
    with open("output.txt", "w") as o:
        for i in range(len(members)):
            if i % 2 == 0:
                new_members.append(members[i])
                o.write(members[i] + "\n")
    return new_members



def name_comparison(compareList: list[str]) -> list[str]:
    from fuzzywuzzy import fuzz
    """Fuzzy Name Algorithm
    
    Documentation: This function compares between the current name to the next name if is similar, then output the percentage of similarity.
    
    Args:
        compareList (list[str]): Gets all the Names then compare the current to the next name, if similar or not.

    Returns:
        list[str]: Returns the original list of comparisons.
    """    
    # compareList = [ "Christian Calipayan" , "Christian Garcia Calipayan"]
    counter = 0
    for i, x in enumerate(range(0, len(compareList), 1)):
        name = compareList
        if i - 1 < 0:
            continue
        try:
            b = fuzz.token_sort_ratio(name[x-1], name[x])
            if b >= 60:
                print(f"{name[x-1]}:{b} == {name[x]}:{b}")
                compareList.remove(name[x-1])
                counter += 1
        except:
            pass

    return compareList

def previous_and_next(some_iterable: iter) -> zip:
    """Previous and Next Zip

    Args:
        some_iterable (iter): Gets the previous and next items using only for each.

    Returns:
        zip: returns the zipped lists. (Prev, Current, Next)
    """    
    from itertools import tee, islice, chain
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

members = generate_members("input")
members = name_comparison(members)
with open("output.txt", "w") as o:
    for member in members:
        o.write(member + "\n")
