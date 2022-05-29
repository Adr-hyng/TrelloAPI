def convert_text(filename: str) -> list[str]:
    """
    Parameters: -> list[str]
        -> This converts the copied spreadsheet data into the txt file to be returned as list.

    filename: str
        - File name of the txt file that contains spreadsheet raw data.
        
    """   
     
    converted = []
    with open(f"{filename}.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            converted.append(" ".join(line.split()))
    return converted
            