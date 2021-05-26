import time
import random
import requests
api_key = 'c2eaa76b-c34c-4d3a-8f33-da95a230d9ea'

N_GAMES = 3

def main():
    print('Welcome Pokemon Navigator')
    name = input("What is your name? ")
    while True:
        print(f'What would you like to do {name}?')
        print('Enter 1 to see how many times a Pokemon has appeared on a card')
        print('Enter 2 to look at the rarity breakdown of a Pokemons cards')
        print('Enter 3 to play a game of Bulbasaur, Charmander, Squirtle!')
        print('Enter 0 to exit')
        choice = int(input('Choice: '))
        if choice == 1:
            cards()
        elif choice == 2:
            rarities()
        elif choice == 3:
            game()
        else:
            break


def game():
    print_welcome()
    score = 0
    for i in range(N_GAMES):
        ai_move = get_ai_move()
        human_move = get_human_move()
        outcome = decide_outcome(ai_move, human_move)
        announce_result(ai_move, outcome)
        score += calc_outcome_score(outcome)
    print(f'Your score is {score}')

def calc_outcome_score(outcome):
    if outcome == "user wins!":
        return 1
    elif outcome == "tied":
        return 0
    else:
        return -1


def announce_result(ai_move, outcome):
    print(f'The ai chose {ai_move}, {outcome}')


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
        

def get_ai_move():
    number = random.randint(1, 3)
    if number == 1:
        return 'bulbasaur'
    if number == 2:
        return 'charmander'
    if number == 3:
        return 'squirtle'

def print_welcome():
    print('Welcome to Bulbasaur Charmander Squirtle')
    print('The same as Rock Paper Scissors, but Pokemon themed')
    print('You will play '+str(N_GAMES)+' games against the AI')
    print('Bulbasaur(grass) beats Squirtle(water)')
    print('Squirtle(water) beats Charmander(fire)')
    print('Charmander(fire) beats Bulbasaur(grass')
    print('----------------------------------------------')
    print('')


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


def get_counts(name_of_pokemon):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=name:{name_of_pokemon}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    count = data['count']
    print(f'{name_of_pokemon} has appered on {count} cards over the past 25 years.')
    

def get_name_count(num, card_dict):
    #sets the API endpath based on the pokemons dex num
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:{num}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json()
    #Retrieves data from API and append to dictionary
    card_dict[data['data'][0]['name']] = data['count']
    return card_dict


gen_one = []

def get_count(dex_num, a_list):
    endpoint = f'https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:{dex_num}'
    data = (requests.get(endpoint, data={'X-api-key': api_key})).json() 
    for i in range(data['count']):
        try:
            a_list.append(data['data'][i]['rarity'])
        except KeyError:
            pass
    return a_list


def rarities():
    print('You can enter the name of a Pokemon')
    print("Or enter 'all' to return all Pokemon")
    print('Warning: all Pokemon will take 5+ min')
    name = input('Choice: ')
    if name == 'all':
        gen_one = []
        for i in range(1, 894):
            get_count(i+1, gen_one)
        gen_one_dict = {i:gen_one.count(i) for i in gen_one}
        print(gen_one_dict)
    else:
        try:
            get_rarity(name)
        except (KeyError):
            print("That is not a valid response.")
    time.sleep(2)

def cards():
    print('You can enter the name of a Pokemon')
    print("Or enter 'all' to return all Pokemon")
    print('Warning: all Pokemon will take 5+ min')
    names = input('Choice: ')
    if names == 'all':
        ######     Input what range of pokemon dex numbers you want to retrieve     ######
        name_counts = dict()
        for num in range (1, 894):
            try:
                get_name_count(num, name_counts)
            except IndexError:
                pass
        print(name_counts)
    else:
        try:
            get_counts(names)
        except:
            print("That is not a valid response.")
    time.sleep(2)

if __name__ == '__main__':
    main()