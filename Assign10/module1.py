import pika
import time
import sys
from threading import Thread

check = False

notes = []
noteCtr = 0

#Send something stored in the notes array into the notesList2 queue, which is received by assign10.py
def sendNote():
    global noteCtr
    global notes
    tempCtr = noteCtr - 1
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='notesList2')

    if tempCtr >= 0:
        channel.basic_publish(exchange='', routing_key='notesList2', body=notes[tempCtr])

    connection.close()

    if tempCtr >= 0:
        notes[tempCtr] = ''
        noteCtr -= 1


#called when message is received from queue
def callback(ch, method, properties, body):
    global noteCtr
    global notes
    global check
    ctr = 1
    if body == "import" and noteCtr > 0:
        check = True
        connection.close()
        return

    #notes.append(body)

    #have here to print and prove it receives for now, notes.append(body) from above is all needed in final code?
    if check == False:
        notes.append(body)
        check = True
        for i in notes:
            print(str(ctr) + ". " + i.decode('utf-8'))
            ctr += 1

    else:
        notes.append(body)
        for i in notes:
            print(str(ctr) + ". " + i.decode('utf-8'))
            ctr += 1
    
    noteCtr += 1


#Open a connection with rabbitmq and receive a message from queue notesList1, sent from Assign10.py
def receiveNote():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='notesList1')

    channel.basic_consume(queue='notesList1', auto_ack=True, on_message_callback=callback)

    channel.start_consuming()


#thread setup
receiveThread = Thread(target= receiveNote)
sendThread = Thread(target= sendNote)

receiveThread.start()

sendThread.start()


while True:
    receiveNote()

    if check == True:
        print("test")
        sendNote()

    break



#if certain input (from button) in queue, send file back then start consuming again?