from flask import Flask, request, jsonify, render_template
import copy

app = Flask(__name__)

def piece_to_logic(piece, type):
    if(piece[type] == "a"):
        if type:
            piece = piece[0] + "1" + piece[2]
        else:
            piece = "1" + piece[1]
    elif(piece[type] == "b"):
        if type:
            piece = piece[0] + "2" + piece[2]
        else:
            piece = "2" + piece[1]
    elif(piece[type] == "c"):
        if type:
            piece = piece[0] + "3" + piece[2]
        else:
            piece = "3" + piece[1]
    elif(piece[type] == "d"):
        if type:
            piece = piece[0] + "4" + piece[2]
        else:
            piece = "4" + piece[1]
    elif(piece[type] == "e"):
        if type:
            piece = piece[0] + "5" + piece[2]
        else:
            piece = "5" + piece[1]
    elif(piece[type] == "f"):
        if type:
            piece = piece[0] + "6" + piece[2]
        else:
            piece = "6" + piece[1]
    elif(piece[type] == "g"):
        if type:
            piece = piece[0] + "7" + piece[2]
        else:
            piece = "7" + piece[1]
    elif(piece[type] == "h"):
        if type:
            piece = piece[0] + "8" + piece[2]
        else:
            piece = "8" + piece[1]
    return piece

def logic_to_piece(num, type):
    if(num[type] == "1"):
        if type:
            num = num[0] + "a" + num[2]
        else:
            num = "a" + num[1]
    elif(num[type] == "2"):
        if type:
            num = num[0] + "b" + num[2]
        else:
            num = "b" + num[1]
    elif(num[type] == "3"):
        if type:
            num = num[0] + "c" + num[2]
        else:
            num = "c" + num[1]
    elif(num[type] == "4"):
        if type:
            num = num[0] + "d" + num[2]
        else:
            num = "d" + num[1]
    elif(num[type] == "5"):
        if type:
            num = num[0] + "e" + num[2]
        else:
            num = "e" + num[1]
    elif(num[type] == "6"):
        if type:
            num = num[0] + "f" + num[2]
        else:
            num = "f" + num[1]
    elif(num[type] == "7"):
        if type:
            num = num[0] + "g" + num[2]
        else:
            num = "g" + num[1]
    elif(num[type] == "8"):
        if type:
            num = num[0] + "h" + num[2]
        else:
            num = "h" + num[1]
    return num

def piece_on_another(piece_num, pieces):
    for item in pieces:
        item = piece_to_logic(item, 1)
        if int(item[1:3]) == piece_num:
            return 1
        
def piece_off_edge(piece_num):
    if ((piece_num-(piece_num%10))/10 > 8) or ((piece_num-(piece_num%10))/10 < 1):
        return 1
    if ((piece_num%10) > 8) or ((piece_num%10) < 1):
        return 1
    else:
        return 0

def straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, num):
    if (piece_num - next_square_num) % num == 0:
        if (next_square_num - piece_num) > 0:
            piece_num += num
            while not (piece_num == next_square_num):
                if piece_on_another(piece_num, current_pieces):
                    return 0
                if piece_on_another(piece_num, opponent_pieces):
                    return 0
                if piece_off_edge(piece_num):
                    return 0
                piece_num += num
        else:
            piece_num -= num
            while not (piece_num == next_square_num):
                if piece_on_another(piece_num, current_pieces):
                    return 0
                if piece_on_another(piece_num, opponent_pieces):
                    return 0
                if piece_off_edge(piece_num):
                    return 0
                piece_num -= num
        if piece_on_another(piece_num, current_pieces):
            return 0
        return 1
    else:
        return 0

def move_valid(set, piece, next_square, side, ignore_own_king):

    current_pieces = set[side]
    opponent_pieces = set[not side]

    if not (piece in current_pieces):
        return 0
        
    if next_square == "0-0" or next_square == "0-0-0":
        if side == 0:
            castles_row = "1"
        else:
            castles_row = "8"

        rook_check = 0
        if next_square == "0-0":
            if not set[2 + side][1]:
                return 0
            for piece in current_pieces:
                if piece == "rh" + castles_row:
                    rook_check = 1

            castles_attacker_columns = ["e","f","g"]
            castles_piece_check_columns = ["f","g"]
        else:
            if not set[side+2][0]:
                return 0
            for piece in current_pieces:
                if piece == "ra" + castles_row:
                    rook_check = 1

            castles_attacker_columns = ["e","d","c"]
            castles_piece_check_columns = ["b","c","d"]

        if not rook_check:
            return 0

        for attacking_piece in opponent_pieces:
            for letter_attack in castles_attacker_columns:
                if move_valid(set, attacking_piece,(letter_attack + castles_row), not side, 1):
                    return 0
        for letter_piece_check in castles_piece_check_columns:
            square = letter_piece_check + castles_row
            for piece in current_pieces:
                if square == piece[1:3]:
                    return 0
            for piece in opponent_pieces:
                if square == piece[1:3]:
                    return 0
        return 1
    
    return_val = 1
    piece_str = piece_to_logic(piece, 1)
    next_square_str = piece_to_logic(next_square, 0)
    piece_num = int(piece_str[1:3])
    next_square_num = int(next_square_str)
    
    for item in current_pieces:
        item = piece_to_logic(item, 1)
        if int(item[1:3]) == next_square_num:
            return 0

    if(piece[0] == "r"):
        straight_1 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 1)
        straight_2 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 10)
        return_val = (straight_1 or straight_2)
    
    elif(piece[0] == "b"):
        diag_1 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 9)
        diag_2 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 11)
        return_val = (diag_1 or diag_2)
        
    elif(piece[0] == "n"):
        diff = next_square_num-piece_num
        if (diff == 12) or (diff == -12) or (diff == 8) or (diff == -8) or (diff == 21) or (diff == -21) or (diff == 19) or (diff == -19):
            pass
        else:
            return_val = 0
        
    elif(piece[0] == "p"):
        diff = next_square_num - piece_num

        #1 for white and -1 for black
        side_num = (-1) ** (side+2)

        #single move ahead
        if (diff == side_num * 1):
            if piece_on_another(next_square_num, opponent_pieces):
                return_val = 0

        #double move ahead        
        elif (diff == side_num * 2):
            if side == 0:
                double_check = 2
            else:
                double_check = 7
            if (piece_num%10) != double_check:
                return_val = 0
            elif piece_on_another(next_square_num, opponent_pieces):
                return_val = 0
            elif piece_on_another(next_square_num - (side_num * 1), opponent_pieces):
                return_val = 0
            elif piece_on_another(next_square_num - (side_num * 1), current_pieces):
                return_val = 0

        #move to corners
        elif (diff == side_num * 11) or (diff == side_num * -9):
            en_passant_row = 3 + (not side) * 3
            if (en_passant_row == int(next_square[1])) and (set[4 + side] == next_square[0]):
                pass
            elif piece_on_another(next_square_num, opponent_pieces):
                pass
            else:
                return_val = 0
        else:
            return_val = 0
            
    elif(piece[0] == "k"):
        diff = next_square_num - piece_num
        if (diff == 1) or (diff == -1) or (diff == 10) or (diff == -10) or (diff == 11) or (diff == -11) or (diff == 9) or (diff == -9):
            pass
        else:
            return_val = 0
    
    elif(piece[0] == "q"):
        straight_1 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 1)
        straight_2 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 10)
        diag_1 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 9)
        diag_2 = straight_or_diag(piece_num, next_square_num, current_pieces, opponent_pieces, 11)
        return_val = (straight_1 or straight_2 or diag_1 or diag_2)

    #make sure own king is not attacked after move is made
    if return_val == 1:
        if ignore_own_king:
            return 1
        else:
            set_replica = [copy.copy(item) for item in set]
            set_replica = make_move(set_replica, side, piece, "none", next_square)
            for square in set_replica[side]:
                if square[0] == "k":
                    king_square = square[1:3]

            for attacking_piece in set_replica[not side]:
                if move_valid(set_replica, attacking_piece, king_square, not side, 1):
                    return 0
            return 1
    else:
        return 0

def checkmate_or_stalemate(set, side):
    check_pieces = set[not side]
    not_checkmate_or_stalemate = 0
    for piece in check_pieces:
        valid_moves = all_legal_moves(piece, set, not side)
        if len(valid_moves) > 0:
            not_checkmate_or_stalemate = 1
            break
    if not not_checkmate_or_stalemate:
        for piece in check_pieces:
            if piece[0] == "k":
                king_square = piece[1:3]
                break
        current_pieces = set[side]
        can_attack = 0
        for piece in current_pieces:
            if move_valid(set, piece, king_square, side, 1):
                can_attack = 1
                break
        if can_attack:
            return [1,0]
        else:
            return [0,1]
    else:
        return [0,0]


def make_move(set, side, piece, promotion_piece, next_square):
    #set en passant to invalid for both sides
    if set[4] != "none" or set[5] != "none":
        set[4] = "none"
        set[5] = "none"

    #castling rights taken
    if piece[0] == "k":
            set[2 + side][0] = 0
            set[2 + side][1] = 0
    if piece[1:3] == "a1" or piece[1:3] == "a8":
        set[2 + side][0] = 0
    if piece[1:3] == "h1" or piece[1:3] == "h8":
        set[2 + side][1] = 0

    if next_square == "0-0" or next_square == "0-0-0":
        #castling rights taken
        set[2 + side][0] = 0
        set[2 + side][1] = 0

        if not side:
            castles_row = "1"
        else:
            castles_row = "8"
        if next_square == "0-0":
            rook_before_letter = "h"
            king_after_letter = "g"
            rook_after_letter = "f"
        else:
            rook_before_letter = "a"
            king_after_letter = "c"
            rook_after_letter = "d"
        set = make_move(set, side, "ke" + castles_row, "none", king_after_letter + castles_row)
        set = make_move(set, side, "r" + rook_before_letter + castles_row, "none", rook_after_letter + castles_row)

    else:
        move_space = abs(int(piece_to_logic(piece, 1)[1:3]) - int(piece_to_logic(next_square, 0)))

        if(piece[0] == "p"):
            #set en passant to valid for specified column
            if move_space == 2:
                set[4 + (not side)] = piece[1]

            #if en passant then delete pawn behind
            if ((move_space == 11) or (move_space == 9)):
                #1 for white and -1 for black
                side_num = (-1) ** (side+2)

                if not piece_on_another(int(piece_to_logic(next_square, 0)), set[not side]):
                    en_passant_takes_square = next_square[0] + str(int(next_square[1]) - side_num)
                    for opponent_piece in set[not side]:
                        if opponent_piece[1:3] == en_passant_takes_square:
                            set[not side].remove(opponent_piece)

        next_piece_type = piece[0]

        #check for promotion
        if promotion_piece != "none":
            next_piece_type = promotion_piece

        #move piece
        set[side][set[side].index(piece)] = next_piece_type + next_square

        #delete opponent piece if landed on
        for opponent_piece in set[not side]:
            if opponent_piece[1:3] == next_square:
                set[not side].remove(opponent_piece)

    return set

def position_evaluation(set, side):
    check = checkmate_or_stalemate(set,side)
    if check[0]:
        return 1000000
    if check[1]:
        return 0
    current_pieces = set[side]
    opponent_pieces = set[not side]
    current_score = 0
    opponent_score = 0
    for piece in current_pieces:
        if piece[0] == "r":
            current_score += 5
        elif piece[0] == "n":
            current_score += 3
        elif piece[0] == "b":
            current_score += 3
        elif piece[0] == "q":
            current_score += 9
        if piece[0] == "p":
            current_score += 1
    for piece in opponent_pieces:
        if piece[0] == "r":
            opponent_score += 5
        elif piece[0] == "n":
            opponent_score += 3
        elif piece[0] == "b":
            opponent_score += 3
        elif piece[0] == "q":
            opponent_score += 9
        if piece[0] == "p":
            opponent_score += 1

    return (current_score - opponent_score)

def all_legal_moves(piece, set, side):
    square_logic = piece_to_logic(piece, 1)[1:3]
    legal_squares =[]
    if (piece[0] == "r") or (piece[0] == "b") or (piece[0] == "q"):
        if piece[0] == "r":
            try_list = [1,-1,10,-10]
        elif piece[0] == "b":
            try_list = [9,-9,11,-11]
        elif piece[0] == "q":
            try_list = [1,-1,10,-10,9,-9,11,-11]
        for try_num in try_list:
            valid = 1
            square_logic_append = copy.copy(square_logic)
            while valid:
                square_logic_append = str(int(square_logic_append) + try_num)
                if not (piece_off_edge(int(square_logic_append))):
                    square_append = logic_to_piece(square_logic_append, 0)
                    if move_valid(set, piece, square_append, side, 0):
                        legal_squares.append(square_append)
                    else:
                        if piece_on_another(int(square_logic_append), set[side]) or piece_on_another(int(square_logic_append) - try_num, set[not side]):
                            valid = 0
                else:
                    valid = 0
    
    elif(piece[0] == "p" or piece[0] == "k" or piece[0] == "n"):
        if piece[0] == "p":
            #1 for white and -1 for black
            side_num = (-1) ** (side+2)
            try_list = [side_num, side_num*2, side_num * 11, side_num * -9]
        elif(piece[0] == "k"):
            try_list = [1, -1, 10, -10, 11, -11, 9, -9]
            if move_valid(set, piece, "0-0", side, 0):
                    legal_squares.append("0-0")
            if move_valid(set, piece, "0-0-0", side, 0):
                    legal_squares.append("0-0-0")
        elif(piece[0] == "n"):
            try_list = [12, -12, 8, -8, 21, -21, 19, -19]
        for try_num in try_list:
            square_logic_append = copy.copy(square_logic)
            square_logic_append = str(int(square_logic_append) + try_num)
            if not (piece_off_edge(int(square_logic_append))):
                square_append = logic_to_piece(square_logic_append, 0)
                if move_valid(set, piece, square_append, side, 0):
                    legal_squares.append(square_append)
        

    return legal_squares

def computer_move(set, side, depth):
    if depth == 0:
        return [-position_evaluation(set, side), None, None]

    else:
        list_eval_piece_promotion_move = []
        for piece in set[side]:
            legal_moves = all_legal_moves(piece, set, side)
            for next_square in legal_moves:

                #address pawn promotion and make valid moves
                promotion_list = ["none"]
                if piece[0] == "p" and (next_square[1] == 1 or next_square[1] == 8):
                    promotion_list = ["r","b","n","q"]
                for promotion_piece in promotion_list:
                    set_replica = [copy.copy(item) for item in set]
                    make_move(set_replica, side, piece, promotion_piece, next_square)

                    #append lower recursive call results to list
                    list_eval_piece_promotion_move.append([computer_move(set_replica, not side, depth - 1)[0]] + [piece, promotion_piece, next_square])

        #address no legal moves
        if len(list_eval_piece_promotion_move) == 0:
            return [position_evaluation(set, not side), None, None]

        return_item = list_eval_piece_promotion_move[0]
        max_val = list_eval_piece_promotion_move[0][0]

        for potential_return_item in list_eval_piece_promotion_move[1:]:
            if potential_return_item[0] > max_val:
                return_item = potential_return_item
                max_val = potential_return_item[0]
        return_item[0] = -return_item[0]
            
        return return_item

def proper_syntax(piece, promotion_piece, next_square):
    if (next_square == "0-0-0" or next_square == "0-0"):
        if (piece[0] == "k"):
            return 1

    check_list_piece = ["r", "b", "n", "p", "k", "q"]
    check_list_str = ["a", "b", "c", "d", "e", "f", "g", "h"]
    check_list_num = ["1","2","3","4","5","6","7","8"]
    check_list_promotion_piece = ["q", "r", "b", "n"]

    if (len(piece) != 3) or (len(next_square) != 2):
        return 0
    elif not (piece[0] in check_list_piece):
        return 0
    elif not (piece[1] in check_list_str):
        return 0
    elif not (piece[2] in check_list_num):
        return 0
    elif not (next_square[0] in check_list_str):
        return 0
    elif not (next_square[1] in check_list_num):
        return 0
    
    next_square_num = int(piece_to_logic(next_square, 0))

    #make sure pawn going to final rank is promoting
    if piece[0] == "p" and ( ((next_square_num%10) == 8) or ((next_square_num%10) == 1) ):
        if promotion_piece == "none":
            return 0
        
    #make sure promotion piece is valid and only works for pawn goingto final square
    if promotion_piece != "none":
        if not (promotion_piece in check_list_promotion_piece):
            return 0
        elif piece[0] != "p":
            return 0
        elif not (((next_square_num%10) == 8) or ((next_square_num%10) == 1)):
            return 0
        
    return 1

def user_move(set, side, move_made):
    promotion_piece = "none"
    move = move_made
    move_parts = move.split()
    if len(move_parts) == 3:
        piece, next_square, promotion_piece = move.split()
        if (promotion_piece != "none") and proper_syntax(piece, promotion_piece, next_square):
            if not move_valid(set, piece, next_square, side, 0):
                return "invalid move"
        else:
            return "improper syntax"
    elif len(move_parts) == 2:
        piece, next_square = move.split()
        if(proper_syntax(piece, promotion_piece, next_square)):
            if not move_valid(set, piece, next_square, side, 0):
                return "invalid move"
        else:
            return "improper syntax"
        
    elif len(move_parts) == 1:
        for king_check in set[side]:
            if king_check [0] == "k":
                king_piece = "k" + king_check[1:]

        piece = king_piece
        next_square = move_parts[0]
        if(proper_syntax(piece, promotion_piece, next_square)):
            if not move_valid(set, piece, next_square, side, 0):
                return "invalid move"
        else:
            return "improper syntax"
    else:
        return "invalid number"

    set = make_move(set, side, piece, promotion_piece, next_square)

    return set

white_pieces = ["ra1", "nb1", "bc1", "qd1", "ke1", "bf1", "ng1", "rh1", "pa2", "pb2", "pc2", "pd2", "pe2", "pf2", "pg2", "ph2"]
black_pieces = ["ra8", "nb8", "bc8", "qd8", "ke8", "bf8", "ng8", "rh8", "pa7", "pb7", "pc7", "pd7", "pe7", "pf7", "pg7", "ph7"]
castle_rights_white = [1,1]
castle_rights_black = [1,1]
white_pieces_en_passant = "none"
black_pieces_en_passant = "none"
set = [white_pieces, black_pieces, castle_rights_white, castle_rights_black, 
        white_pieces_en_passant, black_pieces_en_passant]
end = [0,0]
user_side = None
computer_side = None
difficulty = None

@app.route('/reset_game', methods = ["POST"])
def reset_game():
    global white_pieces
    global black_pieces
    global castle_rights_white
    global castle_rights_black
    global white_pieces_en_passant
    global black_pieces_en_passant
    global set
    global end
    #global user_side
    #global computer_side
    white_pieces = ["ra1", "nb1", "bc1", "qd1", "ke1", "bf1", "ng1", "rh1", "pa2", "pb2", "pc2", "pd2", "pe2", "pf2", "pg2", "ph2"]
    black_pieces = ["ra8", "nb8", "bc8", "qd8", "ke8", "bf8", "ng8", "rh8", "pa7", "pb7", "pc7", "pd7", "pe7", "pf7", "pg7", "ph7"]
    castle_rights_white = [1,1]
    castle_rights_black = [1,1]
    white_pieces_en_passant = "none"
    black_pieces_en_passant = "none"
    set = [white_pieces, black_pieces, castle_rights_white, castle_rights_black, 
            white_pieces_en_passant, black_pieces_en_passant]
    end = [0,0]
    #user_side = None
    #computer_side = None

    #take out maybe:
    return jsonify({'message': 'game reset'})

@app.route('/choose_side', methods=['POST'])
def choose_side():
    global user_side
    global computer_side
    data = request.get_json()
    side = data.get('side')
    if side == "white":
        user_side = 0
    else:
        user_side = 1
    computer_side = not user_side
    
    return jsonify({'message': 'side selected'})

@app.route('/choose_difficulty', methods=['POST'])
def choose_difficulty():
    global difficulty
    data = request.get_json()
    difficulty_string = data.get('difficulty')
    if difficulty_string == "easy":
        difficulty = 1
    elif difficulty_string == "medium":
        difficulty = 2
    else:
        difficulty = 3

    return jsonify({'message': 'difficulty selected'})

@app.route('/move_computer', methods=['GET'])
def make_computer_move():
    global end
    global set
    global computer_side
    computer_move_list = computer_move(set,computer_side,difficulty)
    set = make_move(set, computer_side, computer_move_list[1], computer_move_list[2], computer_move_list[3])
    end = checkmate_or_stalemate(set, computer_side)
    response = {'white_pieces': set[0], 'black_pieces': set[1], 'end': end}

    return jsonify(response), 200

@app.route('/move_user', methods=['GET'])
def make_user_move():
    global end
    global set
    global user_side
    user_input = request.args.get('position')
    set_or_error = user_move(set, user_side, user_input)

    if isinstance (set_or_error, str):
        response = {'error': set_or_error, 'white_pieces': set[0], 'black_pieces': set[1], 'end': end}
    else:
        set = set_or_error
        end = checkmate_or_stalemate(set, user_side)
        response = {'error': "none", 'white_pieces': set[0], 'black_pieces': set[1], 'end': end}

    return jsonify(response), 200

@app.route('/')
def index():
    return render_template("front_end.html")

if __name__ == "__main__":
    app.run(debug=True)