from tkinter import *
from tkinter import messagebox
from random import choice
import os
import sys
import copy

r = Tk()
r.config(bg="white")
r.title("Tic-Tac-Toe")
winHeight = 250
winWidth = 250
gap = 20
r.geometry(f"{winHeight}x{winWidth}")
r.resizable(False, False)

initialState = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]
gamstate = []
result = None

def startGame():
    global gameState
    gameState = copy.deepcopy(initialState)
    label.destroy()
    button.destroy()

    C.pack()
    C.bind("<Button-1>", handleClick)
    createBoard()
    displayStateToBoard(gameState)

def createBoard():
    i = 3
    while (i > 0):
        C.create_line(0, winHeight/i, winWidth, winHeight/i,fill="blue")
        C.create_line(winWidth/i, 0, winWidth/i, winHeight, fill="blue")
        i = i - 1.5
    
def displayStateToBoard(state):
    for i in range(3):
        for j in range(3):
            if (state[i][j] == 1):
                C.create_line(j*winWidth/3+gap, i*winHeight/3+gap, (j+1)*winWidth/3-gap, (i+1)*winHeight/3-gap, fill="red", width=2)
                C.create_line(j*winWidth/3+gap, (i+1)*winHeight/3-gap, (j+1)*winWidth/3-gap, i*winHeight/3+gap, fill="red", width=2)

            elif (state[i][j] == -1):
                C.create_oval(j*winWidth/3+gap, i*winHeight/3+gap, (j+1)*winWidth/3-gap, (i+1)*winHeight/3-gap, outline='blue', width=2)

def getPlayerTurn(state): # Returns which player's turn it is
    matrixToArray = [item for row in state for item in row]
    return -1 if (matrixToArray.count(1) + matrixToArray.count(-1)) % 2 else 1

def isTerminalState(state):
    global result
    copiedState = copy.deepcopy(state)
    matrixToArray = [item for row in copiedState for item in row]
    diagnolX = [copiedState[i][i] for i in range(3)]
    diagnolY = [copiedState[i][2-i] for i in range(3)]
    
    for i in range(3):
        columns = []
        rows = []
        for j in range(3):
            rows.append(copiedState[i][j])
            columns.append(copiedState[j][i])

        for array in [rows, columns, diagnolX, diagnolY]:
            if (sum(array) == 3):
                result = 1
            elif (sum(array) == -3):
                result = -1
            if result is not None:
                return True
    if (matrixToArray.count(0) == 0):
        result = 0
    return result is not None

clickCounter = 0
def handleClick(event):
    global gameState
    global clickCounter
    if not isTerminalState(gameState):
        x, y = event.x, event.y
        row = y // int(winHeight/3)
        col = x // int(winWidth/3)
        if 0 <= row < winHeight and 0 <= col < winWidth:
            if gameState[row][col] == 0:
                gameState = getTransistionState(gameState, [row, col])
                gameState = getNextBestState1MoveAhead(gameState)
                displayStateToBoard(gameState)
                if isTerminalState(gameState):
                    messagebox.showinfo("Game Over!", "Congratulations. You Won!" if result == 1 else "Game Over! Try Again.") 
    else:
        if clickCounter: os.execl(sys.executable, sys.executable, *sys.argv)
        info = Label(r, text="Click Again Anywhere To Restart", bg="white", fg="blue", padx=winWidth/10, pady=winHeight/8)
        info.place(x = (winWidth - info.winfo_reqwidth())/2, y = (winHeight - info.winfo_reqheight())/2)
        clickCounter += 1

def getNextRandomState(state):
    if isTerminalState(state): return state
    availableStates = [getTransistionState(state, action) for action in getActions(state)]
    return choice(availableStates)

def getNextBestState1MoveAhead(state):
    if isTerminalState(state): return state
    availableStatesForPlayer = [getTransistionState(state, action) for action in getActions(state)]
    drawingStatesForPlayer = []
    for availableStateForPlayer in availableStatesForPlayer:
        if isTerminalState(availableStateForPlayer):
            print("player", result)
            if result == getPlayerTurn(state):
                return availableStateForPlayer
            elif result == 0:
                drawingStatesForPlayer.append(availableStateForPlayer)
        # else:
        #     # availableStatesForOpponent = [getTransistionState(availableStateForPlayer, action) for action in getActions(state)]
        #     # for availableStateForOpponent in availableStatesForOpponent:
        #     #     if isTerminalState(availableStateForOpponent):
        #     #         print(availableStateForOpponent)
                    
                #     print("opponent", result)
                #     if result == getPlayerTurn(availableStateForPlayer):
                #         print(availableStatesForPlayer, len(availableStateForPlayer))
                #         availableStatesForPlayer.remove(availableStateForPlayer)

    return choice(drawingStatesForPlayer) if len(drawingStatesForPlayer) else choice(availableStatesForPlayer)

def getActions(state):
    actions = []
    if not isTerminalState(state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    actions.append([i, j])
    return actions

def getTransistionState(state, action):
    newState = copy.deepcopy(state)
    if not isTerminalState(newState):
        i, j = action
        newState[i][j] = getPlayerTurn(newState)
    return newState


label = Label(r, text="Tic-Tac-Toe", fg="darkblue", bg="white", pady=20, font=[1])
label.pack()
button = Button(r, text="Start", command=startGame, bg="darkblue", fg="white", bd=0, padx=20)
button.pack()
C = Canvas(r, height=winHeight, width=winWidth, bd=0, bg="white")

r.mainloop()