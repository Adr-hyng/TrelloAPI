import requests
import json

"""
Progress:
* CARDS
// - PostCard
// - GetCard
// - UpdateCard
// - DeleteCard

* LISTS 
- PostList
- GetList
- UpdateList
- DeleteList

* AUTOMATE
- SORT CARDS IN LIST (DateTime)

TODO:
- Create Post CheckList in Card
"""

class TrelloCard:
    def __init__(self):
        self.endpoint = "https://api.trello.com/1/"
        
class Automate(TrelloCard): #Not Done
    def __init__(self, key, token, idList):
        self.trello = TrelloCard()
        self.key = key
        self.token = token
        self.idList = idList
    
    def sortList(self): # Sort by Pos
        pass
    
    def update_desc(self): # Updates every card's description
        pass
    
    def update_fieldvalue(self): # Updates every card's field value
        pass
    
    def sortList(self, idList, jsonFile, ascending = 'dateLastActivity'):
        self.card_endpoint = self.trello.endpoint + "lists/" + idList
        self.jsons = {
            "key": self.key,
            "token": self.token,
            "idBoard": self.idBoard
        }
        self.updated_list = requests.put(self.card_endpoint, json = self.jsons)
        basic_json = sorted(json.loads(self.updated_list.text), key = lambda i: i[ascending])

    def update(self, id, description):
        self.replace(id, description)

class GetCard(TrelloCard):
    def __init__(self, idList):
        self.trello = TrelloCard()
        self.idList = idList
        
    def petch(self):
        self.card_endpoint = self.trello.endpoint + "lists/" + self.idList + "/cards/"
        self.jsons = {
            "id": self.idList
        }
        self.get_card = requests.get(self.card_endpoint, json = self.jsons)
        try:
            basic_json = sorted(json.loads(self.get_card.text), key = lambda i: i['dateLastActivity'])
            print(self.get_card)
            print(json.dumps(basic_json, indent = 4, sort_keys = True))
        except Exception as e:
            print()
        
        
    def petch_list(self):
        pass
        
class DeleteCard(TrelloCard):
    def __init__(self, key, token):
        self.trello = TrelloCard()
        self.key = key
        self.token = token
        
    def _remove(self, id):
        self.card_endpoint = self.trello.endpoint + "cards/" + id
        self.jsons = {
            "key": self.key,
            "token": self.token
        }
        self.updated_card = requests.delete(self.card_endpoint, json = self.jsons)
        
    def delete(self, id):
        self._remove(id)
        
class UpdateCard(TrelloCard):
    def __init__(self, key, token):
        self.trello = TrelloCard()
        self.key = key
        self.token = token
    
    def replaceField(self, idCard, idCustomField, idValue, value):
        self.card_endpoint = self.trello.endpoint + "cards/" + idCard + "/customField/" + idCustomField + "/item"
        self.jsons = {
            "idValue": idValue,
            "key": self.key,
            "token": self.token,
            "value": {
                "number": value
            }
        }
        self.updated_card = requests.put(self.card_endpoint, json = self.jsons)
    
    def replaceDescription(self, id: str, idList: str, key_value: str):
        self.card_endpoint = self.trello.endpoint + "cards/" + id
        self.jsons = {
            "key": self.key,
            "token": self.token,
            "idList": idList,
            "desc": key_value
        }
        self.updated_card = requests.put(self.card_endpoint, json = self.jsons)
    
    def updateDescription(self, id, idList, key_value):
        self.replaceDescription(id, idList, key_value)
        
    def updateField(self, idCard, idCustomField, idValue, value):    
        self.replaceField(idCard, idCustomField, idValue, value)

class PostCard(TrelloCard):
    def __init__(self, key: str, token: str, idList: str, start: str = None, due: str = None):
        self.trello = TrelloCard()
        self.key = key
        self.token = token
        self.idList = idList
        self.start = start
        self.due = due
    
    def _create(self, card_name: str, card_description):
        self.card_endpoint =  self.trello.endpoint + "cards"
        self.jsons = {
            "key": self.key,
            "token": self.token,
            "idList": self.idList,
            "name": card_name,
            "desc": card_description,
            "due": self.due,
            "start": self.start
                }
        self.new_card = requests.post(self.card_endpoint, json = self.jsons)
    
    def from_txt(self, filename, description):
        file = self.string_to_list(filename)
        for line in file:
            self._create(f"{line}", description)
            
    def post(self, string, description):
        self._create(string, description)