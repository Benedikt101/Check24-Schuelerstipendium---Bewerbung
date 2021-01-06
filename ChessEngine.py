import copy

class ValidMoves():
    def __init__(self):
        self.validMoves = []

    def getValidMoves(self, board, wtm, movelog):
        color = "b"
        if wtm:
            color = "w"
        for r in range(8):
            for c in range(8):
                self.piece = board[r][c]
                if self.piece != "--" and self.piece[0] == color:
                    eval(f"self.valid{self.piece[-1]}Moves({r}, {c}, '{self.piece[0]}', board)")
        self.checkCastling(board, movelog)
        return self.validMoves

    def validPMoves(self, r, c, color, board):
        canMove2Sq = False
        if color == "w" and r == 6 or color == "b" and r == 1:
            canMove2Sq = True
        move1, move2, move3 = -1, -2, -1
        if color == "b":
            move1, move2, move3 = 1, 2, 1
        move4, move5 = 1, -1
        if c == 7:
            move4 = 0
        elif c == 0:
            move5 = 0
        if board[r+move1][c] == "--":
            self.validMoves.append(f"{r}{c}{r+move1}{c}")
            #1-Feld nach Vorne
        if -1 < r+move2 < 8:
            if board[r+move2][c] == "--" and canMove2Sq and  board[r+move3][c] == "--":
                self.validMoves.append(f"{r}{c}{r+move2}{c}")
                #2-Felder nach Vorne
        if board[r+move1][c+move4] != "--"  and board[r+move1][c+move4][0] != color:
            self.validMoves.append(f"{r}{c}{r+move1}{c+move4}")
            #Schlagen-rechts
        if board[r+move1][c+move5] != "--" and board[r+move1][c+move5][0] != color:
            self.validMoves.append(f"{r}{c}{r+move1}{c+move5}")
            #Schlagen-libks

    def validRMoves(self, r, c, color, board):
        var = [(1,1,0,0,8),(-1,-1,0,0,-1),(0,0,-1,-1,-1),(0,0,1,1,8)]
        for i in range(4):
            counter, increment, counter2, increment2, limit = var[i]
            while True:
                if c + counter != limit and r + counter2 != limit:
                    if board[r+counter2][c+counter] == "--":
                        self.validMoves.append(f"{r}{c}{r+counter2}{c+counter}")
                        counter += increment
                        counter2 += increment2
                    elif board[r+counter2][c+counter][0] != color:
                        self.validMoves.append(f"{r}{c}{r+counter2}{c+counter}")
                        break
                    else:
                        break
                else:
                    break

    def validNMoves(self, r, c, color, board):
        coords = [(2,1),(-2,1),(1,2),(-1,2)]
        for i in range(4):
            increment1, increment2 = coords[i]
            if r + increment1 < 8 and r + increment1 > -1:
                if c + increment2 < 8:
                    if board[r+increment1][c+increment2] == "--":
                        self.validMoves.append(f"{r}{c}{r+increment1}{c+increment2}")
                    elif board[r+increment1][c+increment2][0] != color:
                        self.validMoves.append(f"{r}{c}{r+increment1}{c+increment2}")
                if c - increment2 > -1:
                    if board[r+increment1][c-increment2] == "--":
                        self.validMoves.append(f"{r}{c}{r+increment1}{c-increment2}")
                    elif board[r+increment1][c-increment2][0] != color:
                        self.validMoves.append(f"{r}{c}{r+increment1}{c-increment2}")

    def validBMoves(self, r, c, color, board):
        var = [(1,1,1,1), (-1,-1,1,1), (-1,-1,-1,-1),(1,1,-1,-1)]
        for i in range(4):
            counter, increment, counter2, increment2 = var[i]
            while True:
                if c + counter > -1 and c+ counter < 8 and r + counter2 > -1 and r + counter2 < 8:
                    if board[r+counter2][c+counter] == "--":
                        self.validMoves.append(f"{r}{c}{r+counter2}{c+counter}")
                        counter += increment
                        counter2 += increment2
                    elif board[r+counter2][c+counter][0] != color:
                        self.validMoves.append(f"{r}{c}{r+counter2}{c+counter}")
                        break
                    else:
                        break
                else:
                    break

    def validQMoves(self, r, c, color, board):
        self.validRMoves(r,c,color, board)
        self.validBMoves(r,c,color, board)

    def validKMoves(self, r, c, color, board):
        coords = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        for i in range(8):
            coord1, coord2 = coords[i]
            if r + coord1 > -1 and r+coord1 < 8 and c + coord2 > -1 and c + coord2 < 8:
                if board[r+coord1][c+coord2] == "--":
                    self.validMoves.append(f"{r}{c}{r+coord1}{c+coord2}")
                elif board[r+coord1][c+coord2][0] != color:
                    self.validMoves.append(f"{r}{c}{r+coord1}{c+coord2}")

    def checkCastling(self, board, movelog):
        kingpositionwhite, kingpositionblack = None, None
        for i, x in enumerate(board):
            if "wK" in x:
                kingpositionwhite = (i, x.index("wK"))
            if "bK" in x:
                kingpositionblack = (i, x.index("bK"))
        movelog2 = []
        for i in movelog:
            movelog2.append(i[:2])
        if kingpositionwhite == (7, 4) and not "74" in movelog2:
            if board[7][0] == "wR" and not "70" in movelog2 and board[7][1] == "--" and board[7][2] == "--" and board[7][3] == "--":
                self.validMoves.append("w-O-O-O")
            if board[7][7] == "wR" and not "77" in movelog2 and board[7][6] == "--" and board[7][5] == "--":
                self.validMoves.append("w-O-O")
        if kingpositionblack == (0, 4) and not "04" in movelog2:
            if board[0][0] == "bR" and not "00" in movelog2 and board[0][1] == "--" and board[0][2] == "--" and board[0][3] == "--":
                self.validMoves.append("b-O-O-O")
            if board[0][7] == "wR" and not "07" in movelog2 and board[0][6] == "--" and board[0][5] == "--":
                self.validMoves.append("b-O-O")


class CheckSpecialPositions():
    def getPiecePosition(self, board, piece):
        for i, x in enumerate(board):
            if piece in x:
                return f"{i}{x.index(piece)}"

    def checkCheck(self, board, wtm, movelog):
        color = "b"
        if wtm:
            color = "w"
        wtm = not wtm
        vMnM = ValidMoves.getValidMoves(ValidMoves(), board, wtm, movelog) #getValidMoves von der anderen Farbe
        kingposition = self.getPiecePosition(board, f"{color}K")
        vMnM2 = []
        for i in vMnM:
            vMnM2.append(i[2:])
        if kingposition in vMnM2:
            return True
        else:
            return False

    def checkStalemate(self, board, wtm, movelog):
        if ValidMoves.getValidMoves(ValidMoves(), board, wtm, movelog) == []:
            return True

    def checkMate(self, board, wtm, movelog):
        vM = ValidMoves.getValidMoves(ValidMoves(), board, wtm, movelog)
        movestoremove = []
        for i in vM:
            self.copyboard = copy.deepcopy(board)
            Move.makeMove(Move(i), self.copyboard, wtm, i)
            if self.checkCheck(self.copyboard, wtm, movelog):
                movestoremove.append(i)
        for i in movestoremove:
            if i in vM:
                vM.remove(i)
        if vM == []:
            return True
        else:
            return vM

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.movelog = []
        self.validmoves = ValidMoves.getValidMoves(ValidMoves(), self.board, self.whiteToMove, self.movelog)
        self.gamefinished = False

    def checkPawnPromotion(self):
        if "wP" in self.board[0]:
            self.board[0][self.board[0].index("wP")] = "wQ"
        if "bP" in self.board[7]:
            self.board[7][self.board[7].index("bP")] = "bQ"

    def makeMove(self, move):
        vm = ValidMoves()
        if not isinstance(move, str):
            move = move.move
        if move in self.validmoves:
            Move.makeMove(Move(move), self.board, self.whiteToMove, move)
            self.checkPawnPromotion()
            self.movelog.append(move)
            self.whiteToMove = not self.whiteToMove
            if CheckSpecialPositions.checkCheck(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                mate = CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog)
                if mate == True:
                    self.validmoves = []
                    print("CHECKMATE")
                    self.gamefinished = True
                else:
                    self.validmoves = mate
                    print("CHECK")
            elif CheckSpecialPositions.checkStalemate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                print("stalemate")
                self.gamefinished = True
            else:
                self.validmoves = ValidMoves.getValidMoves(vm, self.board, self.whiteToMove, self.movelog)
                if CheckSpecialPositions.checkCheck(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                    if not CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                        self.validMoves = CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog)
                    else:
                        self.validMoves = []
            self.aiMove()

    def aiMove(self):
        vm = ValidMoves()
        if not self.whiteToMove and self.gamefinished == False:
            mn = MiniMax(self.board, self.whiteToMove, self.movelog)
            move = mn.minimax(0, True, -150, 150)[0]
            Move.makeMove(Move(move), self.board, self.whiteToMove, move)
            self.checkPawnPromotion()
            self.movelog.append(move)
            self.whiteToMove = not self.whiteToMove
            if CheckSpecialPositions.checkCheck(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                mate = CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog)
                if mate == True:
                    self.validmoves = []
                    print("CHECKMATE")
                    self.gamefinished = True
                else:
                    self.validmoves = mate
                    print("CHECK")
            else:
                self.validmoves = ValidMoves.getValidMoves(vm, self.board, self.whiteToMove, self.movelog)
                if CheckSpecialPositions.checkCheck(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                    if not CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog):
                        self.validMoves = CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.board, self.whiteToMove, self.movelog)
                    else:
                        self.validMoves = []

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, move):
        self.move = move

    def getChessNotation(self):
        return self.getRankFile(int(self.move[0]), int(self.move[1])) + self.getRankFile(int(self.move[2]), int(self.move[3]))

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def makeMove(self, board, wtm, move):
        coordsks = (6,5,4,7)
        coordsqs = (2,3,4,0)
        if self.move[2:] == "O-O" or self.move[2:] == "O-O-O":
            if wtm and self.move[0] == "w":
                if self.move == "w-O-O":
                    coords = coordsks
                else:
                    coords = coordsqs
                c1, c2, c3 ,c4 = coords
                board[7][c1] = "wK"
                board[7][c2] = "wR"
                board[7][c3] = "--"
                board[7][c4] = "--"
            elif not wtm and self.move[0] == "b":
                if self.move == "b-O-O":
                    coords = coordsks
                else:
                    coords = coordsqs
                c1, c2, c3, c4 = coords
                board[0][c1] = "bK"
                board[0][c2] = "bR"
                board[0][c3] = "--"
                board[0][c4] = "--"
        else:
            board[int(move[2])][int(move[3])] = board[int(move[0])][int(move[1])]
            board[int(move[0])][int(move[1])] = "--"

class EvaluatePosition():
    def __init__(self, board, validmovesBlack, validmovesWhite, color):
        self.board = board
        self.vMB = validmovesBlack
        self.vMW = validmovesWhite
        self.w = 0
        self.b = 0
        self.color = color

    def getPieceValues(self):
        pieceValues = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
        for j in range(8):
            for i in self.board[j]:
                if i != "--":
                    if i[0] == "w":
                        self.w += pieceValues[i[1]]
                    else:
                        self.b += pieceValues[i[1]]

    def pieceDevelopment(self):
        self.w += round((len(self.vMW) * 0.01), 2)
        self.b += round((len(self.vMB) * 0.01), 2)

    def kingSafety(self):
        #Wieviele Bauern sind in der Nähe des Königs + wie weit ist der nächste Bauer auf der Königslinie vom König entfernt
        kingpositionblack, kingpositionwhite = None, None
        for j in range(8):
            for i in self.board[j]:
                if i[1] == "K":
                    if i[0] == "w":
                        kingpositionwhite = (j, self.board[j].index("wK"))
                    else:
                        kingpositionblack = (j, self.board[j].index("bK"))
        whitePawn = []
        blackPawn = []
        wdkp =  bdkp = 8 #Distance from King to nearest Pawn on file
        if kingpositionblack != None and kingpositionwhite != None:
            for i in range(8):
                if self.board[i][kingpositionwhite[0]] == "wP":
                    whitePawn.append(i)
                if self.board[i][kingpositionblack[0]] == "bP":
                    blackPawn.append(i)
            for i in whitePawn:
                if abs(i - kingpositionwhite[1]) < wdkp:
                    wdkp = abs(i - kingpositionwhite[0])
            for i in blackPawn:
                if abs(i - kingpositionblack[1]) < bdkp:
                    bdkp = abs(i - kingpositionblack[0])

            self.w += round(wdkp/100, 2)
            self.b += round(bdkp/100, 2)
            vars = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1,-1), (-1, 0), (-1, -1)]
            kingpositions = [kingpositionwhite, kingpositionblack]
            for j in range(2):
                kingpos = kingpositions[j]
                for i in range(8):
                    var1, var2 = vars[i]
                    if 8 > kingpos[0] + var1 > -1 and 8 > kingpos[1] + var2 > -1:
                        debug = self.board[kingpos[0]+ var1][kingpos[1]+ var2]
                        if self.board[kingpos[0]+ var1][kingpos[1]+ var2][1] == "P":
                            if self.board[kingpos[0]+ var1][kingpos[1]+ var2][0] == "w":
                                self.w += 0.01
                            else:
                                self.b += 0.01

    def centerControl(self):
        centersquares1 = ["33", "34", "43", "44"]
        centersquares2 = ["23", "24", "53", "54", "32", "42", "35", "45"]
        lists = (self.vMW, self.vMB)
        for y in range(2):
            validmoves = lists[y]
            for i in validmoves:
                if i[1] != "-":
                    vars = (i[-2:], i[:2])
                    for x in range(2):
                        j = vars[x]
                        if j in centersquares1:
                            if y == 0:
                                self.w += 0.05
                                round(self.w, 2)
                            else:
                                self.b += 0.05
                                round(self.b, 2)
                        if j in centersquares2:
                            if y == 0:
                                self.w += 0.01
                                round(self.w, 2)
                            else:
                                self.b += 0.01
                                round(self.b, 2)

    def pawnStructure(self):
        validmoves = (self.vMW, self.vMB)
        vars = (1, -1)
        for y in range(2):
            vM = validmoves[y]
            var = vars[y]
            for i in vM:
                if i[1] != "-":
                    if self.board[int(i[0])][int(i[1])][1] == "P":
                        if -1 < int(i[0]) + var < 8:
                            if int(i[1]) +1 < 8:
                                if self.board[int(i[0]) + var][int(i[1])+1] == self.board[int(i[0])][int(i[1])]:
                                    if self.board[int(i[0])][int(i[1])][0] == "w":
                                        self.w += 0.01
                                    else:
                                        self.b += 0.01
                            if int(i[1]) -1 > -1:
                                if self.board[int(i[0]) + var][int(i[1])-1] == self.board[int(i[0])][int(i[1])]:
                                    if self.board[int(i[0])][int(i[1])][0] == "w":
                                        self.w += 0.01
                                    else:
                                        self.b += 0.01

    def evalPosition(self):
        self.getPieceValues()
        self.pieceDevelopment()
        self.kingSafety()
        self.centerControl()
        self.pawnStructure()
        if self.color == "w":
            return self.w - self.b
        else:
            return self.b - self.w

class MiniMax():
    def __init__(self, board, wtm, movelog):
        self.copyboard = copy.deepcopy(board)
        self.whiteToMove = wtm
        self.max_color = "b"
        self.color = False
        if self.whiteToMove:
            self.max_color = "w"
            self.color = True        #False == black, True == white
        self.targetDepth = 2
        self.movecopy = movelog.copy()

    def CheckGameEndings(self):
        if CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.copyboard, self.whiteToMove, self.movecopy) == True:
            if self.color == self.whiteToMove:
                return -1
            else:
                return 1
        elif CheckSpecialPositions.checkStalemate(CheckSpecialPositions(), self.copyboard, self.whiteToMove, self.movecopy):
            return 0

    def minimax(self, currentdepth, max_player, alpha, beta):
        gameend = self.CheckGameEndings()
        if gameend == -1:
            return None, -150
        elif gameend == 1:
            return None, 150
        elif gameend == 0:
            return None, 0
        if currentdepth == self.targetDepth:
            ev = EvaluatePosition(self.copyboard, ValidMoves.getValidMoves(ValidMoves(), self.copyboard, False, self.movecopy), ValidMoves.getValidMoves(ValidMoves(), self.copyboard, True, self.movecopy), self.max_color)
            return None, ev.evalPosition()
        vm = ValidMoves.getValidMoves(ValidMoves(), self.copyboard, self.whiteToMove, self.movecopy)
        if CheckSpecialPositions.checkCheck(CheckSpecialPositions(), self.copyboard, self.whiteToMove, self.movecopy):
                    if not CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.copyboard, self.whiteToMove, self.movecopy):
                        self.validMoves = CheckSpecialPositions.checkMate(CheckSpecialPositions(), self.copyboard, self.whiteToMove, self.movecopy)
                    else:
                        self.validMoves = []
        best_move = None

        if max_player:
            max_pos = -200
            for i in vm:
                undoBoard = copy.deepcopy(self.copyboard)
                Move.makeMove(Move(i), self.copyboard, self.whiteToMove, i)
                self.movecopy.append(i)
                self.whiteToMove = not self.whiteToMove
                current_pos = self.minimax(currentdepth + 1, False, alpha, beta)[1]
                if current_pos > max_pos:
                    max_pos = current_pos
                    best_move = i
                self.copyboard = undoBoard
                self.whiteToMove = not self.whiteToMove
                self.movecopy.pop(-1)
                alpha = max(alpha, current_pos)
                if beta <= alpha:
                    break
            return best_move, max_pos

        else:
            min_pos = 200
            vm.sort(reverse = True)
            for i in vm:
                undoBoard = copy.deepcopy(self.copyboard)
                Move.makeMove(Move(i), self.copyboard, self.whiteToMove, i)
                self.movecopy.append(i)
                self.whiteToMove = not self.whiteToMove
                current_pos = self.minimax(currentdepth + 1, True, alpha, beta)[1]
                if current_pos < min_pos:
                    min_pos = current_pos
                    best_move = i
                self.copyboard = undoBoard
                self.whiteToMove = not self.whiteToMove
                self.movecopy.pop(-1)
                beta = min(beta, current_pos)
                if beta <= alpha:
                    break
            return best_move, min_pos
