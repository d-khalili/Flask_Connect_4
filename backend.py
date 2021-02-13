import random
import app

class Board():
    def __init__(self):
        self.move_list = []
        self.player_1_set = set()
        self.player_2_set = set()
        self.turn_count = 0
        self.win_conditions = self.create_win_conditions()

    def create_win_conditions(self):
        win_condition_list = []
        # A = Horizontal, B = Vertical, C = Diagonal Right, D = Diagonal Left
        win_possibilities = ["A", "B", "C", "D"]
        # Wincomb_dict Structure = [[starting moves], [add number, how many iterations on current row], [add number to get to next row, how many rows to try]]
        wincomb_dict = {'A': [[1,2,3,4], [1,4], [7,6]], 'B': [[1,8,15,22],[7,3],[1,7]], 'C': [[1,9,17,25],[1,4],[7,3]], 'D': [[4,10,16,22],[1,4],[7,3]]}
        for wp in win_possibilities:
            y = 0
            for j in range(wincomb_dict[wp][2][1]):
                x = 0
                for i in range(wincomb_dict[wp][1][1]):
                    win_set = set()
                    for k in range(4):
                        win_set.add(wincomb_dict[wp][0][k]+x+y)
                    win_condition_list.append(win_set)
                    x = x + wincomb_dict[wp][1][0]
                y = y + wincomb_dict[wp][2][0]
        return win_condition_list

    def board_move(self, move, player_ID):
        # Checks to make sure move hasn't been won yet and then goes larger
        print("MOVE: " + str(move))
        while move in self.move_list:
            move += 7
            if move > 42:
                return 0

        while move - 7 not in self.move_list and move > 7:
            move -= 7

        if player_ID == 1:
            self.player_1_set.add(int(move))
        if player_ID == 2:
            self.player_2_set.add(int(move))

        self.move_list.append(int(move))
        self.turn_count += 1

        print('Turn count: ' + str(self.turn_count))
        print('Move list: ' + str(self.move_list))
        print('Player 1 Set: ' + str(self.player_1_set))
        print('Player 2 Set: ' + str(self.player_2_set))
        print('')

    def check_win(self, player_ID):
        if player_ID == 1:
            c_player_set = self.player_1_set
        if player_ID == 2:
            c_player_set = self.player_2_set

        # Check Win
        for set in self.win_conditions:
            if all(item in c_player_set for item in set):
                return 1, set
        # Check Draw
        if self.turn_count > 41:
            return 3, {}
        # Continue otherwise
        else:
            return 0, {}

class Player():
    def __init__(self, player_type, player_ID):
        self.player_type = player_type
        self.player_ID = player_ID

    def make_move(self):
        if self.player_type == 'Random':
            user_move = int(random.randint(1,7))
            return user_move

        if self.player_type == 'Command_line':
            user_move = int(input("Human Move: "))
            return user_move

        if self.player_type == 'Web':
            web_move = app.request.form.get("number")
            if web_move is None:
                web_move = 5
            try:
                int(web_move)
            except:
                web_move = 5

            return int(web_move)

class Game():
    def __init__(self):
        self.B = Board()
        self.P1 = Player('Web', 1)
        self.P2 = Player('Random', 2)

    def play_game(self):
        user_move = self.P1.make_move()
        while self.B.board_move(user_move, self.P1.player_ID) == 0:
            user_move = self.P1.make_move()

        if self.B.check_win(self.P1.player_ID)[0] != 0:
            print("Recording a PLAYER-1 win in play_game")
            return self.B.check_win(self.P1.player_ID)

        user_move = self.P2.make_move()
        while self.B.board_move(user_move, self.P2.player_ID) == 0:
            user_move = self.P2.make_move()

        if self.B.check_win(self.P2.player_ID)[0] != 0:
            print("Recording a PLAYER-2 win in play_game")
            return self.B.check_win(self.P2.player_ID)

    def reset(self):
        self.B.player_1_set = set()
        self.B.player_2_set = set()
        self.B.move_list = []
        self.B.turn_count = 0