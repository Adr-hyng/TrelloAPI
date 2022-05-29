def get_board_list(client, board_id, list_name):
    """
    Paramaters: -> List
        -> This function gets the List Object by passing the name of the List you want to be returned, and ID of the Board in your workspace.

    client: TrelloClient():
        - Client the py-trello API uses.
    
    board_id: str
        - ID of selected board of a certain workspace.
        
    list_name: str
        - Name of List to returned.
        
    """
    
    all_lists = client.get_board(board_id).all_lists()
    result = [_list for _list in all_lists if _list.name == list_name]
    return result[0]

def get_list_card(source_list, card_name):
    """
    Paramaters: -> Card
        -> Returns the Card Object by passing the List Object and Name of the card you want to find.
    
    source_list: List Object (py-trello)
        - List of Cards you want to search for this card.
        
    card_name: str
        - Name of the Card you want to be returned.
        
    """
    
    card = [ _card for _card in source_list if _card.name == card_name]
    return card[0]

def delete_cards(target_list):
    """
    Paramaters: -> None
        -> Returns the Card Object by passing the List Object and Name of the card you want to find.
    
    target_list: List Object (py-trello)
        - List of Cards you want to be removed or deleted.
        
    """

    for card in target_list:
        card.delete()
        
def get_checklists(card, client): # Returns (Checklist Name, ["ItemName"], [itemState])
    """
    Paramaters: -> zip()
        -> This returns the checklists of the selected Card.
        Format: (checkListName, ["itemName",..], [itemState,..])
    
    card: Card
        - Card you want to get the checklists.
    
    client: TrelloClient (py-trello)
        - Client the py-trello API uses.
        
    """
    
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
    
def cards_to_checklist(client, selected_card, checklist_name, checklist, target_list):
    """
    Paramaters: -> None
        -> This adds checklist and checklist's items to be selected Card by converting the selected List's cards. This only applies on a card that has 1 Checklist and 1 Item for checking purposes.
        Example:
        Card:
        -   Checklist: Homework
            - Done (False)
    
    client: TrelloClient (py-trello)
        - Client the py-trello API uses.
        
    selected_card: Card
        - Card you want to be filled with Checklist and items as Cards on the selected List.
        
    checklist_name: str
        - Name of checklist to be added.
        
    checklist: Checklist (py-trello)
        - Checklist Object to be access other methods. 
        
    target_list: List
        - List of Cards you want to be converted into checklist of a selected Card.
        
    """
    
    s_checklists = selected_card.add_checklist(checklist_name, [], [])
    for t_card in target_list:
        t_checklists = get_checklists(t_card, client)
        for t_checklists, t_items in t_checklists:
            checklist.add_checklist_item(s_checklists, t_card.name, t_items[1][0])
            print(f"{t_card.name} is added in the Card {selected_card.name}.")

def set_list_from_checklist(client, selected_card, target_list, Checklist):
    """
    Paramaters: -> None
        -> This is the reverse of "set_card_checklist(...)".
        -> This takes the checklist of the card being selected, then whatever changes you put in the checklist of the card. Will also change each Card on the selected List. Behaves similar as "Synchronization".
    
    client: TrelloClient (py-trello)
        - Client the py-trello API uses.
        
    selected_card: Card
        - Card you want to pick as input.
        
    target_list: List
        - List you want to select as output.
        
    checklist: Checklist (py-trello)
        - Checklist Object to be access other methods. 
        
    """
    
    c_checklist = get_checklists(selected_card, client)
    for checklists, items in c_checklist:
        names, states = items
        for name, state in zip(names, states):
            for card in target_list:
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
    """
    Paramaters: -> None
        -> This takes your selected Card's checklist as output of the selected List' card's checklist. Then synchronizing the Checklist of cards on List of cards and the selected Card's checklist.
    
    client: TrelloClient (py-trello)
        - Client the py-trello API uses.
        
    selected_card: Card
        - Card you want to select as output.
        
    checklist: Checklist (py-trello)
        - Checklist Object to be access other methods.    
         
    target_list: List
        - List of Cards you want to select as input to be check each card and synchronize its state of checklist item to the checklist of selected card.
        
    """

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

def automate_cards(listNames: list[str], target_list):
    """
    Paramaters: -> None
        -> This automatically generates a card from a given List of Names and List you want the card to generate.
         
    cards: list[str]
        - List of names to be put in each individual card.
        
    target_list: List
        - Selected List you want to generate cards.
        
    """

    for card_name in listNames:
        generated_card = target_list.add_card(card_name, "This Officer must fillout the Directory of Student Organization.")
        generated_card.add_checklist("SUBMITTED", ["Done"], [False])
        generated_card.attach("Upload your File Here.", None, None, "https://drive.google.com/drive/u/2/folders/1xtV780CsOFFU-HAtfFHf545-i7Ryi0bE")
        generated_card.attach("File Example", None, None, "https://docs.google.com/document/d/1Jy6abKj5F4dnSAwt3yMn60SJPuDSiP8V/edit?rtpof=true")

def add_pointer_card(card_name, source_list, target_list, header_title: str = "Generated Card Pointer", checklist_name: str = "Generated Checklist"):
    """
    Paramaters: -> None
        -> Creates a pointer card that contains the short link url of each individual card and store them into a single card as description.
        Format: 1. Adrian Alvarez Abaigar -> trello/c/13j1203i,...
         
    card_name: list[str]
        - List of names to be put in each individual card.
        
    source_list: List
        - List wherein you want your card to be added.
        
    target_list: list[Cards]
        - List of cards that your selected list contains, and generate each card's short link.
        
    header_title: str
        - Description Header of a Card.
        
    checklist_name: str
        - Checklist name of a Card created.
    """
    
    description = f"{header_title}:\n"
    for i, card in enumerate(target_list):
        description += f"{i+1}. {card.name}: {card.short_url}\n"
    source_list.add_card(card_name, description)
    card.add_checklist(checklist_name)

def open_text(filename: str):
    """
    Paramaters: -> list[str]
        -> This opens a txt file, and get each line of the txt file and add it to the list and return it as a List
         
    filename: str
        - File name (txt format)
    
    """
    # Opens Textfile and Transfer it to the Program to create as a List and return.
    text_file = []
    with open(f"{filename}.txt", "r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.split()
            name = " ".join(line)
            # print(name)
            text_file.append(name)
    return text_file
