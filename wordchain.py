# WordChain program (part 1)
# Name: Aaron Tan
# Student Number: 10471321

# Import the necessary modules.
import random
import urllib.request
import json
import string

# This inputWord function repeatedly prompts for input until the user enters
# something at least one character long and entirely alphabetic.
# Use a recursive function to call itself instead of using a while True loop.
def inputWord(prompt):
    while True:
        name = input(prompt).strip()
        if name.isalpha() == False:
            print("Invalid. Try again.")
        else:
            return name.lower()

#This inputInt function repeatedly prompts for an input until the user
#input as an integer.
def inputInt(prompt):
    while True:
        number = input(prompt)
        try:
            checkInt = int(number)
        except ValueError:
            print("Invalid. Try again.")
            continue
        return checkInt

#Initialise variables
chain = 0
wordTypes = ['noun','verb','adjective']
playerNames = []
usedWords = []
playerCount = 0

#Begin
print('Welcome to WordChain!')
while True:
    numPlayers = inputInt("How many players (minimum of 2)?: ")
    if numPlayers <2:
        print("Invalid input. You can't input less then 2 players.")
    else:
        #Loops through each player from the number of players.
        for eachPlayer in range(numPlayers):
            name = inputWord("Enter name of player " + str(eachPlayer+1) + ": ")
            playerNames.append(name.title())
        break

#Main gameplay loop.
while True:
    wordType = random.choice(wordTypes)

    #If the game begins for the first time. Randomly select a letter by using a string module.
    if chain == 0:
        startLetter = random.choice(string.ascii_letters).lower()
    else:
        startLetter = word[-1]

    vowels = ['a','e','i','o','u']
    if wordType[0] in vowels:
        determiner = 'an'
    else:
        determiner = 'a'

    #Display player's turn, instruction and player's input.
    print("\n" + playerNames[playerCount] + " is up next.")
    print("Enter ",determiner," ",wordType, " beginning with '", startLetter.upper(), "'", sep="")
    word = inputWord("> ")

    if word[0] == startLetter and word not in usedWords:
        #Send the request to the web server to test if the word is in the wordType
        response = urllib.request.urlopen('http://api.wordnik.com:80/v4/word.json/' \
                                  + word \
                                  + '/definitions?limit=5&partOfSpeech=' \
                                  + wordType \
                                  + '&api_key=aaaa946871985c2eb2004061aba0695e00190753d6560ebea')
        #Grab or load the wordData from the response.
        wordData = json.load(response)
        
   
        #If the user entered the correct
        #start letter and the wordData in list is nothing (means there is no actual json data.)
        #Stop the wordChain.
        if not wordData:
            print("The word", word, "does not contain any data. End program.")
            break
            
        print("Good job, ",playerNames[playerCount], " -'", word, "' is a ", wordType, " defined as...", sep="")
        for eachDef in wordData:
            print(" •" , eachDef['text'])

        chain +=1
        if chain >=2:
            plural = "s"
        else:
            plural = ""
        print("\nThe word chain is now ", chain, " link", plural, " long!", sep="")
        playerCount +=1
        usedWords.append(word)

    else:
        print("Word chain broken - '",word, "' does not appear to be ",determiner," ", wordType ,sep="")
        break

    if playerCount == numPlayers:
        playerCount = 0

#Show final chain length and record a log of the game.
print("\nFinal chain length: " + str(chain))

#Create a new dictionary and pre-set the keys and values.
gameRecord = {"players":numPlayers, "names":playerNames, "chain":chain}

#If the file do exist, it reads the data and use the "logs" variable to hold or grab the list data.
try:
    file = open('logs.txt','r')
    logs = json.load(file)
    file.close()

#If the file does not exist, create an empty list.    
except Exception:
    logs = []
    
finally:
    logs.append(gameRecord)
    file = open('logs.txt','w')
    json.dump(logs, file, indent=4)
    file.close()

    print("Game log saved.")
