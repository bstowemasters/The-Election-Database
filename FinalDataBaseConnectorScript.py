# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 09:52:03 2022

@author: stowe
"""

import mysql.connector
from colorama import Fore

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ben131199",
  database="ELECTION"
)

print(connection)
mycursor = connection.cursor()

party_votes = []
constWinners = []

records = []
seats = []
votes = []
percent = 0

stored = 0

sql = ""
tab = ""

# Stores the total number of votes accross all parties for later use
sql = "select sum(votes) from candidate"
mycursor.execute(sql)
votes = mycursor.fetchone()

# Function to calculate the winning candidate from each constituency
def votes_by_constituency():
    
    iterator = iter(range(72))
    next(iterator)
    
    for idx, n in enumerate(iterator):
        sql = "SELECT SUM(VOTES) FROM CANDIDATE WHERE PARTY_ID="+str(n)
        mycursor.execute(sql)
        records = mycursor.fetchone()

        party_votes.append(records[0])
        
# End of function

# Function to calculate the results by simple proportion
partyPercent = []
partySeats = []

def votes_by_simpProp():    
    
    iterator = iter(range(72))
    next(iterator)
    
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
        print(party_namer(idx+1), " gained", percent, "% of the vote", "\tSeats | ", numOfSeats)
            
    winningIndex = partyPercent.index(max(partyPercent))+1
    
    print("\n", totalVotes, " was the total amount of votes in this election across all parties")
    print(" Total number of seats awarded to the winning party: ", max(partySeats))
    print(" The winner of the election is ", party_namer(winningIndex))
    
    
# End of function    

# Function to calculate election results by simple proportion with 5% threshold
def votes_by_simpProp5():    
    
    partyPercent.clear()
    
    print(Fore.GREEN + "\nElection Results by simple proportion with 5% threshold\n")
    print('\033[39m')
    
    iterator = iter(range(72))
    next(iterator)
    
    totalVotes=0
    percent=0
    
    for n in iterator:
        sql = "SELECT SUM(VOTES), PARTY_ID FROM CANDIDATE WHERE PARTY_ID="+str(n)
        
        mycursor.execute(sql)
        records = mycursor.fetchone()
        
        if records[0]/votes[0]*100 >= 5:
            totalVotes += records[0]
            partyPercent.append(records[0])
            
    for idx, element in enumerate(partyPercent):
            
        percent = round((partyPercent[idx]/totalVotes)*100, 2)
        numOfSeats = round((percent*650/100), 0)
        partySeats.append(numOfSeats)
        print(party_namer(idx+1), " gained", percent, "% of the vote", "\tSeats | ", numOfSeats)
           
    winningIndex = partyPercent.index(max(partyPercent))+1
   
    print("\n", totalVotes, " was the total amount of votes in this election across all eligible parties")
    print(" Total number of seats awarded to the winning party: ", max(partySeats))
    print(" The winner of the election is ", party_namer(winningIndex))
    
# End of function
 
# Function to calculate votes on Largest Remainder Method
highestRemainder = [0, 0]
highest = 0

def largest_Remainder():
    
    print(Fore.GREEN + "Election Results by Largest Remainder (Hare-Niemeyer)")
    print("\033[39m")
    
    sql = "SELECT SUM(VOTES) FROM CANDIDATE"
    mycursor.execute(sql)
    results = mycursor.fetchone()
    
    quota = results[0] / 650
    print("Minimum votes to meet quota: ", round(quota, 0), "\n")
    
    for idx, item in enumerate(party_votes):
        highest = highestRemainder[1]
        if (item % quota) != 0:
            if highest < item % quota:
                #highestRemainder.clear()
                highestRemainder[0] = idx
                highestRemainder[1] = 1
    
    for idx, item in enumerate(party_votes):
        if idx != highestRemainder[0]:
            print(party_namer(idx+1), round((item / quota), 0), " seats")
        else:
            print(party_namer(idx+1), round((item / quota), 0)+1, " seats <- Awarded seat for highest remainder")
 
# End of function    

# Output Election results by D'Hondt (All Votes)

def votes_by_dHont():
        
    for idx, element in enumerate(seats):   # Reset all seats to 0
        seats[idx] = 0.0
        
    seatsCount = 0
    
    while seatsCount < 650:
        
        for element in party_votes:             # Set all votes to their quotient
            idx = party_votes.index(element)
            #print(party_namer(idx+1), " Votes - " ,element)
            newVal = float(element) / (seats[idx] + 1)
            
            #print(idx)                                       # Commented print statements for debugging
            
            party_votes[idx] = newVal
            
        
        winningQuot = max(party_votes)
        winningIdx = party_votes.index(winningQuot)
        
        #print (winningQuot, " is the top quotient value")
        seats[winningIdx] += 1
        seatsCount += 1
    
    for idx, result in enumerate(seats):
        print(party_namer(idx+1), "\tSEATS | ", result )
    
    print()
    print(max(seats), " Was the winning number of seats")
    winningIdx = seats.index(max(seats))
    print("\nThe winning party is... ", party_namer(winningIdx+1))
 
# End of function
    
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
# End of function
   
# Function to count amount of seats for each party
def seat_count():

    # Write script to iterate through constituencies to add up seats
    iterator = iter(range(651))
    next(iterator)

    for idx, element in enumerate(iterator):
        sql = "SELECT PARTY_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(element)
        mycursor.execute(sql)
        
        records = mycursor.fetchone()
        
        constWinners.append(records[0])
    
    parties = iter(range(72))
    next(parties)
    for idx, n in enumerate(parties):       # Iterate through the party IDs and count amount of winners
        seats.append(constWinners.count(n))
# End of function

# Output election results by Constituency
        
votes_by_constituency()
seat_count()

print(Fore.GREEN + "\nElection results by Constituency\n")
print('\033[39m')


for idx, n in enumerate(party_votes):
    pName = party_namer(idx+1)
    print(pName, "\tVotes : ",n, "\t|\tSeats : ", seats[idx])
    
index = seats.index(max(seats))
print("\n", max(seats), " Seats were awarded to ", party_namer(index+1), "\n Winning the election\n")

# Output election results by Simple Proportion

votes_by_simpProp()

# Output election results by Simple Proportion with 5% threshold

votes_by_simpProp5()
print("\n")

# Output election results by Largest Remainder (Hare-Niemeyer) (All votes)

largest_Remainder()

print()
idx = party_votes.index(max(party_votes))
print ("Election winner is " + party_namer(idx+1))

# Election results by D'Hondt Method

print(Fore.GREEN + "\nElection Results by D'Hondt Method:")
print('\033[39m')
votes_by_dHont()

print()
print(Fore.GREEN + "Votes By Region | Simple Proportional Representation")
print('\033[39m')

def seats_by_region():
    
    regionSeats = []     # List to store the number of constituencies / seats allocated for each region (Only works if sorted in order)
    count = 0
    
    sql = str("SELECT CONSTITUENCY_ID, REGION_ID, PARTY_ID, SUM(VOTES) FROM CANDIDATE GROUP BY CONSTITUENCY_ID, REGION_ID ORDER BY REGION_ID, PARTY_ID")
    mycursor.execute(sql)
    records = mycursor.fetchall()
    
        
    for idx, n in enumerate(records):
        #party = int(records[2]) + 1
        print("Constituency " + str(n[0]) + " region:" + str(n[1]) + " Party " + str(n[2]) + "\n")
        print(n)
        
        if n[1] == records[idx-1][1] and idx != 649:
            print("same")
            count += 1
        else:
            print("END BLOCK =========================")
            if idx != 0:
                if idx == 649:  # Accounts for error checking last result skipping final seat allocation
                    count += 1
                count += 1
                regionSeats.append(count)
                count = 0

     
    print(regionSeats)

seats_by_region()

def newVotes():
    
    constWinners.clear()
    regionVotes = []
    currRegVotes = 0
    
    consts = iter(range(651))
    next(consts)

    for idx, element in enumerate(consts):
        sql = "SELECT PARTY_ID, REGION_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(element)
        mycursor.execute(sql)
        results = mycursor.fetchone()
        
        nextCursor = connection.cursor()
        nextResults = []
        
        if idx != 0:
            sql = "SELECT PARTY_ID, REGION_ID, MAX(VOTES) FROM CANDIDATE WHERE CONSTITUENCY_ID="+ str(element+1) + " ORDER BY REGION_ID"
            nextCursor.execute(sql)
            nextResults = nextCursor.fetchone()
        
            nextRes = nextResults
            
            if nextRes[1] == results[1]:
                currRegVotes += results[2]
            else:
                if currRegVotes != 0:
                    regionVotes.append("Votes: " + str(currRegVotes) + "\tParty ID: " + str(results[0]) + "\tRegion: " + str(results[1]))
                    currRegVotes = 0
        nextCursor.close()
    print(regionVotes)
    print("=====")
    
    for e in regionVotes:
        print(e)
    
    
newVotes()



mycursor.close()
connection.close()
                


