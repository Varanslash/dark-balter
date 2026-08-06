import chess
import random

# Create a brand new board
board = chess.Board()
pgn = []
legal_show = input("Do you want to see all legal moves? (y/n): ")
name = input("What is your name? >>>")
elo = input("What is your elo? >>>")
showfen = input("Show FEN? (y/n)")
endnaming = f"{name} ({elo}) vs Dark Balter (900)"
turn = 0

peece = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def eval_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999  # Black delivered checkmate!
        else:
            return 99999   # White delivered checkmate!
    if board.is_game_over():
        return 0  # Draw
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = peece[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value  # White pieces add points
            else:
                score -= value  # Black pieces subtract points
    return score

def depth_eval(board, depth):
    moves = list(board.legal_moves)
    abs_bestscore = 29999999
    abs_bestmoves = []
    pushed = 0

    for move in moves:
        if board.turn == chess.WHITE:
            bestscore = -29999999
        else:
            bestscore = 29999999
        bestmove = []
        pushed = 1
        board.push(move)

        for _ in range(depth - 1):
            if board.is_game_over():
                break

            loop_moves = list(board.legal_moves)

            if board.turn == chess.WHITE:
                bestscore = -29999999
                bestmove = []
                for lmove in loop_moves:
                    board.push(lmove)
                    score = eval_board(board)
                    board.pop()
                    if score > bestscore:
                        bestscore = score
                        bestmove = [lmove]
                    elif score == bestscore:
                        bestmove.append(lmove)
                    else:
                        continue
                sb_move = random.choice(bestmove)
                board.push(sb_move)

            else:
                bestscore = 29999999
                bestmove = []
                for lmove in loop_moves:
                    board.push(lmove)
                    score = eval_board(board)
                    board.pop()
                    if score < bestscore:
                        bestscore = score
                        bestmove = [lmove]
                    elif score == bestscore:
                        bestmove.append(lmove)
                    else:
                        continue
                swb_move = random.choice(bestmove)
                board.push(swb_move)
            pushed += 1

        score = eval_board(board)

        for _ in range(pushed):
            board.pop()

        if score < abs_bestscore:
            abs_bestscore = score
            abs_bestmoves = [move]
        elif score == abs_bestscore:
            abs_bestmoves.append(move)

    res = random.choice(abs_bestmoves)
    return res

while not board.is_game_over():
    turn += 0.5
    # Check whose turn it is
    if board.turn: # Returns True for White, False for Black
        print(f"{name}'s turn")
    else:
        print("Balter's turn")

    # Get a list of every legal move available right now
    if board.turn:
        print(board)
        if legal_show == "y" or legal_show == "Y":
            print("Legal moves:", [board.san(move) for move in board.legal_moves])

        # Make a move (e.g., moving the e-pawn to e4)
        p_move = input("Enter your move in SAN format (e.g., e4): ")
        if p_move == "resign":
            print(f"{endnaming}: 0-1, Termination by resignation")
            print(pgn)
            exit()
        try:
            board.push_san(p_move)
            pgn.append(p_move)
        except ValueError:
            print("Invalid move. Please try again.")
    else:
        before = board.fen()
        b_move = depth_eval(board, 5)
        after = board.fen()
        if showfen == "y" or "Y":
            print(f"Before: {before} \n After: {after}")


        if before != after:
            print("SEARCH CORRUPTED THE BOARD")
            print("Before:", before)
            print("After: ", after)
            raise RuntimeError("depth_eval changed the board")

        bpgn_m = board.san(b_move)
        pgn.append(bpgn_m)
        print(f"Balter played {turn}. {bpgn_m}")
        board.push(b_move)
        print(board)

print(f"{name} ({elo}) vs Dark Balter (900): {board.result()}")
print(pgn)