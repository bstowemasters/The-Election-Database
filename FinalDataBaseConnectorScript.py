# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 09:52:03 2022

@author: stowe
"""

import mysql.connector
from colorama import Fore

connection = mysql.connector.connect(   # Specifying database connection credentials
  host="localhost",
  user="root",
  password="Ben131199",
  database="ELECTION"
)

print(connection)
mycursor = connection.cursor()

# Delete any curently stored results so that new results can be calculated incase of any data changes.

sql = "DELETE FROM RESULTS;"
mycursor.execute(sql)

# Some gloval variables and lists that need default values or using in multiple functions without passing.

party_votes = []
constWinners = []

records = []
seats = []
votes = []

percent = 0
stored = 0
totalVotes = 0 # Used for calculating total votes for lsit to be appended to mysql
totVotes = 0

sql = ""

completeResults = []    # Stores complete results to add to SQL table

# Stores the total number of votes accross all parties for later use
sql = "select sum(votes) from candidate"
mycursor.execute(sql)
votes = mycursor.fetchone()

# Function to output the title of the method used
def output(string):
    print()
    print(Fore.GREEN + "\n" + string)
    print('\033[39m')

# End of function

# Function to add passed elements to list ( to be appended to mySQL table )

def addToList(sys, pty, seat, pOfSeat, pOfVote, diff):
    completeResults.append([sys, pty, int(seat), round(pOfSeat, 2), round(pOfVote, 2), round(diff, 2)])

# End of function

# Function to calculate the winning candidate from each constituency
def votes_by_constituency():
    
    iterator = iter(range(72))
    next(iterator)
    
    for idx, n in enumerate(iterator):
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        mycursor.execute(sql)
        records = mycursor.fetchone()

        party_votes.append(records[0])  # Adds the total votes for each party to their corresponding party via an index in the list | etc index 0 = party 1 and store their votes in that index.
        
        
# End of function

# Function to calculate the results by simple proportion

partyPercent = []
partySeats = []

def votes_by_simpProp():    
    
    iterator = iter(range(72))
    next(iterator)
    
    global totalVotes
    totalVotes=0
    percent=0
    
    print(Fore.GREEN + "Election results by simple proportion\n")
    print('\033[39m')
    
    for n in iterator:
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        
        mycursor.execute(sql)
        records = mycursor.fetchone()
        
        totalVotes += records[0]
        partyPercent.append(records[0])
    
        
    for idx, element in enumerate(partyPercent):

        percent = round((partyPercent[idx]/totalVotes)*100, 2)
        numOfSeats = round((percent*650/100), 0)
        partySeats.append(numOfSeats)
        print(percent, "% of the vote\t|", "\tSeats | ", numOfSeats, "\t", party_namer(idx+1))
        addToList("Simple Proportional Representation - By Constituency", idx+1, partySeats[idx], percent, partySeats[idx]/650*100, (percent - (partySeats[idx]/650)*100))
        
    winningIndex = partyPercent.index(max(partyPercent))+1
    
    print("\n", totalVotes, " was the total amount of votes in this election across all parties")
    print(" Total number of seats awarded to the winning party: ", max(partySeats))
    print(" The winner of the election is ", party_namer(winningIndex))
    
    

    
    
# End of function    

# Function to calculate election results by simple proportion with 5% threshold
def votes_by_simpProp5():    
    
    partyPercent.clear()
    
    output("Election Results by simple proportion with 5% threshold\n")
    
    iterator = iter(range(72))
    next(iterator)
    
    totalVotes=0
    percent=0
    
    for n in iterator:
        sql = "SELECT SUM(VOTES), PARTY_ID FROM CANDIDATE WHERE PARTY_ID="+str(n)   # Used to iterate through all of the parties and their total votes.
        
        mycursor.execute(sql)
        records = mycursor.fetchone()
        
        if records[0]/votes[0]*100 >= 5:    # Removes invalid results that are below threshold of 5%
            totalVotes += records[0]
            partyPercent.append(records[0])
            
    for idx, element in enumerate(partyPercent):
            
        percent = round((partyPercent[idx]/totalVotes)*100, 2)
        numOfSeats = round((percent*650/100), 0)    # Calculate number of seats, round down to get whole number since you can't have 0.3 of a seat etc.
        partySeats.append(numOfSeats)
        print(percent, "% of the vote", "\tSeats | ", numOfSeats, "\t", party_namer(idx+1))
        addToList("Simple Proportional Representation 5% Threshold - By Constituency", idx+1, partySeats[idx], partySeats[idx]/650*100, percent, (partySeats[idx]/650)*100 - percent)
        
    winningIndex = partyPercent.index(max(partyPercent))+1  # Finds the index of the party with the highest percentage and stores the position to find the party name (1 is added to account for 0th index not existing in party id)
   
    print("\n", totalVotes, " was the total amount of votes in this election across all eligible parties")
    print(" Total number of seats awarded to the winning party: ", max(partySeats))
    print(" The winner of the election is ", party_namer(winningIndex))
    
    
# End of function
 
# Function to calculate votes on Largest Remainder Method
highestRemainder = [0, 0]
highest = 0

def largest_Remainder():
    
    output("Election Results by Largest Remainder (Hare-Niemeyer)") # Function called to output title in green colour for clarity.
    
    totVotes = 0
    
    sql = "SELECT SUM(VOTES) FROM CANDIDATE"# Used to store total amoun of votes
    mycursor.execute(sql)
    results = mycursor.fetchone()
    
    quota = results[0] / 650    # Calculates the quota.
    print("Minimum votes to meet quota: ", round(quota, 0), "\n")
    
    for idx, item in enumerate(party_votes):
        highest = highestRemainder[1]   # Sets the initial value to the current value to compare against other values.
        totVotes += party_votes[0]      # Adds the current votes to votes total.
        if (item % quota) != 0: # Checks if there even is a reaminder.
            if highest < item % quota:
                #highestRemainder.clear()
                highestRemainder[0] = idx # Sets the current party to the highest remainder.
                highestRemainder[1] = 1
    
    for idx, item in enumerate(party_votes):
        if idx != highestRemainder[0]:  # Checks if first iteration.
            seatNum = round((item / quota), 0)
            print(party_namer(idx+1), seatNum, " seats")
            addToList("Largest Remainder - All Votes", idx+1, seatNum, seatNum/650*100, party_votes[idx]/totalVotes*100, (seatNum/650*100 - (party_votes[idx]/totVotes)*100))
        else:
            print(party_namer(idx+1), round((item / quota), 0)+1, " seats <- Awarded seat for highest remainder")
 
# End of function    

# Output Election results by D'Hondt (All Votes)

pty_votes = [] # Temp storage for party votes since value is changed in function

def votes_by_dHont(): 
    
    global pty_votes
    pty_votes = party_votes.copy()  # Clones list and allows results to be changed globally in new list | To use in other functions.
    
    for idx, element in enumerate(seats):   # Reset all seats to 0
        seats[idx] = 0.0
        
    seatsCount = 0
    
    while seatsCount < 650: # Runs until all seats are allocated.
        
        for element in party_votes:             # Set all votes to their quotient
            idx = party_votes.index(element)
            #print(party_namer(idx+1), " Votes - " ,element)
            newVal = float(element) / (seats[idx] + 1)
                        
            party_votes[idx] = newVal
            
        
        winningQuot = max(party_votes)
        winningIdx = party_votes.index(winningQuot)
        
        #print (winningQuot, " is the top quotient value")
        seats[winningIdx] += 1  # Adds one seat to the highest quotient party.
        seatsCount += 1
    
    for idx, result in enumerate(seats):
        print(party_namer(idx+1), "\tSEATS | ", result )
        addToList("DHondt - All Votes", idx+1, result, result/650*100, pty_votes[idx]/totalVotes*100, (float(result/650*100) - float(pty_votes[idx]/totalVotes)*100))
    print()
    print(max(seats), " Was the winning number of seats")   # Find the element in list with the highest value | returns most seats out of parties. | Finds winner etc...
    winningIdx = seats.index(max(seats))
    print("\nThe winning party is... ", party_namer(winningIdx+1))  # 1 Is added to the index to account for no 0th party | parties index in sql starts at 1 not 0.
 
# End of function

# Function to calcuclate the number of seats in each region

areaSeats = []     # List to store the number of constituencies / seats allocated for each region (Only works if sorted in order)


def seats_by_method(method):
    
    # Select correct results to be returned from DB.
    if method == "County":
        sql = str("SELECT CONSTITUENCY_ID, COUNTY_ID, PARTY_ID, SUM(VOTES) FROM CANDIDATE GROUP BY CONSTITUENCY_ID, COUNTY_ID ORDER BY COUNTY_ID, PARTY_ID")
        areaSeats.clear()
    if method == "Region":
        sql = str("SELECT CONSTITUENCY_ID, REGION_ID, PARTY_ID, SUM(VOTES) FROM CANDIDATE GROUP BY CONSTITUENCY_ID, REGION_ID ORDER BY REGION_ID, PARTY_ID")
        
    count = 0
    
    #sql = str("SELECT CONSTITUENCY_ID, REGION_ID, PARTY_ID, SUM(VOTES) FROM CANDIDATE GROUP BY CONSTITUENCY_ID, REGION_ID ORDER BY REGION_ID, PARTY_ID")    # Test output to console.
    mycursor.execute(sql)
    records = mycursor.fetchall()
    
        
    for idx, n in enumerate(records):
        #party = int(records[2]) + 1    # Some test scripts here to check results and output to console.
        #print("Constituency " + str(n[0]) + " region:" + str(n[1]) + " Party " + str(n[2]) + "\n")
        #print(n)
        
        if n[1] == records[idx-1][1] and idx != 649:    # Check for last result since this will break the program as the last result can't be compared to the next result it's non existant.
            #print("same")
            count += 1
        else:
            #print("END BLOCK =========================")
            if idx != 0:
                if idx == 649:  # Accounts for error checking last result skipping final seat allocation
                    count += 1
                count += 1  # Accounts for starting at 0
                areaSeats.append(count) # Adds the total amount of seats (based on constituencies in area)
                count = 0   # Resets count for next iteration.

     
    print("Total Seats Per ", method, "\t" , areaSeats, "\n")
    
# End of function

# Function to calculate the votes by region using simple proportion

def results_by_simpProp_method(thresh, area):
    party = range(71)
    
    if area == "Region":
        value = range(12)
    if area == "County":
        sql = "SELECT COUNT(DISTINCT COUNTY_ID) FROM CANDIDATE;" # Work out the amount of different counties there are and save.
        mycursor.execute(sql)
        county = mycursor.fetchone()
        value = range(county[0])
    
    temp = "" # Stores the value of whether the 5% threshold is selected.
    if thresh == True:
        temp = " with 5% threshold" # Allows the correct title to be added to list and output to console.
    else:
        temp = ""
        

    totalAreaVotes = 0  # Start val at 0, allows for reset if reusing function.
    currAreaVotes = []

    for idx, s in enumerate(seats):
        seats[idx] = 0

    for v in value:
        #print("\nRegion: ", r+1, "\n")
        for p in party:
            
            # Assignment of sql query to return results based off method selected.
            if area == "Region":
                sql = "SELECT PARTY_ID, REGION_ID, SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID=" + str(p+1) + " AND REGION_ID=" + str(v+1)
            if area == "County":
                sql = "SELECT PARTY_ID, REGION_ID, SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID=" + str(p+1) + " AND COUNTY_ID=" + str(v+1)
                
            mycursor.execute(sql)
            results = mycursor.fetchone()
            
            #print(r, " - " ,p)
            if results[0] != None:  # Checks if no votes as working with null values provides errors.
                totalAreaVotes += results[2]
                tup = (results[0], results[1], results[2])  # Declare tuple to append to list
                currAreaVotes.append(list(tup)) # Append tuple to list for percentage calculation once total votes have been accumulated.
        
        if thresh == True:
            for idx, element in enumerate(currAreaVotes):   # Iterates through all parties calculating % of votes to check against threshold.
                percent = round(((element[2]/totalAreaVotes)*100), 0)
                if percent < 5:
                    totalAreaVotes -= element[2]    # Removes invalid votes from total
                    currAreaVotes.pop(idx)          # Removes invalid results from the list of eligible parties results.
        
        for element in currAreaVotes:   # Checks the current region / county votes for each party 
            percent = round(((element[2]/totalAreaVotes)*100), 0)   # Calculates % of votes.
                
            #print("Party: " + str(element[0]) + "\tRegion: " + str(element[1]) + "\tTotal Votes: " + str(element[2]) + "\t% of Vote: " + str(percent) + "%")
            
            idx = element[0]
                    
            seats[idx-1] += round((percent/100 * areaSeats[v]), 0)  # Allocates a seat for each winning party.
            
                
        currAreaVotes.clear() # Resest the list of region and party votes for next calculation of %
        #print("\nTotal Votes: ", str(totalRegionVotes))
        totalAreaVotes = 0



    for idx, count in enumerate(seats): # Outputs the amount of seats for each party by reading list
        print("Seats: ", count, " | " ,party_namer(idx+1))
        pOfSeats = float(count/650*100)
        pOfVotes = float(pty_votes[idx]) / float(totalVotes) * 100
        addToList("Simple Proportional Representation - By " + area + temp, idx+1, count, pOfSeats, pOfVotes, pOfSeats-pOfVotes)    # Adds results to list for adding to sql.
        
    win = seats.index(max(seats))
    print("\nThe winner of the election is ", party_namer(win+1), " with ", max(seats), " seats")
# End of function
    
# Function to calculate the corresponding party name based from the party_id
def party_namer(party): # Query to find the party name from the ID
    sql = """SELECT	PARTY_ID, PARTY_NAME
          FROM	CANDIDATE
          JOIN	PARTY ON CANDIDATE.PARTY_ID = PARTY.ID
          GROUP BY PARTY_ID, PARTY_NAME;"""
    mycursor.execute(sql)

    iterator = iter(range(72))  # Iterates through the party IDs
    next(iterator)
    
    for element in iterator:    # Iterates through the party IDs and find the corresponding party name
        records = mycursor.fetchone()
        
        if party == records[0]:
            name = records[1]
            
    return(name)
# End of function
   
# Function to count amount of seats for each party
def seat_count():

    # Write script to iterate through constituencies to add up seats
    iterator = iter(range(651))
    next(iterator)

    for idx, element in enumerate(iterator):
        sql = "SELECT PARTY_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(element) # Selects all of the constituencies and finds max amount of votes within constituency.
        mycursor.execute(sql)
        
        records = mycursor.fetchone()
        
        constWinners.append(records[0]) # Adds the constituency winner with the most votes to the list of party winners per constituency.
    
    parties = iter(range(72))
    next(parties)
    for idx, n in enumerate(parties):       # Iterate through the party IDs and count amount of winners
        seats.append(constWinners.count(n))
# End of function

# Function to print and add results to database.
def updateDB():
    # Output Results
    
    for res in completeResults:
        print(res[0], res[1], res[2], str(res[3])+"%", str(res[4])+"%", str(res[5])+"%")    # Outputs data in string format to confirm with user data to be added.
        
    print("\nAdding Results to Database... Please wait")
    
    # Add to SQL
    
    for res in completeResults:
        sql = "INSERT INTO RESULTS(SYS, PARTY, SEATS, PER_OF_SEATS, PER_OF_VOTES, DIFF) VALUES (%s, %s, %s, %s, %s, %s)"# Identifies values and variables to add to database
        val = (res[0], res[1], res[2], res[3], res[4], res[5])  # Adds data to values in sql query
        mycursor.execute(sql, val)  # Runs query to add values to database and specifies values.
    
    print("Adding data complete!")
    
    connection.commit()  #- Used to save the results to the database ( stops reset each run of script ) - Left open for marking purposes


# Output election results by Constituency

output("Election results by Constituency")

votes_by_constituency()
seat_count()

totalVts = 0

for idx, n in enumerate(party_votes):
    pName = party_namer(idx+1)
    print("Votes : ", n, "\t|\tSeats : ", seats[idx], "\t", pName)
    totalVts += n
    
index = seats.index(max(seats))
print("\n", max(seats), " Seats were awarded to ", party_namer(index+1), "\n Winning the election\n")

for idx, n in enumerate(party_votes):
    
    pOfSeats = seats[idx]/650
    pOfVotes = n/totalVts * 100
    diff = float(pOfVotes) - float(pOfSeats) * 100
    
    addToList("Past the Post - By Constituency", idx+1, seats[idx], pOfSeats*100, pOfVotes, diff)

# Output election results by Simple Proportion

votes_by_simpProp()

# Output election results by Simple Proportion with 5% threshold

votes_by_simpProp5()
print("\n")

# Output election results by Largest Remainder (Hare-Niemeyer) (All votes)

largest_Remainder()

print()
idx = party_votes.index(max(party_votes))
print("Election winner is " + party_namer(idx+1))

# Election results by D'Hondt Method

output("Election Results by D'Hondt Method:")

votes_by_dHont()

# Election results by Simple Proportion (by region)

output("Votes By Region | Simple Proportional Representation")

seats_by_method("Region") # Calculates the amount of constituencies (seats) in each region
results_by_simpProp_method(False, "Region")

# Results by Simple Proportion 5% Threshold (by region)

output("Votes By Region | Simple Proportional Representation 5% Threshold")

results_by_simpProp_method(True, "Region")

# Results by Simple Proportion (by county)

output("Votes By County | Simple Proportional Representation")

seats_by_method("County")
results_by_simpProp_method(False, "County")

# Results by Simple Proportion 5% Threshold (by county)

output("Votes By County | Simple Proportional Representation 5% Threshold")

seats_by_method("County")
results_by_simpProp_method(True, "County")

# Results by D'Hondt by County

""" Couldn't crack this one
def votes_by_dHont_method(thresh, area):
    
    for idx, element in enumerate(seats):   # Reset all seats to 0
        seats[idx] = 0.0
    
    party = range(71)
    
    if area == "Region":
        value = range(12)
    if area == "County":
        sql = "SELECT COUNT(DISTINCT COUNTY_ID) FROM CANDIDATE;"
        mycursor.execute(sql)
        county = mycursor.fetchone()
        value = range(county[0])
    
    temp = "" # Stores the value of whether the 5% threshold is selected.
    if thresh == True:
        temp = " with 5% threshold"
    else:
        temp = ""
    
    global pty_votes
    pty_votes = party_votes.copy()
    
    for v in value:
        for p in party:
            # Assignment of sql query to return results based off method selected.
            if area == "Region":
                sql = "SELECT PARTY_ID, REGION_ID, SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID=" + str(p+1) + " AND REGION_ID=" + str(v+1)
            if area == "County":
                sql = "SELECT PARTY_ID, REGION_ID, SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID=" + str(p+1) + " AND COUNTY_ID=" + str(v+1)
            
            mycursor.execute(sql)
            results = mycursor.fetchone()
            pty_votes[p] = results[2] 
        
    seatsCount = 0
    
    while seatsCount < 650:
        
        for element in pty_votes:             # Set all votes to their quotient
            idx = pty_votes.index(element)
            #print(party_namer(idx+1), " Votes - " ,element)
            if element != None:
                newVal = float(element) / (areaSeats[idx] + 1)
                pty_votes[idx] = newVal
            
        
        winningQuot = max(party_votes)
        winningIdx = pty_votes.index(winningQuot)
        
        #print (winningQuot, " is the top quotient value")
        seats[winningIdx] += 1
        seatsCount += 1
    
    for idx, result in enumerate(seats):
        print(party_namer(idx+1), "\tSEATS | ", result )
        #addToList("DHondt - By " + area + temp, idx+1, result, result/650*100, pty_votes[idx]/totalVotes*100, (float(result/650*100) - float(pty_votes[idx]/totalVotes)*100))
    print()
    print(max(seats), " Was the winning number of seats")
    winningIdx = seats.index(max(seats))
    print("\nThe winning party is... ", party_namer(winningIdx+1))
 
# End of function



seats_by_method("County")
output("Votes By D'Hondt Method - By County")
votes_by_dHont_method(False, "County")

# END

"""

# Add results to database

updateDB()

""" Check if data has been added - commented out since test was successful.
sql = "select * from results"
mycursor.execute(sql)
result = mycursor.fetchall()

for element in result:
    print(element)
"""

# Closing active connection

mycursor.close()
connection.close()
                


