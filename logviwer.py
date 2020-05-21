# Logviwer program (part 2)
# Name: Aaron Tan
# Student Number: 10471321 

# Import the necessary modules.

import tkinter
import tkinter.messagebox
import json

class ProgramGUI:
    def __init__(self):
        #Set the main window properties.
        self.main = tkinter.Tk()
        self.main.geometry('500x500+400+100')
        self.main.title("WordChain Log Viewer")

        try:
            self.logs = open('logs.txt','r')
            self.logsData = json.load(self.logs)
            self.logs.close()
        except Exception:
            self.error = tkinter.messagebox.showerror("Error", "File either don't exist or does not contain any Json data.")
            self.main.destroy()
            return 

        #Specify which index and then you can later use this self.nextLog to specify which list index
        #you want to retrieve. 
        self.nextLog = 0 
      
        #Set frames
        self.logFrame = tkinter.Frame()
        self.playerFrame= tkinter.Frame()
        self.chainFrame = tkinter.Frame()
        self.buttonFrame = tkinter.Frame()

        #1. logFrame (top frame)
        self.logLabel = tkinter.Label(self.logFrame, text='Log #:')
        self.logNumDisplay = tkinter.Label(self.logFrame, text=self.nextLog)
        
        self.logLabel.pack(side='left')
        self.logNumDisplay.pack(side='left')

        #2. playerFrame (middle-upper frame)
        self.playerLabel = tkinter.Label(self.playerFrame, text="Players:")
        self.numPlayersDisplay = tkinter.Label(self.playerFrame, text='')
        
        self.playerLabel.pack(side='left')
        self.numPlayersDisplay.pack(side='left')

        #3. chainFrame (middle-lower frame)
        self.chainLabel = tkinter.Label(self.chainFrame, text="Chain Length:")
        self.numChainsDisplay = tkinter.Label(self.chainFrame, text='')

        self.chainLabel.pack(side='left')
        self.numChainsDisplay.pack(side='left')

        #4. buttonFrame (bottom frame)
        self.nextButton = tkinter.Button(self.buttonFrame, text='Next Log', command = self.showLog ,width=15, height=3 )
        self.showButton = tkinter.Button(self.buttonFrame, text='Show Stats', command = self.showStats, width=15, height=3)

        self.nextButton.pack(side='left')
        self.showButton.pack(side='left')
        
        #Set the "packs" frames.
        self.logFrame.pack()
        self.playerFrame.pack()
        self.chainFrame.pack()
        self.buttonFrame.pack()

        self.showLog()
        tkinter.mainloop()
       
        
    def showLog(self):
        try:
            self.comma = ", "
            #Make changes when the user clicked "nextLog" to display the next stats.
            
            self.numPlayersDisplay.configure(text=str(self.logsData[self.nextLog]['players']) \
            + " (" + str(self.comma.join(self.logsData[self.nextLog]['names']) + ")"))
            self.numChainsDisplay.configure(text=self.logsData[self.nextLog]['chain'])
            
            self.logNumDisplay.configure(text=self.nextLog + 1)
            self.nextLog += 1
     
        except IndexError:
            tkinter.messagebox.showwarning('End of file','No more logs to show.')
            self.nextButton.configure(state='disabled')

    def showStats(self):
        #Initalise total attributes:
        self.totalPlayers = 0
        self.totalChains = 0

        #Loop through each index in a list (contain dicitonaries)
        for items in self.logsData:
            self.totalPlayers += items['players']
            self.totalChains += items['chain']
         
        self.average = self.totalPlayers // len(self.logsData)
                
        tkinter.messagebox.showinfo('WordChain Statistics', 'Number of Games: ' + str(len(self.logsData))\
                                        + "\n Average Players: " + str(self.average) \
                                        + "\n Max chain: " + str(self.totalChains))

# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
