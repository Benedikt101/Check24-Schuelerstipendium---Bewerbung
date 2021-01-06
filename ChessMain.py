import pygame as p
import ChessEngine

width = height = 512
dimensions = 8
sq_size = height//dimensions
max_fps = 15
images = {}
p.init()

def load_Images():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(f"pieces/{piece}.png"), (int(sq_size * 0.95), int(sq_size * 0.95)))

def main():
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    load_Images()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(f"{playerClicks[0][0]}{playerClicks[0][1]}{playerClicks[1][0]}{playerClicks[1][1]}")
                    print(move.getChessNotation())
                    if playerClicks[0] == (7,4) and playerClicks[1] == (7,6):
                        move = "w-O-O"
                    elif playerClicks[0] == (7,4) and playerClicks[1] == (7,2):
                        move = "w-O-O-O"
                    elif playerClicks[0] == (0,4) and playerClicks[1] == (0,6):
                        move = "b-O-O"
                    elif playerClicks[0] == (0,4) and playerClicks[1] == (0,2):
                        move = "b-O-O-O"
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen, gs.board)

def drawBoard(screen, board):
    colors = [p.Color(240, 218, 181), p.Color(181, 135, 99)]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

if __name__ == "__main__":
    main()