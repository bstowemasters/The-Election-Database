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

percent = 0

stored = 0

sql = ""
tab = ""

# Function to auto indent text for formatting in console.
def beautify_format(index):

    if len(party_namer(records[0])) <= 7:
        tab = "\t\t\t\t\t\t\t\t"
    if len(party_namer(records[0])) < 12 and len(party_namer(records[0])) > 7:
        tab = "\t\t\t\t\t\t\t"
    if len(party_namer(records[0])) >= 12 and len(party_namer(records[0])) <= 15:
        tab = "\t\t\t\t\t\t"
    if len(party_namer(records[0])) > 15 and len(party_namer(records[0])) <= 20:
        tab = "\t\t\t\t\t"
    
    if len(party_namer(records[0])) > 20 and len(party_namer(records[0])) < 25:
        tab = "\t\t\t\t"
    if len(party_namer(records[0])) >=25 and len(party_namer(records[0])) <30:
        tab = "\t\t\t"
    if len(party_namer(records[0])) >=30:
        tab = "\t"
        
    if index < 100 and len(party_namer(records[0])) >= 12 and len(party_namer(records[0])) <= 15:
        tab = "\t\t\t\t\t\t\t"
    if index < 100 and len(party_namer(records[0])) > 15 and len(party_namer(records[0])) <= 20:
        tab = "\t\t\t\t\t\t"
    return tab

# Function to calculate the most popular vote 
def most_common(lst):
    return max(set(lst), key=lst.count)

# Function to count amount of seats for each party
def seat_count():
    itr = iter(range(72))
    next(itr)

    for element in itr:
        print(party_namer(element), " - SEATS | ", constWinner.count(element))

# Function to calculate the corresponding party name based from the party_id
def party_namer(party):
    sql = """SELECT	PARTY_ID, PARTY_NAME
          FROM	CANDIDATE
          JOIN	PARTY ON CANDIDATE.PARTY_ID = PARTY.ID
          GROUP BY PARTY_ID, PARTY_NAME;"""
    mycursor.execute(sql)
    
    iterator = iter(range(72))
    next(iterator)
    
    for element in iterator:
        records = mycursor.fetchone()
        if party == records[0]:
            name = records[1]
            
    return(name)

#Function to print the votes information
def print_votes(lst):
    for element in lst:
        print(party_namer(element), ": Votes: ", lst[0], ", ", percent, "% of the total vote") # Used for debugging

# Function to calculate total seats by constituency
def votes_by_constituency():
    
    iterator = iter(range(72))
    next(iterator)
    
    for n in iterator:
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        mycursor.execute(sql)
        records = mycursor.fetchone()

        mylist.append(records[0])
        
        
    
    #stored = max(mylist)    # Calculates the most popular party_id

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


votes_by_constituency()

print("\n===================================================")






print("\nELECTION RESULTS BY CONSTITUENCY:\n")

constWinner = []

constID = iter(range(651))
next(constID)

for n in constID:
     
    sql = "SELECT PARTY_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(n)

    #print(sql)
    mycursor.execute(sql)
    records = mycursor.fetchone()

    tab = beautify_format(n)
    
    print("Constituency - ",str(n), ": ", party_namer(records[0]), tab, records[1], "| VOTES")
    
    constWinner.append(records[0])
    
winningSeats = constWinner.count(most_common(constWinner))
winningID = most_common(constWinner)

print("\nThe winning number of seats was - ", str(winningSeats), "\n")    # Calculates the most popular value in the list

winName = party_namer(winningID)

seat_count()


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

