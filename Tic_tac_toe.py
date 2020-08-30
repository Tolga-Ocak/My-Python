import copy
import random
import itertools
import time
from selenium import webdriver


class Board:

    array = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]

    turn = 0

    def xox(self, loc_xo):

        i, j = loc_xo
        value = "X" if self.turn % 2 == 0 else "O"
        if self.array[i][j] == " ":
            self.array[i][j] = value
            self.turn += 1
            return True
        else:
            print("\nERROR: Enter Empty Place.")
            return False

    def check(self):

        for i in range(3):
            first_cond = self.array[i][0] == self.array[i][1] == self.array[i][2] != " "
            second_cond = self.array[0][i] == self.array[1][i] == self.array[2][i] != " "
            if first_cond or second_cond:
                return True
        third_cond = self.array[0][0] == self.array[1][1] == self.array[2][2] != " "
        fourth_cond = self.array[0][2] == self.array[1][1] == self.array[2][0] != " "

        if third_cond or fourth_cond:
            return True
        else:
            return False

    def reset(self):
        self.turn = 0
        self.array = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]


class AI(Board):

    array = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]

    Conditions_opponent = {
        "Strategy Error": 4,
        "Strategy Win": 3,
        "User Error": 2,
        "No Win": 1,
    }
    Condition_AI = {
        "Strategy Win": 4,
        "User Error": 3,
        "No Win": 2,
        "Strategy Error": 1,
    }
    paths = {}
    data_X = {}
    data_O = {}

    data_turn = 1
    AI = 0

    saved_paths = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    saved_key = []
    next_paths = []

    def __init__(self):
        for letter in ("X", "O"):
            if self.check_database(letter):
                print("""
                -----------------------------------------------------------------------------------
                Warning
                
                * It is beta test for Tic Tac Toe game.
                * If you don't have the databases, you have to wait game to create new ones.
                * It will take 9 or 10 minutes.
                * Until finish to create new databases, please DO NOT CLOSE WINDOW.
                * And DO NOT TOUCH DATABASE (dataset_X, dataset_O).
                
                Rules
                
                * X is first player, O is second player.
                * The AI is built not to lose. If The AI lose, PLEASE REPORT ADMIN.
                * To play Tic Tac Toe, you must enter number of the squares. 
                -----------------------------------------------------------------------------------
                """)
                self.create_database()
                if self.AI == 0:
                    self.data_X = copy.deepcopy(self.paths)
                elif self.AI == 1:
                    self.data_O = copy.deepcopy(self.paths)
            self.AI += 1

    def choose_player(self, player):
        if player == "X":
            self.AI = 1
        elif player == "O":
            self.AI = 0

    def check_database(self, letter):
        if letter == "X":
            try:
                with open("dataset_X.txt", "r", encoding="UTF-8") as file:
                    n = 0
                    while True:
                        text_line = file.readline().split("\t\t")
                        if text_line == [""]:
                            break
                        text_line[0], text_line[1] = text_line[0].rstrip(), text_line[1].rstrip()
                        text_line[2] = text_line[2][:-1]
                        if n != 0:
                            self.data_X[text_line[0]] = [text_line[1], text_line[2]]
                        n += 1
            except FileNotFoundError:
                return True
        if letter == "O":
            try:
                with open("dataset_O.txt", "r", encoding="UTF-8") as file:
                    n = 0
                    while True:
                        text_line = file.readline().split("\t\t")
                        if text_line == [""]:
                            break
                        text_line[0], text_line[1] = text_line[0].rstrip(), text_line[1].rstrip()
                        text_line[2] = text_line[2][:-1]
                        if n != 0:
                            self.data_O[text_line[0]] = [text_line[1], text_line[2]]
                        n += 1
            except FileNotFoundError:
                return True

    def create_database(self):
        self.paths = {
            "0": ["No Condition", 0],
            "1": ["No Condition", 0],
            "2": ["No Condition", 0],
            "3": ["No Condition", 0],
            "4": ["No Condition", 0],
            "5": ["No Condition", 0],
            "6": ["No Condition", 0],
            "7": ["No Condition", 0],
            "8": ["No Condition", 0],
        }
        if self.AI == 0:
            while self.data_turn < 9:
                self.determine_path()
                self.data_turn += 1
            self.define_condition()
            with open("dataset_X.txt", "w", encoding="UTF-8") as file:
                file.write("{:10}\t\t{:16}\t\t{}\n".format("Path", "Condition", "Turn"))
                for i in self.paths:
                    file.write("{:10}\t\t{:16}\t\t{}\n".format(i, self.paths[i][0], self.paths[i][1]))
                file.close()
            self.data_turn = 1
        else:
            while self.data_turn < 9:
                self.determine_path()
                self.data_turn += 1
            self.define_condition()
            with open("dataset_O.txt", "w", encoding="UTF-8") as file:
                file.write("{:10}\t\t{:16}\t\t{}\n".format("Path", "Condition", "Turn"))
                for i in self.paths:
                    file.write("{:10}\t\t{:16}\t\t{}\n".format(i, self.paths[i][0], self.paths[i][1]))
                file.close()
            self.data_turn = 1
        self.saved_paths = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]

    def determine_path(self):
        for path in self.saved_paths:
            for digit in range(0, 9):
                if not (str(digit) in path):
                    new_key = path + str(digit)
                    self.saved_key.append(new_key)
            self.control()
            self.saved_key = []
        self.saved_paths = self.next_paths.copy()
        self.next_paths = []

    def control(self):
        win = []
        lose = []
        for key in self.saved_key:

            for letter in key[:-1]:
                lin = int(letter) // 3
                col = int(letter) % 3
                self.xox((lin, col))

            if self.data_turn % 2 == self.AI:
                lin = int(key[-1]) // 3
                col = int(key[-1]) % 3
                self.turn += 1
                self.xox((lin, col))
                if self.check():
                    lose.append(key)

            if self.data_turn % 2 != self.AI:
                lin = int(key[-1]) // 3
                col = int(key[-1]) % 3
                self.turn += 1
                self.xox((lin, col))
                if self.check():
                    win.append(key)
            self.reset()

        if len(lose) == 1:
            self.paths[lose[0]] = ["No Condition", self.data_turn]
            self.next_paths.append(lose[0])
        elif len(lose) > 1:
            for key in self.saved_key:
                self.paths[key] = ["Strategy Error", self.data_turn]
        elif len(win) == 1:
            self.next_paths.append(win[0])
            self.paths[win[0]] = ["No Condition", self.data_turn]
            self.saved_key.remove(win[0])
            for key in self.saved_key:
                self.paths[key] = ["User Error", self.data_turn]
        elif len(win) > 1:
            for key in self.saved_key:
                self.paths[key] = ["Strategy Win", self.data_turn]
        else:
            for key in self.saved_key:
                self.paths[key] = ["No Condition", self.data_turn]
                self.next_paths.append(key)

    def define_condition(self):
        new_paths = {}
        for data in self.paths:

            if self.paths[data] == ["No Condition", 8]:
                new_paths[data] = ["No Win", 8]

            if self.paths[data][0] == "Strategy Win":
                for letter in data:
                    lin = int(letter) // 3
                    col = int(letter) % 3
                    self.xox((lin, col))
                saved_array = copy.deepcopy(self.array)
                for digit in range(0, 9):
                    self.array = copy.deepcopy(saved_array)
                    if not (str(digit) in data):
                        lin = digit // 3
                        col = digit % 3
                        self.xox((lin, col))
                        if self.check():
                            new_paths[data + str(digit)] = ["Strategy Win", self.turn-1]
                        self.turn -= 1
                self.reset()

            if self.paths[data][0] == "User Error":
                for letter in data:
                    lin = int(letter) // 3
                    col = int(letter) % 3
                    self.xox((lin, col))
                saved_array = copy.deepcopy(self.array)
                for digit in range(0, 9):
                    self.array = copy.deepcopy(saved_array)
                    if not (str(digit) in data):
                        lin = digit // 3
                        col = digit % 3
                        self.xox((lin, col))
                        if self.check():
                            new_paths[data + str(digit)] = ["User Error", self.turn-1]
                            break
                        self.turn -= 1
                self.reset()

        self.paths = {**self.paths, **new_paths}

        for number in range(7, -1, -1):
            for data in self.paths:
                search = []
                conditions = []
                if self.paths[data] == ["No Condition", number]:
                    for digit in range(0, 9):
                        if not (str(digit) in data):
                            search.append(data+str(digit))
                    for result in self.paths:
                        if result in search:
                            conditions.append(self.paths[result])

                    highest = 0
                    types = ""
                    for condition in conditions:
                        if condition[1] % 2 == self.AI:
                            if highest < self.Condition_AI[condition[0]]:
                                highest = self.Condition_AI[condition[0]]
                                types = condition[0]
                        else:
                            if highest < self.Conditions_opponent[condition[0]]:
                                highest = self.Conditions_opponent[condition[0]]
                                types = condition[0]
                    self.paths[data][0] = types

    def play(self, order_):
        chosen_paths_ = []
        possible_paths = []
        data_type = copy.deepcopy(self.data_X) if self.AI == 0 else copy.deepcopy(self.data_O)
        for number in range(0, 9):
            chosen_path = order_ + str(number)
            chosen_paths_.append(chosen_path)
        condition_number = 0
        for data in data_type:
            if data in chosen_paths_:
                if condition_number < self.Condition_AI[data_type[data][0]]:
                    condition_number = self.Condition_AI[data_type[data][0]]
                    possible_paths.clear()
                    possible_paths.append(data)
                elif condition_number == self.Condition_AI[data_type[data][0]]:
                    possible_paths.append(data)
        if len(possible_paths) == 1:
            return possible_paths[0]
        elif len(possible_paths) > 1:
            benefit = 0
            benefit_numb = []
            for possible_path in possible_paths:
                chosen_paths_.clear()
                for number in range(0, 9):
                    chosen_path = possible_path + str(number)
                    chosen_paths_.append(chosen_path)
                condition_number = 0
                for data in data_type:
                    if data in chosen_paths_:
                        if condition_number < self.Condition_AI[data_type[data][0]]:
                            condition_number = self.Condition_AI[data_type[data][0]]
                            benefit = 1
                        elif condition_number == self.Condition_AI[data_type[data][0]]:
                            benefit += 1
                benefit_numb.append(benefit)
            if benefit_numb.count(max(benefit_numb)) == 1:
                return possible_paths[benefit_numb.index(max(benefit_numb))]
            elif benefit_numb.count(max(benefit_numb)) > 1:
                index = []
                for i in range(benefit_numb.count(max(benefit_numb))):
                    max_index = benefit_numb.index(max(benefit_numb))
                    benefit_numb[max_index] = 0
                    index.append(max_index)
                return possible_paths[random.choice(index)]


class Google:

    Google_board = [["", "", ""], ["", "", ""], ["", "", ""]]

    order = ""

    turn = 0

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:/Users/Lenovo/Desktop/XOX/chromedriver.exe')
        url = "https://www.google.com/search?ei=rSFIX_SBM4iJrwTZmoegDg&q=tic+tac+toe+&oq=tic+tac+toe+&gs_lcp" \
              "=CgZwc3ktYWIQAzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoGCAAQFhAeUIoFWI4MYIYQ" \
              "aABwAHgAgAGoAYgBmgeSAQMwLjaYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwi0jJufprzrAhWI" \
              "xIsKHVnNAeQQ4dUDCA0&uact=5 "
        self.browser.get(url)
        click = '//*[@id="rso"]/div[1]/div[1]/div/div[1]/div/div/div/div[2]'
        play = self.browser.find_element_by_xpath(click)
        play.click()
        time.sleep(1.5)

    def impossible(self):
        xpath = '//*[@id="rso"]/div[1]/div[1]/div/div[1]/div/div/div/div[1]/g-dropdown-menu'
        options = self.browser.find_element_by_xpath(xpath)
        options.click()
        time.sleep(1)
        xpath = '//*[@id="lb"]/div/g-menu/g-menu-item[3]/div'
        impossible = self.browser.find_element_by_xpath(xpath)
        impossible.click()
        time.sleep(1)

    def search(self):
        time.sleep(1)
        for i, j in itertools.product([1, 2, 3], [1, 2, 3]):
            xpath = '//*[@id="rso"]/div[1]/div[1]/div/div[1]/div/div/div/div[2]/table/tbody/tr[{}]/td[{}]'.format(i, j)
            element = self.browser.find_element_by_xpath(xpath)
            html = element.get_attribute('outerHTML')
            tag_open = html.find("<svg")
            tag_close = html.find("</svg>")
            svg_1 = html[tag_open:(tag_close + 6)]
            html = html[0:tag_open] + html[(tag_close + 6):-1]
            tag_open = html.find("<svg")
            tag_close = html.find("</svg>")
            svg_2 = html[tag_open:(tag_close + 6)]
            count_1 = 'display: none; visibility: visible;"'
            count_2 = 'visibility: visible; display: none;"'
            if not ((svg_1.count(count_1) or svg_1.count(count_2)) and (svg_2.count(count_1) or svg_2.count(count_2))):
                if self.Google_board[i-1][j-1] == "":
                    self.Google_board[i-1][j-1] = "X" if self.turn % 2 == 0 else "O"
                    self.order += str(3*(i-1)+(j-1))
                    self.turn += 1
                    return self.order

    def playing(self, add):
        add = int(add) - 1
        self.order += str(add)
        i = add // 3
        j = add % 3
        click = '//*[@id="rso"]/div[1]/div[1]/div/div[1]/div/div/div/div[2]/table/tbody/tr[{}]/td[{}]'.format(i+1, j+1)
        play = self.browser.find_element_by_xpath(click)
        play.click()
        self.Google_board[i][j] = "X" if self.turn % 2 == 0 else "O"
        self.turn += 1

    def reset(self):
        time.sleep(2)
        self.order = ""
        self.Google_board = [["", "", ""], ["", "", ""], ["", "", ""]]
        click = '//*[@id="rso"]/div[1]/div[1]/div/div[1]/div/div/div/g-raised-button'
        reset = self.browser.find_element_by_xpath(click)
        reset.click()
        time.sleep(1.5)

    def close(self):
        self.browser.close()
        print("Initiating system shutdown...")


print("""
---------------------------
     Tic Tac Toe Game
---------------------------
""")

system_choose = input("Will you use selenium system(yes/no): ")

if system_choose.upper() == "NO":

    system = True
    board = Board()
    opponent = AI()

    while system:

        answer = input("\nAre you ready to game?(yes/any key): ")

        if answer.lower() == "yes":
            print("\nInitiating game...")
            choose = input("\nChoose player.(O/X):")
            if choose.upper() == "X" or choose.upper() == "O":
                opponent.choose_player(choose.upper())
            else:
                print("\nFalse command.\n\nInitiating system shutdown...")
                system = False
                time.sleep(1)
        else:
            print("\nInitiating system shutdown...")
            system = False
            time.sleep(1)

        order = ""
        finish = False
        while system:

            print("\n", board.array[0], "\n", board.array[1], "\n", board.array[2], "\n")
            if board.turn % 2 != opponent.AI:
                numb = int(input("Choose square: "))
                numb -= 1
                line = numb // 3
                column = numb % 3
                error_user = board.xox((line, column))
                if error_user:
                    order = order + str(numb)
                    finish = board.check()
            else:
                order = opponent.play(order)
                numb = order[-1]
                numb = int(numb)
                print("Choose square: {}".format(numb+1))
                line = numb // 3
                column = numb % 3
                board.xox((line, column))
                finish = board.check()

            if finish or board.turn == 9:
                print("\n", board.array[0], "\n", board.array[1], "\n", board.array[2], "\n")
                print("Game Is Over.\n")
                board.reset()
                break

elif system_choose.upper() == "YES":

    system = True
    board = Board()
    opponent = AI()
    google_AI = Google()
    google_AI.impossible()

    while system:

        order = ""
        finish = False
        opponent.choose_player("O")

        while system:

            print("\n", board.array[0], "\n", board.array[1], "\n", board.array[2], "\n")
            if board.turn % 2 != opponent.AI:
                order = google_AI.search()
                numb = order[-1]
                numb = int(numb)
                print("Choose square: {}".format(numb + 1))
                line = numb // 3
                column = numb % 3
                board.xox((line, column))
                finish = board.check()

            else:
                order = opponent.play(order)
                numb = order[-1]
                numb = int(numb)
                print("Choose square: {}".format(numb + 1))
                line = numb // 3
                column = numb % 3
                google_AI.playing(numb+1)
                board.xox((line, column))
                finish = board.check()

            if finish or board.turn == 9:
                print("\n", board.array[0], "\n", board.array[1], "\n", board.array[2], "\n")
                print("Game Is Over.\n")
                board.reset()
                google_AI.reset()
                break
