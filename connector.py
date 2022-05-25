import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ben131199",
  database="ELECTION"
)

def most_common(lst):
    return max(set(lst), key=lst.count)

print(connection)

mylist = []
records = []

mycursor = connection.cursor()

sql = ""
stored = 0



iterator = iter(range(72))
next(iterator)

for n in iterator:
    sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
    mycursor.execute(sql)
    records = mycursor.fetchone()
    print("Record ", n, ": ", records[0])
    
    mylist.append(records[0])




print("=========")


for element in mylist:
    print(element)

stored = max(mylist)
print ("\n", stored, " - Was the highest number")


print("\nELECTION RESULTS BY CONSTITUENCY:\n")

seats = []

constID = iter(range(651))
next(constID)

for n in constID:
     
    sql = "SELECT PARTY_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(n)

    print(sql)
    mycursor.execute(sql)
    records = mycursor.fetchone()
    print(records)
    
    seats.append(records[0])
    
print(seats)

print("The winning number of seats was - ", seats.count(most_common(seats)))    # Calculates teh most popular value in the list

iterator = iter(range(72))
next(iterator)

for i in iterator:
    if most_common(seats) == iterator:
        

print(most_common(seats), " - Was the winner of the election")

mycursor.close()
connection.close()

 
  
"""
sql = "INSERT INTO products (name, type, description, material, colour, upholstered, upholstered_colour, cost, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

# To insert single entry
val = ("Cool Computer Desk", "Desk", "Computer Desk With Drawers", "MDF","White", 1, "Gloss White", 49.99, 89.99)


# To insert multiple entries:
    
val = [
       ('Modern Computer Desk', 'Desk', 'Computer Desk With Drawers', 'MDF','White', 1, 'Gloss White', 49.99, 89.99),
       ('3 - Drawer Chest', 'Drawers', 'Drawer Unit with black handles', 'MDF', 'Gloss White', 0, '', 29.99, 69.99),
       ('Swivel Chair', 'Chair', 'Computer Office Chair With Wheels', 'ABS Plastic','White & Black', 1, 'White Leather', 79.99, 189.99),
       ('Broken Bedside Unit', 'Bedroom Cabinets', 'Bedside cabinet With Drawers', 'Plywood', 'Black Oak', 0, '', 19.99, 39.99)
]  

mycursor.execute(sql, val)

mydb.commit()
print(mycursor.rowcount, "Record Added Successfully.")
"""

