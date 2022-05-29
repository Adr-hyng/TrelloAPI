from trello import TrelloClient
from trello import Checklist
import trello_utility

client = TrelloClient(
api_key="ada3d2dc9923a095eab8986824e3bd2e",
api_secret="8e6ec0608e798b8cc1a28869f6417fca5421f7df8b7d40285d04076ad2d76836",
token="6c347234f4b88343e1d482b0b3145bb7e419a55aabe3d9dcb0b5fdb1c68d10be")


target_list = "Directory of Student Organization (OFFICERS)"
target_card = "Directory of Student Organization Card List (Officers)"


board_id = "62779f48da1c5f1aca31acb0" # Official Board of ICpEP.SE Chapter 1 Organization

directory_organization = trello_utility.get_board_list(client, board_id, target_list)

directory_organization.add_card("CARD SAMPLE", "Description Sample")


source_list = trello_utility.get_board_list(client, board_id, "Files")
selected_card = trello_utility.get_list_card(source_list, target_card)

print(selected_card.name)

# trello_utility.set_list_from_checklist(client, selected_card, directory_organization, Checklist)

# trello_utility.cards_to_checklist(client, selected_card, Checklist, cards)





