# Create Sort by DateLastActivity


class Trello_Modern:
    def __init__(self):
        pass
    
class PostCard:
    def __init__(self):
        pass
    
class GetCard:
    def __init__(self):
        pass
    
class UpdateCard:
    def __init__(self):
        pass
    
class DeleteCard:
    def __init__(self):
        pass
    
class List:
    def bubble_sort():
        cards = client.get_list("6203abc9bc236359a7d95d01").list_cards()
        for i in range(len(cards)):
            for j in range(0, len(cards) - i - 1):
                if not(cards[j].dateLastActivity > cards[j+1].dateLastActivity):
                    temp = cards[j].pos
                    cards[j].change_pos(cards[j+1].pos)
                    cards[j+1].change_pos(temp)
    
    def is_sorted(self, arr):
        if(arr == sorted(arr)):
            return True
        return False
                
    def sort_cards(self, cards): # Names
        # printer = [ print(card.name ,card.dateLastActivity) for card in cards]
        names = [ card.name for card in cards]
        positions = [ card.pos for card in cards]
        last_activities = [ card.dateLastActivity for card in cards]
        
        positions = sorted(positions)
        names = sorted(names)
        last_activities = sorted(last_activities)
        
        sortment = []
        for i in range(len(cards)):
            for j in range(len(cards)):
                if cards[i].dateLastActivity == last_activities[j]:
                    index = last_activities.index(last_activities[j])
                    sortment.append(index)
                    cards[i].change_pos(positions[index])
            print(sortment)
        new_card = client.get_list(self.list_id).list_cards()
        return self.sort_cards(new_card) if not self.is_sorted(sortment) else print("sorted")
