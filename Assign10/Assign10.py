import time
from tkinter import *
from tkinter.ttk import *
import sys
import pika
from threading import Thread

window = Tk()
counter = 0
yPlace = 100
warningCheck = False
currentFileInput = ''
fileContent = ''
tutorialHidden = True
userInput = ''
input = Text(window, height = 10, width = 20, wrap = WORD)


#Send the users input into the notesList1 queue, which is received by "module1.py" and stored
def sendNote():
    global userInput
    global input
    userInput = input.get(1.0, "end-1c")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='notesList1')

    channel.basic_publish(exchange='', routing_key='notesList1', body=userInput)

    connection.close()


#Receive the message sent from "module1.py"
def receiveNote():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='notesList2')

    channel.basic_consume(queue='notesList2', auto_ack=True, on_message_callback=callback)

    channel.start_consuming()


#thread setup
sendThread = Thread(target= sendNote)
receiveThread = Thread(target= receiveNote)

sendThread.start()
receiveThread.start()

#create entry window
inputFile = Entry(window, width = 50)

tutorial = Text(window, height = 5, width = 50, wrap = WORD)



#make a new note if there is room, later change into making a new window to condense code and remove smell
def makeNote():
    global warningCheck
    global counter
    xPlace = 200
    global yPlace
    global fileContent
    global userInput
    global input

    #creates input box inside window (this is the note)
    if counter == 0:
        input.place(x = xPlace, y = yPlace)
        input.insert('end', fileContent)

       
        saveButton = Button(window, text = "Save", command = sendNote())
        saveButton.place(x = xPlace + 45, y = yPlace + 165)

        counter += 1

    #if enough notes have been created, modify note placement formula so that the boxes do not overlap
    elif counter < 3:
        xPlace = xPlace + (250 * counter)
        input.place(x = xPlace, y = yPlace)
        input.insert('end', fileContent)

        saveButton = Button(window, text = "Save", command = sendNote())
        saveButton.place(x = xPlace + 45, y = yPlace + 165)

        counter += 1

    #update yPlace prior to 4 so that warningCheck works
    elif counter == 3:
        xPlace = xPlace + (250 * counter)
        input.place(x = xPlace, y = yPlace)
        input.insert('end', fileContent)

        saveButton = Button(window, text = "Save", command = sendNote())
        saveButton.place(x = xPlace + 45, y = yPlace + 165)

        counter += 1
        yPlace = yPlace + 200

    #make sure it does not overprint the warning
    elif warningCheck == True:
        pass

    #make warning that the max number of notes has been reached
    elif yPlace > 500:
        warning = Label(window, width = 50, text = "You have created the max number of notes!")
        warning.pack()
        warningCheck = True

    #creates a new row of notes
    elif counter == 4:
        counter = 0
        input.place(x = xPlace, y = yPlace)
        input.insert('end', fileContent)

        saveButton = Button(window, text = "Save", command = sendNote())
        saveButton.place(x = xPlace + 45, y = yPlace + 165)

        counter += 1

    #clear file content so that the next note created does not have unwanted text
    fileContent = ''


#what happens when something is received
def callback(ch, method, properties, body):
    global fileContent
    fileContent = body

    connection.close()



#take and store user input
def acceptInput():
    global fileContent

    receiveNote()

    makeNote()



#hide the tutorial box
def hideTutorial():
    global tutorial
    global tutorialHidden

    if tutorialHidden == False:
        tutorial.place(x = 675, y = 30)
        tutorialHidden = True

    elif tutorialHidden == True:
        tutorial.place_forget()
        tutorialHidden = False



#basic program loop
while True:
    window.geometry('1280x720')
    window.resizable(0, 0)

    #calls makeNote function to create a small note window when clicked
    noteButton = Button(window, text = 'New Note', command = makeNote)
    noteButton.place(x = 800, y = 0)

    importButton = Button(window, text = "Import", command = acceptInput)
    importButton.place(x = 875, y = 0)

    tutorial.place(x = 675, y = 30)
    tutorial.insert('end', "Use the 'New Note' button to create a note on the page. This will let you type anything! This will also create a save button to save your input in a file. Use the 'Import' button to take the name of a file to place the text of a file in a new note!")

    closeTutorial = Button(window, text = "Toggle Tutorial", command = hideTutorial)
    closeTutorial.place(x = 950, y = 0)

    window.mainloop()

    break