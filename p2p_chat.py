#B17CS001 - ABHINAV PANDEY
#IMPLEMENTING PEER TO PEER CHAT SYSTEM THAT MAINTAINS HISTORY EVEN AFTER CLIENT GOES OFFLINE
#------------------------------------------------------------------------------------------------



import socket       #socket programming library
import threading        #for multithreading, since both the sender and receiver should run concurrently
import mysql.connector      #for storing history of chats in mysql database

ENCODING = 'utf-8'

def listen(my_IP, my_port):         #the function that can listen on upto 10 connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            #creating the socket object
    sock.bind((my_IP, my_port))         #binding to the port given as input
    sock.listen(10)         #listen on upto 10 connections

    while True:         #in a while loop so that socket is ready to accept incoming data every time

        connection, client_address = sock.accept()          #accepting data sent by the sender
        try:
            full_message = ""
            while True:         #this loop runs till all incoming data is received in size of 16 bytes
                data = connection.recv(16)          #receive data in chunks of size 16 bytes
                full_message = full_message + data.decode(ENCODING)
                if not data:            #when incoming data is stopped
                    print(full_message.strip())         #print the message received along with the sender name
                    
                    friend, message = full_message.split(" : ", 1)          #separate the sender name and message to store into the database
                    
                    sql = "insert into data (sender, receiver,  message) values (%s, %s, %s)"           #sql query to insert data into table for later retrieval
                    val = (friend, "me", message)
                    mycursor.execute(sql, val)          #execute the sql command

                    mydb.commit()       #commit the changes made to the actual database table

                    break
        finally:
            connection.shutdown(2)          #to close the socket connection
            connection.close()


def send(friend_IP, friend_port, my_name):          #the function used to send message along with sender name

    while True:     #infinite loop so that one can always input the message to be sent to the connected friend
        message = input("")         #the message to be sent

        if message == "quit":           #'quit' command to break connection with the connected peer and so as to be able to connect to some other peer
            global flag
            flag = False
            break

        sql = "insert into data (sender, receiver, message) values (%s, %s, %s)"            #sql query to store the sent data for later retrieval so as to maintain history
        val = ("me", friend_name, message)
        mycursor.execute(sql, val)

        mydb.commit()

        message_with_name = my_name + " : " + message           #adding sender name with the message 

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #socket object
        s.connect((friend_IP, friend_port))         #connect with friend using his IP over the network and the port which he has opened to receive socket connections
        s.sendall(message_with_name.encode(ENCODING))       #send the message
        s.shutdown(2)           #break the connection
        s.close()       

    main()          #this is executed when 'quit' is called so as to connect to some other peer



def main():

    print("-----------------------------------")
    temp = input("Friend's Name : ")            #taking details of the peer to which we want to send messages
    global friend_name
    friend_name = temp
    friend_IP = input("Friend's IP : ")
    friend_port = int(input("Friend's Port : "))
    print("-----------------------------------")
    print()

sql = "select * from data where sender = %s union select * from data where receiver = %s order by sr_no"        #query to extract chat history corresponding to the peer name to which connection is to be established
    name = (friend_name, friend_name)
    mycursor.execute(sql, name)
    fetched_data = mycursor.fetchall()

    for data in fetched_data:           #printing chat history of the connected peer
        print(data[1] + " : " + data[3])
    print()


    if flag == True:
        receiver_thread = threading.Thread(target = listen, args = (my_IP, my_port))        #receiver thread object creation
    sender_thread = threading.Thread(target = send, args = (friend_IP, friend_port, my_name))       #sender thread object creation

    if flag == True:
        receiver_thread.start()         #receiver thread started
    sender_thread.start()           #sender thread

    if flag == True:
        receiver_thread.join()          #joining threads so that one runs after completion of the other
    sender_thread.join()



flag = True

print("-----------------------------------")
my_name = input("My Name : ")           #taking input of the user details
my_IP = "localhost"
my_port = int(input("My Port : "))
friend_name = ""

mydb = mysql.connector.connect(         #database object creation
    host="localhost",
    user="root",
    password="root_password",
    auth_plugin='mysql_native_password',
    database = "p2p_chat_history"
)

mycursor = mydb.cursor()

if __name__ == '__main__':
    main()