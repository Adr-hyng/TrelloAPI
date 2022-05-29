from trello import TrelloClient

API_KEY = "" # Insert your API key here.
API_SECRET_KEY = "" # Insert your API Secret Key here.
API_TOKEN = "" # Insert your API Token here.

client = TrelloClient(
api_key = API_KEY,
api_secret = API_SECRET_KEY,
token = API_TOKEN)

list_name = "My Sample List" # Name of Trello list you want to add the card to.

BOARD_ID = "" # Insert your board ID here.

all_lists = client.get_board(BOARD_ID).all_lists()

target_list = [_list for _list in all_lists if _list.name == list_name]

added_card = target_list[0].add_card(name = "CARD SAMPLE", desc = "Description Sample")

print(added_card.name)

