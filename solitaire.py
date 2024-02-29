import random

class SolitaireGame():
    def __init__(self):
        self.cards = [
            "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sJ", "sQ", "sK", "sA",  # spades (black)
            "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "HA",  # hearts (red)
            "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cJ", "cQ", "cK", "cA",  # clubs (black)
            "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", "DA"  # diamonds (red)
        ]

        self.ranks_value = {"X": 0, "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}

        self.card_input = []

        self.index = 0 # cycle through stock index
        self.movable_element_index = 0 # movable element index for indexing

        self.game_over = False

        self.deal = False

        self.movable_last_elements = []
        self.movable_last_elements_unorganized = []

        self.stock = ['[]']
        self.current_stock = self.stock[-1]
        self.current_stock_removed_tracker = []
        self.current_stock_removed_index = 0
        self.current_stock_removed_index_copy = 0
        self.previous_stock = self.stock[-1]
        self.stock_reduction = False
        self.stock_reduction_for_dealing = False

        self.piles = []

        self.revealed_cards = []
        self.revealed_pile_cards = set()
        self.revealed_foundation_cards = []

        self.foundations_spades = ['XX']
        self.foundations_hearts = ['XX']
        self.foundations_clubs = ['XX']
        self.foundations_diamonds = ['XX']

        self.table = []

        self.load_game = False

    def create_deck(self):
        random.shuffle(self.cards)
        return self.cards
    
    def display_table_stock_and_foundations(self):
        print()
        if self.stock_reduction and self.current_stock in self.current_stock_removed_tracker:
            self.current_stock = self.previous_stock
            self.previous_stock = self.stock[self.current_stock_removed_index - 2]

            self.stock_reduction = False
            self.current_stock_removed_index = 0


        current_spades = self.foundations_spades[-1] if len(self.foundations_spades) > 1 else self.foundations_spades[0]
        current_hearts = self.foundations_hearts[-1] if len(self.foundations_hearts) > 1 else self.foundations_hearts[0]
        current_clubs = self.foundations_clubs[-1] if len(self.foundations_clubs) > 1 else self.foundations_clubs[0]
        current_diamonds = self.foundations_diamonds[-1] if len(self.foundations_diamonds) > 1 else self.foundations_diamonds[0]
        print('------------------------------------------------------------------------')
        print(f"{self.index} Current_Stock: {self.current_stock}           Foundations:   s: {''.join(current_spades)}  H: {''.join(current_hearts)}  c: {''.join(current_clubs)}  D: {''.join(current_diamonds)}")
        print()
        # print Table at the bottom
        print("Table")
        print()
        print(" 1          2          3          4          5          6          7")
        print()
        print(max(len(col) for col in self.table))
        for i in range(max(len(col) for col in self.table)):

            for col in self.table:

                if i >= len(col):  # check if i is greater than or equal to the length of the column
                    print('      ', end='     ')  # print empty spaces for shorter columns
                else:
                    card = col[i]
                    if card in self.revealed_pile_cards or i == len(col) - 1:
                        print(f' {card:<5}', end='     ')

                        self.revealed_pile_cards.add(card) # adds the card to revealed pile cards when revealed or when it is the last in the element
                    else:
                        print(' []   ', end='     ')  # print a hidden card placeholder


            print()
        
        print('-----------------------------------------------------------------------')
        
        if self.card_input:
            print("Input", self.card_input)
        print()

        print()
        print("Commands:")
        print("[1] Move")
        print("[2] Deal")
        print("[3] Save")
        print("[4] Load")
        print("[CTRL + C] Exit")
        print()

    def setup_game(self):
        deck = self.create_deck()

        self.stock.extend(deck[:24])
        self.piles.extend(deck[24:])

        # setting up the 7 piles
        self.table.append(self.piles[:1])
        self.table.append(self.piles[1:3])
        self.table.append(self.piles[3:6])
        self.table.append(self.piles[6:10])
        self.table.append(self.piles[10:15])
        self.table.append(self.piles[15:21])
        self.table.append(self.piles[21:])

    def stock_cycle(self):

        while self.index < len(self.stock):
            if self.index == (len(self.stock) - 1): # if the stock reach end, totally reset the sht
                self.index = 0
                self.current_stock = []
                copy = self.stock[1:]
                random.shuffle(copy)
                self.stock[1:] = copy
                self.deal = False

            if len(self.stock) == 0:
                self.current_stock = [1]

            if self.deal: # if deal
                if self.stock_reduction_for_dealing:
                    self.current_stock = self.stock[self.index]
                    self.previous_stock = self.stock[self.index - 1]
                    self.stock_reduction_for_dealing = False
                else:
                    self.current_stock = self.stock[self.index + 1]
                    self.previous_stock = self.stock[self.index]

                self.index += 1

                self.deal = False

                break

            if not self.deal or not self.current_stock: # if not yet deal, nothing happens
                self.current_stock = []
                break

            else:
                self.current_stock = self.stock[self.index]
                break

    def start_game(self):
        self.setup_game()

        while not self.game_over:    

            print()
            print()
            print()
            print()
            print()
            print()
            print("                          S O L I T A I R E")

            self.display_table_stock_and_foundations()

            # ---------------------------- compile all revealed cards in the board ---------------------------


            # piles
            for pile in self.revealed_pile_cards:
                self.revealed_cards.append(pile)

            # stock
            self.revealed_cards.append(self.current_stock) 

            # foundation
            self.revealed_cards.append(''.join(self.foundations_spades[-1])) if len(self.foundations_spades) > 1 else ''
            self.revealed_cards.append(''.join(self.foundations_hearts[-1])) if len(self.foundations_hearts) > 1 else ''
            self.revealed_cards.append(''.join(self.foundations_clubs[-1])) if len(self.foundations_clubs) > 1 else ''
            self.revealed_cards.append(''.join(self.foundations_diamonds[-1])) if len(self.foundations_diamonds) > 1 else ''
            # ---------------------------- compile all revealed cards in the board ---------------------------
            
    

            # ---------------------- combine all foundation cards to the foundation --------------------
            self.revealed_foundation_cards.append(''.join(self.foundations_spades[-1])) if len(self.foundations_spades) > 1 else ''
            self.revealed_foundation_cards.append(''.join(self.foundations_hearts[-1])) if len(self.foundations_hearts) > 1 else ''
            self.revealed_foundation_cards.append(''.join(self.foundations_clubs[-1])) if len(self.foundations_clubs) > 1 else ''
            self.revealed_foundation_cards.append(''.join(self.foundations_diamonds[-1])) if len(self.foundations_diamonds) > 1 else ''
            # ---------------------- combine all foundation cards to the foundation --------------------


            #
            for i in self.table:
                #print(i)

                revealed = []

                for j in i:
                    if j in self.revealed_pile_cards:
                        revealed.append(j)
                        self.movable_last_elements_unorganized.append(j)

                #print(revealed)

                self.movable_last_elements.append(revealed)

            #




            print()
            user_input = input("Enter choice: ")
            while user_input not in ['1', '2', '3', '4']:
                self.display_table_stock_and_foundations()
                user_input = input("Error. Please enter a valid choice: ")
            
            self.load_game = False
            
            if user_input == '1':
                self.display_table_stock_and_foundations()
                card_input = input("Pick a card: ")

                while card_input not in self.cards or card_input not in self.revealed_cards:
                    if card_input not in self.cards:
                        print("That is not a card!")
                        self.display_table_stock_and_foundations()
                        card_input = input("Pick a valid card: ")
                    
                    elif card_input not in self.revealed_cards:
                        print("Card is not visible!")
                        self.display_table_stock_and_foundations()
                        card_input = input("Pick a valid visible card: ")
                    
                    else:
                        break


                self.card_input = card_input # initializes the input as the global variable


                # ---------------------- INDEXING OF LAST ELEMENTS ----------------------------
                if self.card_input in self.movable_last_elements_unorganized:# and add something here that i forgot:
                    for x, row in enumerate(self.movable_last_elements):
                        for y, card in enumerate(row):
                            if card == self.card_input:
                                self.movable_element_index = (x, y)

                # ---------------------- INDEXING OF LAST ELEMENTS ----------------------------



                # if card was in pile
                if self.card_input in self.revealed_pile_cards:
                    print('Pile')
                    
                    target_pile = input("Target Pile: ")
                    while target_pile not in ['s', 'H', 'c', 'D', '1', '2', '3', '4', '5', '6', '7']:
                        target_pile = input("Please enter a valid target pile: ")

                        
                    # ------------------------------- TO FOUNDATIONS -------------------------------
                    # if foundations spades is the target
                    if target_pile == 's':
                        if self.card_input[0] == 's':
                            current_spade = str(self.foundations_spades[-1] if len(self.foundations_spades) > 1 else self.foundations_spades[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_spade[1:]] == 0:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_spades.append(self.card_input)                          
                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_spade[1:]] == 1:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_spades.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue



                    # if foundations Hearts is the target
                    elif target_pile == 'H':
                        if self.card_input[0] == 'H':
                            current_heart = str(self.foundations_hearts[-1] if len(self.foundations_hearts) > 1 else self.foundations_hearts[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_heart[1:]] == 0:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_hearts.append(self.card_input)                          
                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_heart[1:]] == 1:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_hearts.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue


                    # if foundations clubs is the target
                    elif target_pile == 'c':
                        if self.card_input[0] == 'c':
                            current_club = str(self.foundations_clubs[-1] if len(self.foundations_clubs) > 1 else self.foundations_clubs[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_club[1:]] == 0:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_clubs.append(self.card_input)                          
                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_club[1:]] == 1:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_clubs.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue

                    # if foundations Diamonds is the target
                    elif target_pile == 'D':
                        if self.card_input[0] == 'D':
                            current_diamond = str(self.foundations_diamonds[-1] if len(self.foundations_diamonds) > 1 else self.foundations_diamonds[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_diamond[1:]] == 0:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_diamonds.append(self.card_input)                          
                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_diamond[1:]] == 1:
                                self.revealed_pile_cards.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_diamonds.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue
                    # ------------------------------- TO FOUNDATIONS -------------------------------



                    # ------------------------------- TO ANOTHER PILE -------------------------------
                    elif target_pile == '1':
                    
                        if self.table[0]:
                            if (self.card_input[0].isupper() and str(self.table[0][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[0][-1][0]).isupper()):
                                if self.ranks_value[self.table[0][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[0].append(movable_last_element)    

                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()                          
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[0].append(movable_last_element) 
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '2':

                        if self.table[1]:
                            if (self.card_input[0].isupper() and str(self.table[1][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[1][-1][0]).isupper()):
                                if self.ranks_value[self.table[1][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[1].append(movable_last_element)    
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[1].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '3':

                        if self.table[2]:
                            if (self.card_input[0].isupper() and str(self.table[2][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[2][-1][0]).isupper()):
                                if self.ranks_value[self.table[2][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[2].append(movable_last_element)    
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[2].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '4':

                        if self.table[3]:
                            if (self.card_input[0].isupper() and str(self.table[3][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[3][-1][0]).isupper()):
                                if self.ranks_value[self.table[3][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[3].append(movable_last_element)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[3].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '5':

                        if self.table[4]:
                            if (self.card_input[0].isupper() and str(self.table[4][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[4][-1][0]).isupper()):
                                if self.ranks_value[self.table[4][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[4].append(movable_last_element)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[4].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '6':

                        if self.table[5]:
                            if (self.card_input[0].isupper() and str(self.table[5][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[5][-1][0]).isupper()):
                                if self.ranks_value[self.table[5][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[5].append(movable_last_element)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[5].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '7':

                        if self.table[6]:
                            if (self.card_input[0].isupper() and str(self.table[6][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[6][-1][0]).isupper()):
                                if self.ranks_value[self.table[6][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                        self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                        self.table[6].append(movable_last_element)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                for movable_last_element in self.movable_last_elements[self.movable_element_index[0]][self.movable_element_index[1]:]:
                                    self.table = [[card for card in sublist if card != movable_last_element] for sublist in self.table]
                                    self.table[6].append(movable_last_element)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                # if card was in stock
                elif self.card_input in self.current_stock:
                    print('Stock')

                    target_pile = input("Target Pile: ")
                    while target_pile not in ['s', 'H', 'c', 'D', '1', '2', '3', '4', '5', '6', '7']:
                        target_pile = input("Please enter a valid target pile: ")

                    # ------------------------------- TO FOUNDATIONS -------------------------------
                    # if foundations spades is the target
                    if target_pile == 's':
                        if self.card_input[0] == 's':
                            current_spade = str(self.foundations_spades[-1] if len(self.foundations_spades) > 1 else self.foundations_spades[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_spade[1:]] == 0: # if current spade is nothing, then you can append 1 only
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_spades.append(self.card_input)
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_spade[1:]] == 1: # if the current spade is 1 rank lower than the card input, then you can append
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_spades.append(self.card_input)
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue



                    # if foundations Hearts is the target
                    elif target_pile == 'H':
                        if self.card_input[0] == 'H':
                            current_heart = str(self.foundations_hearts[-1] if len(self.foundations_hearts) > 1 else self.foundations_hearts[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_heart[1:]] == 0:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_hearts.append(self.card_input)   
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)

                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_heart[1:]] == 1:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_hearts.append(self.card_input)
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)

                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue


                    # if foundations clubs is the target
                    elif target_pile == 'c':
                        if self.card_input[0] == 'c':
                            current_club = str(self.foundations_clubs[-1] if len(self.foundations_clubs) > 1 else self.foundations_clubs[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_club[1:]] == 0:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table]
                                self.foundations_clubs.append(self.card_input)  
                                self.stock_reduction = True                         
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)

                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_club[1:]] == 1:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_clubs.append(self.card_input)
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue

                    # if foundations Diamonds is the target
                    elif target_pile == 'D':
                        if self.card_input[0] == 'D':
                            current_diamond = str(self.foundations_diamonds[-1] if len(self.foundations_diamonds) > 1 else self.foundations_diamonds[0])
                        
                            # check if input is applicable to place in the foundations spades (if 2nd index of input is lower than the 2nd index of the current spade)
                            if self.ranks_value[self.card_input[1:]] == 1 and self.ranks_value[current_diamond[1:]] == 0:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] 
                                self.foundations_diamonds.append(self.card_input)   
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)

                            
                            elif self.ranks_value[self.card_input[1:]] - self.ranks_value[current_diamond[1:]] == 1:
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input)
                                self.table = [[card for card in sublist if card != self.card_input] for sublist in self.table] # removes the card in the specific pile
                                self.foundations_diamonds.append(self.card_input)
                                self.stock_reduction = True    
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print("That move is invalid!")
                                print()

                        else:
                            print()
                            print('That move is invalid!')
                            print()
                            continue
                    # ------------------------------- TO FOUNDATIONS -------------------------------



                    # ------------------------------- TO PILE -------------------------------
                    elif target_pile == '1':
                    
                        if self.table[0]:
                            if (self.card_input[0].isupper() and str(self.table[0][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[0][-1][0]).isupper()):
                                if self.ranks_value[self.table[0][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[0].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)
  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()                          
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[0].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '2':

                        if self.table[1]:
                            if (self.card_input[0].isupper() and str(self.table[1][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[1][-1][0]).isupper()):
                                if self.ranks_value[self.table[1][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[1].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[1].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '3':

                        if self.table[2]:
                            if (self.card_input[0].isupper() and str(self.table[2][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[2][-1][0]).isupper()):
                                if self.ranks_value[self.table[2][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[2].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)   
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[2].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '4':

                        if self.table[3]:
                            if (self.card_input[0].isupper() and str(self.table[3][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[3][-1][0]).isupper()):
                                if self.ranks_value[self.table[3][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[3].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[3].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '5':

                        if self.table[4]:
                            if (self.card_input[0].isupper() and str(self.table[4][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[4][-1][0]).isupper()):
                                if self.ranks_value[self.table[4][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[4].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[4].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '6':

                        if self.table[5]:
                            if (self.card_input[0].isupper() and str(self.table[5][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[5][-1][0]).isupper()):
                                if self.ranks_value[self.table[5][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[5].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)   
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[5].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()


                    elif target_pile == '7':

                        if self.table[6]:
                            if (self.card_input[0].isupper() and str(self.table[6][-1][0]).islower()) or (self.card_input[0].islower() and str(self.table[6][-1][0]).isupper()):
                                if self.ranks_value[self.table[6][-1][1:]] - self.ranks_value[self.card_input[1:]] == 1:
                                    # satisfying some criteria for the stock mechanism
                                    self.current_stock_removed_index = self.stock.index(self.card_input)
                                    self.stock.remove(self.card_input) # removing the stock card from the list
                                    
                                    self.table[6].append(self.card_input) # moving the stock card to the first pile
                                    
                                    # satisfying some criteria for the stock mechanism
                                    self.stock_reduction = True 
                                    self.stock_reduction_for_dealing = True
                                    self.current_stock_removed_tracker.append(self.card_input)  
                                else:
                                    print()
                                    print('That move is invalid!')
                                    print()
                            else:
                                print()
                                print('That move is invalid!')
                                print()
                        else:
                            if self.card_input[1:] == 'K':
                                # satisfying some criteria for the stock mechanism
                                self.current_stock_removed_index = self.stock.index(self.card_input)
                                self.stock.remove(self.card_input) # removing the stock card from the list
                                
                                self.table[6].append(self.card_input) # moving the stock card to the first pile
                                
                                # satisfying some criteria for the stock mechanism
                                self.stock_reduction = True 
                                self.stock_reduction_for_dealing = True
                                self.current_stock_removed_tracker.append(self.card_input)
                            else:
                                print()
                                print('That move is invalid!')
                                print()
  

            

                # if card was in foundation
                elif self.card_input in self.revealed_foundation_cards:
                    print('Foundation')

                

            # deal the stock cards
            if user_input == '2':
                # call a stock card cycler
                self.deal = True
                self.stock_cycle()

            # save option
            if user_input == '3':
                filename_input = input("Enter a filename to save: ")
                SolitaireSaveLoad.save_game_state(self, filename_input)

            # load option
            if user_input == '4':
                filename_input = input("Enter a filename to load: ")
                SolitaireSaveLoad.load_game_state(self, filename_input)

            # reinitialize 
            if not self.load_game:
                self.revealed_cards = []
                self.revealed_foundation_cards = []
                self.last_elements = []
                self.movable_last_elements = []
                self.movable_last_elements_unorganized = []


class SolitaireSaveLoad():
    @staticmethod

    def save_game_state(self, filename_input):

        print()
        print("Saved!")
        
        with open(filename_input, "w") as file:
            # saving necessary game state variables to the file

            # whole stock
            file.write(f"{' '.join(self.stock)}\n") 

            # whole table
            for table_column in self.table:
                file.write(f"{self.table.index(table_column) + 1} {' '.join(table_column)}\n")

            # each foundations
            file.write(f"{' '.join(self.foundations_spades)} {' '.join(self.foundations_hearts)} {' '.join(self.foundations_clubs)} {' '.join(self.foundations_diamonds)}\n")

            # movable last elements in pile
            file.write(f"{' '.join(self.movable_last_elements_unorganized)}\n")

            # piles
            file.write(f"{' '. join(self.piles)}\n")

            # revealed pile cards
            file.write(f"{' '. join(self.revealed_pile_cards)}")
          

    def load_game_state(self, filename_input):

        print()
        print("Loading!")

        try: 
            with open(filename_input, "r") as file:
                # where to store the values
                final_stock_list = []
                final_table = []
                final_spades = ['XX']
                final_hearts = ['XX']
                final_clubs = ['XX']
                final_diamonds = ['XX']
                final_movable_list_unorganized = []
                final_piles = []
                final_revealed_cards = set()

                # read each lines

                lines = file.readlines()

                index = 0

                for element in lines:

                    if index == 0: # stock
                        stock_list = element.split()
                        for stock in stock_list:
                            final_stock_list.append(stock)


                        index += 1

                    elif index == 1:
                        first_column = element.split()
                        column = []
                        for element in first_column:
                            if element != '1':
                                column.append(element)
                        final_table.append(column)

                        index += 1

                    elif index == 2:
                        second_column = element.split()
                        column = []
                        for element in second_column:
                            if element != '2':
                                column.append(element)
                        final_table.append(column)

                        index += 1

                        
                    elif index == 3:
                        third_column = element.split()
                        column = []
                        for element in third_column:
                            if element != '3':
                                column.append(element)
                        final_table.append(column)
                        
                        index += 1


                    elif index == 4:
                        fourth_column = element.split()
                        column = []
                        for element in fourth_column:
                            if element != '4':
                                column.append(element)
                        final_table.append(column)

                        index += 1


                    elif index == 5:
                        fifth_column = element.split()
                        column = []
                        for element in fifth_column:
                            if element != '5':
                                column.append(element)
                        final_table.append(column)

                        index += 1

                    elif index == 6:
                        sixth_column = element.split()
                        column = []
                        for element in sixth_column:
                            if element != '6':
                                column.append(element)
                        final_table.append(column)

                        index += 1

                    elif index == 7:
                        seventh_column = element.split()
                        column = []
                        for element in seventh_column:
                            if element != '7':
                                column.append(element)
                        final_table.append(column)

                        index += 1




                    # foundations
                    elif index == 8:
                        foundations = element.split()
                        x = 0
                        

                        for foundation in foundations:
                            suit = foundation[0]
                            card = foundation[1:]

                            if suit == 's':
                                final_spades.append(foundation)
                            elif suit == 'H':
                                final_hearts.append(foundation)
                            elif suit == 'c':
                                final_clubs.append(foundation)
                            elif suit == 'D':
                                final_diamonds.append(foundation)

                        index += 1


                    
                    # movable last elements
                    elif index == 9:
                        last_elements = element.split()

                        for last in last_elements:
                            final_movable_list_unorganized.append(last)

                    
                        index += 1


                    # piles
                    elif index == 10:
                        piles = element.split()

                        for pile in piles:
                            final_piles.append(pile)

                        index += 1


                    # revealed pile cards
                    elif index == 11:
                        revealed = element.split()

                        for reveal in revealed:
                            final_revealed_cards.add(reveal)
                            




                # integrating the new values to the game, meaning loading the game na
                self.load_game = True
                self.stock = final_stock_list
                self.table = final_table
                self.foundations_spades = final_spades
                self.foundations_hearts = final_hearts
                self.foundations_clubs = final_clubs
                self.foundations_diamonds = final_diamonds
                self.movable_last_elements_unorganized = final_movable_list_unorganized
                self.piles = final_piles
                self.revealed_pile_cards = final_revealed_cards

                  
        except FileNotFoundError:
            print("No saved game state found. Start a new game.")
        
              
            
solitaire_game = SolitaireGame()

solitaire_game.start_game()
