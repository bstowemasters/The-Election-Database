# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 09:52:03 2022

@author: stowe
"""

import mysql.connector
import colorama 
from colorama import Fore, Back

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

print(Fore.GREEN + "Election results by simple proportion\n")
print('\033[39m')

votes_by_simpProp()

# Output election results by Simple Proportion with 5% threshold

print(Fore.GREEN + "\nElection Results by simple proportion with 5% threshold\n")
print('\033[39m')
   

votes_by_simpProp5()

# Output election results by Largest Remainder (Hare-Niemeyer) (All votes)

highestRemainder = [0, 0]
highest = 0

def largest_Remainder():
    sql = "SELECT SUM(VOTES) FROM CANDIDATE"
    mycursor.execute(sql)
    results = mycursor.fetchone()
    
    quota = results[0] / 650
    print(quota)
    
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
            print(party_namer(idx+1), round((item / quota), 0)+1, " seats <- Awarded Additional seat for highest remainder")

largest_Remainder()
