#Libraries requried
import matplotlib.pyplot as plt
import random
import requests
import time

#My current key for the API
api_key = 'c2eaa76b-c34c-4d3a-8f33-da95a230d9ea'


def main():
    print('Welcome Pokemon Navigator')
    name = input("What is your name? ")
    #Starts the master loop
    while True:
        print(f'What would you like to do {name}?')
        print('Enter 1 to see how many times a Pokemon has appeared on a card')
        print("Enter 2 to see the rarity breakdown of a those cards")
        print('Enter 3 to compare how many times several Pokemon have appeared')
        print('Enter 4 to play a game of Bulbasaur Charmander Squirtle!')
        print('Enter 0 to exit')
        #Allows card number look-up through the card function
        try:
            choice = int(input('Choice: '))
        except (ValueError):
            print("That is not a valid choice.")
            break
        if choice == 1:
            cards_choice()
        #Allows card rarity look-up through the rarity function
        elif choice == 2:
            rarity_choice()
        #Aloows the user to compare several Pokemon through the compare function
        elif choice == 3:
            compare_choice()
        #Allows the user to play a game through the game function
        elif choice == 4:
            game_choice()
        #Breaks the master loop
        else:
            print("That is not a valid choice.")
            break


def graph_cards(name_of_pokemon, poke_dict):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=name:{name_of_pokemon}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    count = data['count']
    if count > 0:
        poke_dict[name_of_pokemon] = [count]
    else:
        print(f'{name_of_pokemon} is not a valid Pokemon name.')
    
poke_dict = {}

def produce_graph(poke_dict):
    name = []
    number = []
    items = poke_dict.items()
    for item in items:
        name.append(item[0]), number.append(item[1][0])
    plt.barh(name, number)
    plt.show()

def compare_choice():
    while True:
        pokemon_name = input("Enter Pokemon one at a time,\nEnter 'graph' to compare selected Pokemon: ")
        if pokemon_name == 'graph':
            break
        else:
            graph_cards(pokemon_name, poke_dict)
    produce_graph(poke_dict)


def make_rarity_graph(rarity_dict):
    rarity = []
    number = []
    items = rarity_dict.items()
    for item in items:
        rarity.append(item[0]), number.append(item[1]) 
    plt.barh(rarity, number)
    plt.show()


#Returns card rarities for Pokemon in a selected Pokedex range
def get_rarity(name):
    a_list = []
    #Access all cards for an individual Pokemon from API based on Pokedex Number. 
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=name:{name}'
    #Returns data on those cards in JSON form
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json()
    #For however many cards that Pokemon has been on
    for i in range(data['count']):
        #What is the rarity of that card (if exists)
        try:
            a_list.append(data['data'][i]['rarity'])
        #Skips cards that do not include a rarity (i.e. McDonalds promos)
        except KeyError:
            pass
    #Returns a list of card rarities for all Pokemon in the selected range.
    gen_one_dict = {i:a_list.count(i) for i in a_list}
    print(gen_one_dict)
    make_rarity_graph(gen_one_dict)


def count_cards(name_of_pokemon):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=name:{name_of_pokemon}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    count = data['count']
    if count > 0:
        print(f'{name_of_pokemon} has appered on {count} cards over the past 25 years.')
    else:
        print(f'{name_of_pokemon} is not a valid Pokemon name.')
    

def count_all_cards(num, card_dict):
    #sets the API endpath based on the pokemons dex num
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:{num}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json()
    #Retrieves data from API and append to dictionary
    card_dict[data['data'][0]['name']] = data['count']
    return card_dict


gen_one = []

def count_rarities(dex_num, a_list):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:{dex_num}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    for i in range(data['count']):
        try:
            a_list.append(data['data'][i]['rarity'])
        except KeyError:
            pass
    return a_list


def rarity_choice():
    print('You can enter the name of a Pokemon')
    print("Or enter 'all' to return all Pokemon")
    print('Warning: all Pokemon will take 5+ min')
    name = input('Choice: ')
    if name == 'all':
        gen_one = []
        for i in range(1, 894):
            count_rarities(i+1, gen_one)
        gen_one_dict = {i:gen_one.count(i) for i in gen_one}
        print(gen_one_dict)
        make_rarity_graph(gen_one_dict)
    else:
        try:
            get_rarity(name)
        except (KeyError):
            print("That is not a valid response.")
    time.sleep(2)

def cards_choice():
    print('You can enter the name of a Pokemon')
    print("Or enter 'all' to return all Pokemon")
    print('Warning: all Pokemon will take 5+ min')
    names = input('Choice: ')
    if names == 'all':
        name_counts = dict()
        for num in range (1, 894):
            try:
                count_all_cards(num, name_counts)
            except IndexError:
                pass
        print(name_counts)
    else:
        try:
            count_cards(names)
        except:
            print("That is not a valid response.")
    time.sleep(2)


#Function for the rock paper scissors themed game
def game_choice():
    print_welcome()
    score = 0
    for i in range(3):
        #Decides what the AI will choose
        ai_move = get_ai_move()
        #Gets the human players move
        human_move = get_human_move()
        #Determines who won the match
        outcome = decide_outcome(ai_move, human_move)
        #Announces who won the match
        announce_result(ai_move, outcome)
        #Keeps track of wins and losses
        score += calc_outcome_score(outcome)
    #Prints the final score 
    print(f'Your score is {score}')

#Keeps track of wins and losses during games
def calc_outcome_score(outcome):
    if outcome == "user wins!":
        return 1
    elif outcome == "tied":
        return 0
    else:
        return -1


#Announces who won the game
def announce_result(ai_move, outcome):
    print(f'The ai chose {ai_move}, {outcome}')

#Determines who won the game based on choices
def decide_outcome(ai_move, human_move):
    if ai_move == human_move:
        return "tied"
    if ai_move == "bulbasaur":
        if human_move == "charmander":
            return "user wins!"
        return "ai wins!"
    if ai_move == "charmander":
        if human_move == "squirtle":
            return "user wins!"
        return "ai wins!"
    if ai_move == "squirtle":
        if human_move == "bulbasaur":
            return "user wins!"
        return "ai wins!"


#Records what choice the human player has made
def get_human_move():
    while True:
        choice = input("Enter bulbasaur, charmander or squirtle: ")
        if choice.lower() == "bulbasaur":
            return choice
        if choice.lower() == "charmander":
            return choice
        if choice.lower() == "squirtle":
            return choice
        else:
            print("invalid choice")
        

#Randomly determines what the computer will choose
def get_ai_move():
    number = random.randint(1, 3)
    if number == 1:
        return 'bulbasaur'
    if number == 2:
        return 'charmander'
    if number == 3:
        return 'squirtle'

#prints a greeting and instructions for the game
def print_welcome():
    print('Welcome to Bulbasaur Charmander Squirtle')
    print('The same as Rock Paper Scissors, but Pokemon themed')
    print('You will play 3 games against the AI')
    print('Bulbasaur(grass) beats Squirtle(water)')
    print('Squirtle(water) beats Charmander(fire)')
    print('Charmander(fire) beats Bulbasaur(grass')
    print('----------------------------------------------')
    print('')


if __name__ == '__main__':
    main()