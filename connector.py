import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ben131199",
  database="ELECTION"
)

print(connection)
mycursor = connection.cursor()

mylist = []
records = []

stored = 0

sql = ""

# Function to calculate the most popular vote 
def most_common(lst):
    return max(set(lst), key=lst.count)

# Function to calculate the corresponding party name based from the party_id
def party_namer(winner):
    sql = """SELECT	PARTY_ID, PARTY_NAME
          FROM	CANDIDATE
          JOIN	PARTY ON CANDIDATE.PARTY_ID = PARTY.ID
          GROUP BY PARTY_ID, PARTY_NAME;"""
    mycursor.execute(sql)
    
    iterator = iter(range(72))
    next(iterator)
    
    for element in iterator:
        records = mycursor.fetchone()
        if winner == records[0]:
            name = records[1]
            
    return(name)


# Function to calculate total seats by constituency
def votes_by_constituency():
    iterator = iter(range(72))
    next(iterator)
    
    for n in iterator:
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        mycursor.execute(sql)
        records = mycursor.fetchone()
        #print("Record ", n, ": ", records[0]) # Used for debugging
        mylist.append(records[0])
    
    stored = max(mylist)    # Calculates the most popular party_id

# Function to calculate the total votes for each party

def votes_by_party():    
    iterator = iter(range(72))
    next(iterator)
    
    totalVotes=0
    percent=0
    
    for n in iterator:
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        mycursor.execute(sql)
        records = mycursor.fetchone()
        #print("Party ", n, ": ", records[0]) # Used for debugging
        mylist.append(records[0])
        totalVotes += records[0]
        
        if records[0] > percent:
            percent = records[0]

        
    print("\n", totalVotes, " was the total amount of votes in this election across all parties")
    percent = round((percent/totalVotes)*100, 2)
    print("\nThe winning party had ", percent, "% of the vote\n")

    print("Total number of seats awarded to the winning party: ", round((percent*650/100), 0))


def votes_by_party_threshold():
    for n in mylist:
        print(mylist)   






votes_by_constituency()

print("\n===================================================")







print("\nELECTION RESULTS BY CONSTITUENCY:\n")

seats = []

constID = iter(range(651))
next(constID)

for n in constID:
     
    sql = "SELECT PARTY_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(n)

    #print(sql)
    mycursor.execute(sql)
    records = mycursor.fetchone()
    #print(records)
    
    seats.append(records[0])
    
winningSeats = seats.count(most_common(seats))
winningID = most_common(seats)

print("The winning number of seats was - ", str(winningSeats))    # Calculates the most popular value in the list

winName = party_namer(winningID)

print("\nThe", winName, "Party - Is the winner of the election")
print("\n===================================================\n")

# Seats based on Simple Proportional Representation (All Votes)

print("Seats based on Simple Proportional Representation (All Votes)\n")
votes_by_party()

# Seats based on SImple Proportional Representation (5% Threshold)

print("\n===================================================\n")

print("Seats based on Simple Proportional Representation (5% Threshold)\n")

#votes_by_party_threshold()

def myfunc():
    
    partyID = iter(range(72))
    next(partyID)

    for n in constID:
        sql = "SELECT PARTY_ID, SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+ str(n)

        mycursor.execute(sql)
        records = mycursor.fetchone()
        print(records[0])
        # try to remove 5% of worst votes from list
myfunc()

# Ends mySQL Connector

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

