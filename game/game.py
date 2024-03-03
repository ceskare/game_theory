from collections import Counter


class Game(object):
    def __init__(self):
        self.matches = None
        self.registry = Counter()

    def play(self, _player1, _player2, matches=10):
        self.matches = matches
        role1 = _player1.get_role()
        role2 = _player2.get_role()
        for action_number in range(1, self.matches + 1):
            if role1 or role2 in ["detective", "copycat"]:
                if role1 == "detective":
                    _player1.get_action(action_number)
                else:
                    _player2.get_action(action_number)

            action1 = _player1.act(_player2.get_action(action_number))
            action2 = _player2.act(_player1.get_action(action_number))

            if action1 == 'cooperate' and action2 == 'cooperate':
                self.registry[role1] += 2
                self.registry[role2] += 2
            elif action1 == 'cheat' and action2 == 'cooperate':
                self.registry[role1] += 3
                self.registry[role2] -= 1
            elif action1 == 'cooperate' and action2 == 'cheat':
                self.registry[role1] -= 1
                self.registry[role2] += 3
            elif action1 == 'cheat' and action2 == 'cheat':
                pass

    def top3(self):
        sorted_registry = sorted(self.registry.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_registry[:3]:
            print(name, score)


class Player:
    def __init__(self):
        self.action = None
        self.last_action = None
        self.has_cheated = False

    def get_action(self, action_number):
        return self.action

    def act(self, opponent_action):
        return self.action


class Cheater(Player):
    def __init__(self):
        super().__init__()
        self.action = "cheat"

    @staticmethod
    def get_role():
        return "cheater"


class Cooperator(Player):
    def __init__(self):
        super().__init__()
        self.action = "cooperate"

    @staticmethod
    def get_role():
        return "cooperator"


class Copycat(Player):
    @staticmethod
    def get_role():
        return "copycat"

    def __init__(self):
        super().__init__()
        self.current_action = "cooperate"

    def act(self, opponent_action):
        self.current_action = "cooperate"
        if self.last_action == "cheat":
            self.current_action = "cheat"
        self.last_action = opponent_action
        return self.current_action

    def get_action(self, action_number):
        return self.last_action


class Grudger(Player):
    def __init__(self):
        super().__init__()
        self.action = "cooperate"

    @staticmethod
    def get_role():
        return "grudger"

    def act(self, opponent_action):
        if self.has_cheated:
            self.action = "cheat"
        if opponent_action == "cheat":
            self.has_cheated = True
        return self.action


class Detective(Player):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.action = "cooperate"
        self.last_action = "cooperate"

    @staticmethod
    def get_role():
        return "detective"

    def act(self, opponent_action):

        if self.counter <= 4:
            if opponent_action == "cheat":
                self.has_cheated = True
            if self.counter != 2:
                self.action = "cooperate"
            self.last_action = opponent_action
        else:
            if not self.has_cheated:
                self.action = "cheat"
            else:
                self.action = "cooperate"
                if self.last_action == 'cheat':
                    self.action = "cheat"
                self.last_action = opponent_action
        return self.action

    def get_action(self, action_number):
        self.counter = action_number
        if self.counter == 2:
            self.action = "cheat"
        if self.counter == 3:
            self.action = "cooperate"
        return self.action


game = Game()
player_types = [Grudger, Cheater, Copycat, Detective, Cooperator]

for i in range(len(player_types)):
    for j in range(i + 1, len(player_types)):
        player1 = player_types[i]()
        player2 = player_types[j]()
        game.play(player1, player2, 10)

game.top3()
