import json
from trello import TrelloClient
from datetime import datetime
from datetime import timezone

"""
Important
deadline = now + timedelta(days = deadlineDays)

start = f"{now.strftime('%Y-%m-%d')}T00:05:46.157Z",
due = f"{deadline.strftime('%Y-%m-%d')}T23:59:46.157Z"
"""

class Card:
    def __init__(self, id):
        self.client = TrelloClient(
            api_key="ada3d2dc9923a095eab8986824e3bd2e",
            api_secret="8e6ec0608e798b8cc1a28869f6417fca5421f7df8b7d40285d04076ad2d76836",
            token="6c347234f4b88343e1d482b0b3145bb7e419a55aabe3d9dcb0b5fdb1c68d10be"
            )
        
        self.id = id
        self.me = self.client.get_card(self.id)
        
        self.action = self.me.fetch_actions(action_filter = "updateCard", action_limit = 5)[0]
        self.source_list = self.action['data']['list']['name']
        self.destination_list = ""
        self.current_time = datetime.fromisoformat(self.action['date'][:-1]).astimezone(timezone.utc)
        self.me.set_name(self.me.name.replace("(Not Moved)", ""))
        self.me.set_name(self.me.name + "(Not Moved)")
        if self.has_moved(self.me, self.current_time):
            print(f"{self.me.name} - from {self.source_list} Moved to {self.destination_list}")
            self.me.set_name(self.me.name.replace("(Not Moved)", ""))
            data[self.destination_list].append(self.me.name)
        
    def has_moved(self, card, before):
        card_action = card.fetch_actions(action_filter = "updateCard", action_limit = 5)[0]
        card_date = card_action['date'][:-1]
        current = datetime.fromisoformat(card_date).astimezone(timezone.utc)
        if before == current:
            new_card = self.client.get_card(card.id)
            return self.has_moved(new_card, current)
        elif before != current:
            try:
                self.destination_list = card_action['data']['listAfter']['name']
            except KeyError:
                self.destination_list = card_action['data']['list']['name']
            return True

# def has_moved(card, before):
#     card_action = card.fetch_actions(action_filter = "updateCard", action_limit = 5)[0]
#     card_date = card_action['date'][:-1]
#     current = datetime.fromisoformat(card_date).astimezone(timezone.utc)
#     if before == current:
#         new_card = client.get_card(card.id)
#         return has_moved(new_card, current)
#     else:
#         print("HEY")
#         return True

client = TrelloClient(
api_key="ada3d2dc9923a095eab8986824e3bd2e",
api_secret="8e6ec0608e798b8cc1a28869f6417fca5421f7df8b7d40285d04076ad2d76836",
token="6c347234f4b88343e1d482b0b3145bb7e419a55aabe3d9dcb0b5fdb1c68d10be")

card_id = "6203c56e905e623fa43bf187"


lists = client.get_board("61990ce926d06b813c44c52e").get_lists("open")
cards = client.get_list("6203abc9bc236359a7d95d01").list_cards()

data = {}
for b_list in lists:
    data.update({b_list.name: []})
print(data)

for _card in cards:
    Card(_card.id)


