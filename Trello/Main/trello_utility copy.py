
def get_board_list(client, board_id, list_name, ):
    all_lists = client.get_board("62779f48da1c5f1aca31acb0").all_lists()
    for _list in all_lists:
        if _list.name == list_name:
            my_list = _list
    return my_list

def get_list_card(source_list, card_name):
    cards = source_list.list_cards("open")
    for card in cards:
        if card.name == card_name:
            return card

def delete_cards(list_id):
    remove_cards = list_id.list_cards("open")
    for card in remove_cards:
        card.delete()
        
def get_checklists(card, client): # (Checklist Name, [])
    json_obj = client.fetch_json('/cards/' + card.id + '/checklists', )
    checklists = []
    items = []
    
    i = 0
    for i in range(len(json_obj)):
        for key, value in json_obj[i].items():
            if key == "name":
                checklists.append(value)
            elif key == "checkItems":
                names = []
                states = []
                for j in range(len(json_obj[i][key])):
                    item = json_obj[i][key][j]
                    names.append(item['name'])
                    states.append(True if item['state'] == "complete" else False)
                items.append((names, states))
    return zip(checklists, items)

def _get_items(checklist):
    pass
    # json_obj = client.fetch_json('/cards/' + card.id + '/checklists', )
    
def cards_to_checklist(client, selected_card, checklist, target_list):
    """
    - This adds checklist to the selected card based on a list that is given by the user.
    
    client: Client from TrelloClient (py-trello)
    selected_card: Card you want to convert the Target list you want into Checklist of this Card.
    checklist: Checklist From py-trello
    target_list: Lists of Cards.
    """
    # This function converts all cards from a certain list into checklist of 1 card.
    # This function is good only with 1 Checklist and 1 item on the Checklist
    s_checklists = selected_card.add_checklist("Progress List from Directory of Student Organization (OFFICERS) List", [], [])
    for t_card in target_list:
        t_checklists = get_checklists(t_card, client)
        for t_checklists, t_items in t_checklists:
            checklist.add_checklist_item(s_checklists, t_card.name, t_items[1][0])
            print(f"{t_card.name} is added in the Card {selected_card.name}.")

def set_list_from_checklist(client, selected_card, target_list, Checklist):
    # Takes the Checklist items from selected card to be as input, and whenever you change something
    # in that checklist items to be checked then run, this it will automatically sync.
    c_checklist = get_checklists(selected_card, client)
    cards = target_list.list_cards("open")
    for checklists, items in c_checklist:
        names, states = items
        for name, state in zip(names, states):
            for card in cards:
                if card.name == name:
                    item = list(get_checklists(card, client))[0][1][0][0]
                    condition = list(get_checklists(card, client))[0][1][1][0]
                    if condition == state:
                        print(f"{card.name} does not need to process. Skip")
                        continue
                    else:
                        new_name = card.name + " (Working)"
                        Checklist.rename_checklist_item(selected_card.checklists[-1], card.name, new_name)
                        Checklist.set_checklist_item(card.checklists[-1], item, state)
                        Checklist.rename_checklist_item(selected_card.checklists[-1], new_name, card.name)
                        print(f"{name} is done working at {target_list.name}")

def set_card_checklist(client, selected_card, checklist, target_list):
    # This only works with 1 Checklist on Card of Selected Target List and 1 Items on that Checklist.
    # Gin kukuha niya an Cards ha selected List ha Trello tas kikitaon an Checklist han Card na Selected List kun Done Checked naba an usa na Checklist
    # Tas kun checked hiya, then kopyahon la niya an State ha selected Card mo.
    # Set this card's checklist based on the Cards on the Target List.
    s_checklists = selected_card.checklists[-1]
    for i, t_card in enumerate(target_list):
        new_name = t_card.name + " (WORKING)"
        t_checklists = get_checklists(t_card, client)
        checklist.rename_checklist_item(s_checklists, t_card.name, new_name)
        for t_checklists, t_items in t_checklists:
            checklist.set_checklist_item(s_checklists, new_name, t_items[1][0])
            checklist.rename_checklist_item(s_checklists, new_name, t_card.name)
            current_item = list(get_checklists(selected_card, client))[0][1][0][i]
            print(f"{current_item} is done working.")

def officer_cards(officers: list[str], list_id: list[str]):
    # Creates a card for officers that has an attachments and names and checklist.
    for officer in officers:
        card = list_id.add_card(officer, "This Officer must fillout the Directory of Student Organization.")
        card.add_checklist("SUBMITTED", ["Done"], [False])
        card.attach("Upload your File Here.", None, None, "https://drive.google.com/drive/u/2/folders/1xtV780CsOFFU-HAtfFHf545-i7Ryi0bE")
        card.attach("File Example", None, None, "https://docs.google.com/document/d/1Jy6abKj5F4dnSAwt3yMn60SJPuDSiP8V/edit?rtpof=true")

def set_card_as_list(card_name,source_list, header_title, checklist_name, target_list):
    # Creates a Card with Connected to Targeted List, gets all the cards from Target List and Get's the url of each card and store it.
    # Then it makes it as description of stored url in order to be a Card List placeholder.
    description = f"{header_title}:\n"
    for i, card in enumerate(target_list.list_cards("open")):
        description += f"{i+1}. {card.name}: {card.short_url}\n"
    source_list.add_card(card_name, description)
    card.add_checklist(checklist_name)

def open_text(filename: str):
    text_file = []
    with open(f"{filename}.txt", "r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.split()
            name = " ".join(line)
            # print(name)
            text_file.append(name)
    return text_file
