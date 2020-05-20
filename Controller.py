from flask import Flask, render_template, request, jsonify
from baseApp import app, db, socketio
from Model import ContactForm
from flask_mail import Mail,Message
import random
from flask_socketio import send, emit

players = []

@app.route("/")
def home():
    print()
    return render_template("index.html")

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('connect')
def test_connect():
    print('Client Connected')

@socketio.on('addPlayer')
def addPlayer(returnDict):
    newPlayer = Player(returnDict["socketId"])
    players.append(newPlayer)
    response = jsonify([player.__dict__ for player in players if player is not None])
    print('currentPlayers',response.data)
    emit('currentPlayers',response.data)

@socketio.on('disconnect')
def test_disconnect():
    removePlayer(players,request.sid)
    print('Client disconnected')

def removePlayer(playerList,socketId):
    if len(playerList) > 1:
        for player in playerList:
            if player.id == socketId:
                players.remove(player)
    response = jsonify([player.__dict__ for player in players])
    print('currentPlayers',response.data)
    emit('currentPlayers',response.data)
    print('here')


class Player():
    def __init__(self,socketId: str):
        self.id = socketId
        self.x = random.randint(0,10)
        self.y = random.randint(0,10)
        self.team = random.randint(0,3)
    
    def __repr__(self):
        return self.id
        
