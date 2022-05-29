from trello import TrelloClient


client = TrelloClient(
api_key="ada3d2dc9923a095eab8986824e3bd2e",
api_secret="8e6ec0608e798b8cc1a28869f6417fca5421f7df8b7d40285d04076ad2d76836",
token="6c347234f4b88343e1d482b0b3145bb7e419a55aabe3d9dcb0b5fdb1c68d10be")



lists = client.get_board("623f2103725e1288b83ed364").get_lists("open")
cards = client.get_list("6203abc9bc236359a7d95d01").list_cards()

class Student:
    def __init__(self, name = "", course = ""):
        self.name = name
        self.course = course
        


def zip_text():
    students = []
    with open("members.txt", "r") as n:
        members = n.readlines()
    with open("courses.txt", "r") as c:
        courses = c.readlines()
    for name, course in zip(members, courses):
        students.append(Student(name.strip("\n"), course.strip("\n")))
    return students

        
        

def create_card(name, description):
    card = client.get_list("623f321d224bdc1093bf33f8").add_card(name, f"**Course**: {description}\n-----------------------\n")
    check_list = card.add_checklist("Submission of LP", ["Learning Packet 1", "Learning Packet 2", "Learning Packet 3", "Learning Packet 4"], [False, False, False, False])

students = zip_text()
for student in students:
    create_card(student.name, student.course)
    
# for i in range(3):
#     create_card(students[i].name, students[i].course)