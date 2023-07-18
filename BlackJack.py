import random

suits = ("Hearts", "Diamonds", "Clubs", "Spades")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self) :
        self.allcards=[]
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.allcards.append(created_card)
    def shuffle(self):
        random.shuffle(self.allcards)
    def deal(self):
        return self.allcards.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank] #Adding the values of drawn cards

        #tracking aces
        if card.rank =="Ace":
            self.aces+=1
    
    def adjust_for_ace(self):
        while self.value>21 and self.aces:
            self.value -= 10
            self.aces -=1

class Chips:
    def __init__(self, total):
        self.total = total # This can be set to a default value or supplied by a user input
        self.bet = 0
            
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total = self.total - self.bet

def take_bet(Chips):
    while True:

        try:
            Chips.bet = int(input("Enter the amount to bet: "))
        except:
            print("Please enter an integer\n")
        else:
            if Chips.bet>Chips.total:
                print("Sorry you do not have enough chips. you have  {}".format(Chips.total))
            else:
                break

def hit(deck, hand):

    new_card = deck.deal()
    hand.add_card(new_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:

        choice = int(input("Press 1 to Hit and Press 2 to Stand"))
        if choice == 1:
            hit(deck,hand)
        elif choice == 2:
            playing = False
        else:
            print("Please enter valid input\n")
            continue
        break

def show_some(player,dealer):
    print("Dealer's cards\nFirst Card hidden\nSecond Card is : ")
    print(dealer.cards[1],"\n")

    print("Player's Cards are : \n")
    for i in player.cards:
        print(i)
    
    
def show_all(player,dealer):
    
    print("Dealer's Cards are : \n")
    for i in dealer.cards:
        print(i)
    print("The value of Dealer's hand is {}".format(dealer.value))
    print("Player's Cards are : \n")
    for i in player.cards:
        print(i)
    print("The value of Player's hand is {}".format(player.value))

def player_busts(player, dealer, chips):
    print("Bust player")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins ")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Bust Dealer")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("Dealer Wins")
    chips.lose_bet()
    
def push(player, dealer):
    print("Dealer and player Tie! PUSH")


while True:
    print("Welcome to Blackjack Game\n")
    # Print an opening statement

    
    # Create & shuffle the deck, deal two cards to each player
    New_deck = Deck()
    New_deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(New_deck.deal())
    player_hand.add_card(New_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(New_deck.deal())
    dealer_hand.add_card(New_deck.deal())
    
    # Set up the Player's chips
    n = int ( input("Enter the amount of chips you want to start with: \n"))
    player_chips = Chips(n)
    
    

    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(New_deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value>21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value<=21:
        while dealer_hand.value<17:
            hit(New_deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value>21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif player_hand.value>21:
            player_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value>player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
            
        elif player_hand.value>dealer_hand.value:

            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)
        

    
    # Inform Player of their chips total 
    print("The total chips of player is {}".format(player_chips.total))
    
    # Ask to play again
    new = input("Do you wanna play again? Y/N: \n")
    if new[0].lower()=='y':
        playing = True
        
    else:
        print("Thank you for playing! \n")
        break
