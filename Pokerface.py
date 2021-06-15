import copy
import itertools


class UI:

    def __init__(self):
        pass


class Interpretation:

    table_cards = []
    hand_cards = []

    hand_rankings = {10: "Royal Flush",
                     9: "Straight Flush",
                     8: "Four of a Kind",
                     7: "Full House",
                     6: "Flush",
                     5: "Straight",
                     4: "Three of a Kind",
                     3: "Two Pair",
                     2: "Pair",
                     1: "High Card"}

    possible_combinations = {}
    combination_ranking = {}

    predictions_ai = {}
    predictions_opp = {}
    ratio = {}

    AI = []
    opponent = []

    def interpreting_card(self, table_cards, hand_cards, player):

        self.table_cards = table_cards
        self.hand_cards = hand_cards

        for card in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
            card = list(card)
            if (self.table_cards.count(card) + self.hand_cards.count(card)) > 1:
                raise ValueError("Repeated card is detected.")

        for card in self.table_cards:
            if (card[0] <= 1) or (card[0] >= 15) or (not card[1] in ["diamonds", "hearts", "spades", "clubs"]):
                raise ValueError("There is no {} {} in deck.".format(card[0], card[1]))

        for card in self.hand_cards:
            if (card[0] <= 1) or (card[0] >= 15) or (not card[1] in ["diamonds", "hearts", "spades", "clubs"]):
                raise ValueError("There is no {} {} in deck.".format(card[0], card[1]))

        if (len(self.table_cards) < 3) or (len(self.table_cards) > 5) or (len(self.hand_cards) != 2):
            raise ValueError("the number of arguments is incorrect")

        all_cards = self.table_cards + self.hand_cards
        self.combinations(all_cards)
        self.ranking()
        if player == "AI":
            self.AI = self.high_rank()
        elif player == "opponent":
            self.opponent = self.high_rank()

    def interpreting_possibility(self):

        self.predictions_ai.clear()
        self.predictions_opp.clear()
        combination_ai = []
        possible_table = self.table_possibilities()
        for possible_card in possible_table:
            all_cards = possible_card + self.hand_cards
            self.combinations(all_cards)
            self.ranking()
            result = self.high_rank()
            combination_ai.append(result)
            if not self.hand_rankings[result[5][0]] in self.predictions_ai.keys():
                self.predictions_ai[self.hand_rankings[result[5][0]]] = (1 / len(possible_table)) * 100
            else:
                self.predictions_ai[self.hand_rankings[result[5][0]]] += (1 / len(possible_table)) * 100

        combination_opp = []
        possible_all_card = self.hand_possibilities()
        for possible_card in possible_all_card:
            self.combinations(possible_card)
            self.ranking()
            result = self.high_rank()
            combination_opp.append(result)
            if not self.hand_rankings[result[5][0]] in self.predictions_opp.keys():
                self.predictions_opp[self.hand_rankings[result[5][0]]] = (1 / len(possible_all_card)) * 100
            else:
                self.predictions_opp[self.hand_rankings[result[5][0]]] += (1 / len(possible_all_card)) * 100

        self.ratio = self.win_lose_ratio(combination_opp)

    def combinations(self, all_cards):

        n = 0

        if len(self.possible_combinations) != 0:
            self.possible_combinations.clear()

        if len(all_cards) == 5:
            self.possible_combinations["combination_1"] = all_cards

        elif len(all_cards) == 6:
            for card in all_cards:
                n += 1
                combination = all_cards.copy()
                combination.remove(card)
                self.possible_combinations["combination_{}".format(n)] = combination

        else:
            chosen_cards = all_cards.copy()
            for card_1 in all_cards:
                combination_1 = all_cards.copy()
                combination_1.remove(card_1)
                chosen_cards.remove(card_1)
                for card_2 in chosen_cards:
                    n += 1
                    combination_2 = combination_1.copy()
                    combination_2.remove(card_2)
                    self.possible_combinations["combination_{}".format(n)] = combination_2

    def ranking(self):

        if len(self.combination_ranking) != 0:
            self.combination_ranking.clear()

        n = 0
        for cards in list(self.possible_combinations.values()):

            n += 1
            key = "combination_{}".format(n)
            numbers = [cards[0][0], cards[1][0], cards[2][0], cards[3][0], cards[4][0]]
            numbers.sort()
            number_card = {}

            for number in range(2, 15):
                if numbers.count(number) != 0:
                    number_card[number] = numbers.count(number)

            if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
                if numbers == [10, 11, 12, 13, 14]:
                    self.combination_ranking[key] = [10, 14]

                elif (numbers[0] + 4) == (numbers[1] + 3) == (numbers[2] + 2) == (numbers[3] + 1) == numbers[4]:
                    self.combination_ranking[key] = [9, max(numbers)]

                else:
                    self.combination_ranking[key] = [6, max(numbers)]

            else:
                if 4 in number_card.values():
                    index_1 = list(number_card.keys())[list(number_card.values()).index(4)]
                    index_2 = list(number_card.keys())[list(number_card.values()).index(1)]
                    self.combination_ranking[key] = [8, index_1, index_2]

                elif (2 in number_card.values()) and (3 in number_card.values()):
                    index_1 = list(number_card.keys())[list(number_card.values()).index(3)]
                    index_2 = list(number_card.keys())[list(number_card.values()).index(2)]
                    self.combination_ranking[key] = [7, index_1, index_2]

                elif (numbers[0] + 4) == (numbers[1] + 3) == (numbers[2] + 2) == (numbers[3] + 1) == numbers[4]:
                    self.combination_ranking[key] = [5, max(numbers)]

                elif 3 in number_card.values():
                    index_1 = list(number_card.keys())[list(number_card.values()).index(3)]
                    number_card.pop(index_1)
                    index_2 = list(number_card.keys())[list(number_card.values()).index(1)]
                    number_card.pop(index_2)
                    index_3 = list(number_card.keys())[list(number_card.values()).index(1)]
                    self.combination_ranking[key] = [4, index_1, max([index_2, index_3]), min([index_2, index_3])]

                elif list(number_card.values()).count(2) == 2:
                    index_1 = list(number_card.keys())[list(number_card.values()).index(2)]
                    number_card.pop(index_1)
                    index_2 = list(number_card.keys())[list(number_card.values()).index(2)]
                    number_card.pop(index_2)
                    index_3 = list(number_card.keys())[list(number_card.values()).index(1)]
                    self.combination_ranking[key] = [3, max([index_1, index_2]), min([index_1, index_2]), index_3]

                elif 2 in number_card.values():
                    index_1 = list(number_card.keys())[list(number_card.values()).index(2)]
                    number_card.pop(index_1)
                    index_2 = max(list(number_card.keys()))
                    number_card.pop(index_2)
                    index_3 = max(list(number_card.keys()))
                    number_card.pop(index_3)
                    index_4 = list(number_card.keys())[0]
                    self.combination_ranking[key] = [2, index_1, index_2, index_3, index_4]

                else:
                    self.combination_ranking[key] = [1, numbers[4], numbers[3], numbers[2], numbers[1], numbers[0]]

    def high_rank(self):

        index_ = list(self.combination_ranking.values()).index(max(self.combination_ranking.values()))
        best_combination = copy.deepcopy(self.possible_combinations["combination_{}".format(index_ + 1)])
        best_combination.append(max(self.combination_ranking.values()))

        return best_combination

    def table_possibilities(self):

        possibilities = []
        if len(self.table_cards) == 4:
            for cards in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
                temporal_ = copy.deepcopy(self.table_cards)
                cards = list(cards)
                if (not (cards in temporal_)) and (not (cards in self.hand_cards)):
                    temporal_.append(cards)
                    possibilities.append(temporal_)

        elif len(self.table_cards) == 3:
            used_ones = []
            for cards_01 in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
                temporal_ = copy.deepcopy(self.table_cards)
                cards_01 = list(cards_01)
                if (not (cards_01 in temporal_)) and (not (cards_01 in self.hand_cards)):
                    temporal_.append(cards_01)
                    used_ones.append(cards_01)

                    for cards_02 in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
                        temporal_1 = copy.deepcopy(temporal_)
                        cards_02 = list(cards_02)
                        if (not (cards_02 in temporal_1)) and (not (cards_02 in used_ones)) and \
                                (not (cards_02 in self.hand_cards)):
                            temporal_1.append(cards_02)
                            possibilities.append(temporal_1)

        return possibilities

    def hand_possibilities(self):

        possibilities = []
        used_hand = []
        for cards_01 in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
            for cards_02 in itertools.product(range(2, 15), ["diamonds", "hearts", "spades", "clubs"]):
                cards_01, cards_02 = list(cards_01), list(cards_02)
                if (cards_01 != cards_02) and (not ([cards_01, cards_02] in used_hand)):
                    used_hand.append([cards_01, cards_02])
                    used_hand.append([cards_02, cards_01])
                    if (not (cards_01 in self.table_cards)) and (not (cards_02 in self.table_cards)) and (
                            not (cards_01 in self.hand_cards)) and (not (cards_02 in self.hand_cards)):
                        possibilities.append(self.table_cards + [cards_01] + [cards_02])

        return possibilities

    def win_lose_ratio(self, combination_opp):

        win = 0
        total = 0
        for card_combination in combination_opp:
            if self.AI[5] == max(self.AI[5], card_combination[5]):
                win += 1
            total += 1
        ratio = {"Win:": (win/total)*100, "Lose": (1-(win/total))*100}

        return ratio


if __name__ == "__main__":
    UI = UI()
    Interpretation = Interpretation()

    print("""
    d- diamonds
    h- hearts
    c- clubs
    s- spades
     
    for table
    """)

    while True:

        try:
            cards_1 = []
            for i in range(3):
                x = int(input("Enter number for {}:".format(i + 1)))
                y = (input("Enter card for {}:".format(i + 1)))
                if y == "d":
                    y = "diamonds"
                elif y == "h":
                    y = "hearts"
                elif y == "c":
                    y = "clubs"
                elif y == "s":
                    y = "spades"

                cards_1.append([x, y])

            print("for hand")
            cards_2 = []
            for i in range(2):
                x = int(input("Enter number for {}:".format(i + 1)))
                y = (input("Enter card for {}:".format(i + 1)))
                if y == "d":
                    y = "diamonds"
                elif y == "h":
                    y = "hearts"
                elif y == "c":
                    y = "clubs"
                elif y == "s":
                    y = "spades"

                cards_2.append([x, y])

            Interpretation.interpreting_card(table_cards=cards_1, hand_cards=cards_2, player="AI")
            best = Interpretation.AI
            print("\n\n{} : {}, {}, {}, {}, {}\n\n".format(
                Interpretation.hand_rankings[best[5][0]], best[0], best[1], best[2], best[3], best[4]))
            Interpretation.interpreting_possibility()
            print(Interpretation.predictions_ai, "\n")
            print(Interpretation.predictions_opp, "\n")
            print(Interpretation.ratio, "\n")

            turn = 2
            while turn != 4:
                try:
                    x = int(input("Enter number for {}:".format(turn + 2)))
                    y = (input("Enter card for {}:".format(turn + 2)))
                    if y == "d":
                        y = "diamonds"
                    elif y == "h":
                        y = "hearts"
                    elif y == "c":
                        y = "clubs"
                    elif y == "s":
                        y = "spades"

                    cards_1.append([x, y])

                    Interpretation.interpreting_card(table_cards=cards_1, hand_cards=cards_2, player="AI")
                    best = Interpretation.AI
                    print("\n\n{} : {}, {}, {}, {}, {}\n\n".format(
                        Interpretation.hand_rankings[best[5][0]], best[0], best[1], best[2], best[3], best[4]))
                    Interpretation.interpreting_possibility()
                    print(Interpretation.predictions_ai, "\n")
                    print(Interpretation.predictions_opp, "\n")
                    print(Interpretation.ratio, "\n")
                    turn += 1

                except ValueError:
                    print("\nInput is incorrect\n")

        except ValueError:
            print("\nInput is incorrect\n")
