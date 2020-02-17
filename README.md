# Peer-to-Peer-Chat-System-with-chat-History

Peer to Peer Chat Application with Chat History
------------------------------------------------

Dependencies:
1) Python 3
2) MySQL Server Connection


How to Run:

1. install MySQL Server
2. Create database and table using the code given in db_creation.sql
3. Use the login credentials of SQL server account in "p2p_chat.py" on lines 116 and 117
4. run "python3 p2p_chat.py" on your system
5. steps 1 to 4 need to be followed by other peers who want to establish connection

Input Format:
1. Enter Your Details(Name, port)
2. Input Friend details(Peer Name, Peer IP, Peer's connection Port)
3. Enter 'quit' to stop sending messages to stop connection to the connected peer and make connection to some other peer

Output Format:
1. Chat History with the connected peer is shown as soon as the peer is connected
2. Messages from upto 10 peers will be received
