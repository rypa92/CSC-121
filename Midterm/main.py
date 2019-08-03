import BlackJackClasses
import sys


def main():
    def EndRound():
        print()
        print("Turn over!\n")
        print(player)
        print()
        print(dealer.endofRoundTotal())
        print()
        # If player busted ..
        if int(player.scores()[-1] > 21):
            print("You busted.")
            print("Losing is a bummer..")
            print("$0 was gained. Better luck next time!")
        # If dealer busted ..
        elif any(i > 21 for i in dealer.scores()):
            print("You win ${w}!".format(w=betAmount * 2))
            player.money = player.money + betAmount * 2
            print("Total Money: ${m}".format(m=player.money))
        # If player has a higher score ..
        elif int(player.scores()[-1]) > int(dealer.scores()[-1]):
            print("You win ${w}!".format(w=betAmount * 2))
            player.money = player.money + betAmount * 2
            print("Total Money: ${m}".format(m=player.money))
        # If dealer has a higher score ..
        elif int(player.scores()[-1]) < int(dealer.scores()[-1]):
            print("The dealer had a higher score.")
            print("Losing is a bummer..")
            print("$0 was gained. Better luck next time!")
        # If play and dealer tie ..
        elif int(player.scores()[-1]) == int(dealer.scores()[-1]):
            print("Both hands were equal!")
            print("House always wins a little. Half of your bet will be returned.")
            print("You received ${w}.".format(w=betAmount / 2))
            player.money = player.money + betAmount / 2
        else:
            print("Broken?")

    # Fanciness setup
    print("===================================")
    print("==♥♦♣♠ WELCOME TO BLACK JACK ♠♣♦♥==")
    print("===================================")
    playername = input("Please enter your name: ")
    print("We will start by using the $100 you have in your bank account.")
    print("Enjoy gambling!")

    # Setup player and dealer
    player = BlackJackClasses.player(playername, 100)
    dealer = BlackJackClasses.dealer("Dealer", 100)

    # Main Loop
    while True:
        # Turn Loop
        while True:
            # Create Deck
            deck = BlackJackClasses.deck()

            # Determine if the deck needs changing BEFORE the turn.
            if len(deck.new_deck) <= 10:
                print("\n")
                print(deck.reset())
                print("\n")

            pHand = deck.dealHand()
            dHand = deck.dealHand()
            player.new_hand(pHand)
            dealer.new_hand(dHand)

            # Get bets from player
            while True:
                try:
                    betAmount = int(input("Please enter an amount to bet: (You may enter a '0' to quit.) "))
                    if betAmount > player.money:
                        raise ValueError
                    elif player.money == 0:
                        print("You're out of money! Thanks for playing!")
                        sys.exit()
                    elif betAmount == 0:
                        print("Thanks for playing!")
                        sys.exit()
                except ValueError:
                    print("Please enter an amount less than your current money.")
                    continue
                else:
                    player.bet = betAmount
                    player.money = player.money - betAmount
                    break

            # Play the game!
            while True:
                # Print player information
                print(player)
                print()

                # Print dealer information
                print(dealer)
                print()

                if betAmount == 0:
                    break
                elif 21 in dealer.scores():
                    EndRound()
                    break
                elif 21 in player.scores():
                    EndRound()
                    break
                elif int(player.scores()[0]) < 22:
                    print()
                    print("===================================")
                    print("= 1 - Hit me!                     =")
                    print("= 2 - Stand                       =")
                    print("===================================")
                    while True:
                        try:
                            selection = input("What would you like to do? ")
                        except ValueError:
                            print("Please enter a valid selection")
                            continue
                        else:
                            break
                    if int(selection) == 1:
                        player.hit(deck.dealCard())
                    elif int(selection) == 2:
                        while dealer.scores()[0] < 17:
                            dealer.hit(deck.dealCard())
                        EndRound()
                        break
                else:
                    EndRound()
                    break


main()
