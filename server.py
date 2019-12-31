import socket
from _thread import *
import pickle
import sys
from user import User
import copy

server = "192.168.1.22"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen() #NUMBER OF CONNECTIONS(PEOPLE)
print("Waiting for a connection, Server Started")

users = {}
idCount = 0
def threaded_client(conn,y):
    newlist = list()
    for i in users.keys():
        newlist.append(i)
    nl = []
    for i in newlist:
        nl.append([i,users[i].password])
    conn.send(pickle.dumps(nl))
    userId= conn.recv(2048).decode()
    try:
        h = users[userId]
    except:
        users[userId] = User(userId)
    conn.send(pickle.dumps(users[userId]))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            #if users[userId].received[0] != None:
             #   print(users[userId].received, "recieved")
            data.received = users[userId].received
            users[userId] = data
            if not data:
                print("Disconnected")
                break
            else:

                if data.message[0] != None:
                    message = data.message
                    try:
                        h = users[message[1]]
                        users[message[1]].received = (message[0], userId)
                    except:
                        users[message[1]] = User(message[1])
                        users[message[1]].history.append((message[0], userId))


            u = copy.deepcopy(users[userId])
            users[userId].received = (None,None)
            conn.sendall(pickle.dumps(u))
        except:
            break


    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client,(conn,1))