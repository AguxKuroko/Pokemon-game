import requests
import random
import csv
import art
import os


# Function to generate random Pokemon IDs
def generate_random_pokemon_ids(num_pokemon, max_id=151):
    # Generate a list of unique random Pokemon IDs within the specified range
    return random.sample(range(1, max_id + 1), num_pokemon)


# Function to get Pokemon data from the PokeAPI
def get_pokemon_data(pokemon_id):
    # Construct the URL for the PokeAPI using the provided Pokemon ID
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    # Send a GET request to the PokeAPI
    response = requests.get(url)

    # Parse the JSON data from the API response
    data = response.json()

    # Create a dictionary containing relevant Pokemon information
    return {
        "name": data["name"].capitalize(),
        "id": data["id"],
        "height": data["height"],
        "weight": data["weight"]
    }


# Function for the player to choose a stat
def choose_stat():
    # Prompt the player to choose a stat (id, height, weight)
    return input("Choose a stat (id, height, weight): ").lower()


# Function to compare Pokemon stats and determine the winner of a round
def compare_pokemon_stat(player_stat, opponent_stat):
    if player_stat > opponent_stat:
        return "You win!"
    elif player_stat < opponent_stat:
        return "Computer wins!"
    else:
        return "It's a tie!"


# Function to play a round of the Pokemon game
def play_round(chosen_stat):
    # Generate random Pokemon choices for the player and the computer
    pokemon_choices = generate_random_pokemon_ids(3)

    # Display Pokemon choices to the player
    print("\nChoose your Pokemon:")
    for i, pokemon_id in enumerate(pokemon_choices, start=1):
        pokemon_data = get_pokemon_data(pokemon_id)
        print(
            f"{i}. {pokemon_data['name']} (ID: {pokemon_data['id']}, Height: {pokemon_data['height']}, Weight: {pokemon_data['weight']})")

    # Player selects a Pokemon
    user_choice = int(input("Enter the number of the Pokemon you want to use: "))
    player_pokemon_id = pokemon_choices[user_choice - 1]

    # Computer selects a random Pokemon
    opponent_pokemon_id = random.choice(pokemon_choices)

    # Retrieve Pokemon data for the chosen Pokemon and the opponent
    player_pokemon = get_pokemon_data(player_pokemon_id)
    opponent_pokemon = get_pokemon_data(opponent_pokemon_id)

    # Display the chosen Pokemon and the opponent to the player
    print(
        f"\nYour Pokemon: {player_pokemon['name']} (ID: {player_pokemon['id']}, Height: {player_pokemon['height']}, Weight: {player_pokemon['weight']})")
    print(art.vs)
    print(
        f"Computer's Pokemon: {opponent_pokemon['name']} (ID: {opponent_pokemon['id']}, Height: {opponent_pokemon['height']}, Weight: {opponent_pokemon['weight']})")

    # Get the chosen stat for the player and opponent
    player_stat = player_pokemon.get(chosen_stat, 0)
    opponent_stat = opponent_pokemon.get(chosen_stat, 0)

    # Compare Pokemon stats and determine the result of the round
    result = compare_pokemon_stat(player_stat, opponent_stat)

    # Display the result to the player
    print(result)
    return result


# Function to update high scores in a CSV file
def update_high_scores(player_name, player_wins, filename="high_scores.csv"):
    if os.path.exists(filename):
        # If the file exists, open it in append mode and add a new row
        with open(filename, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, player_wins])
    else:
        # If the file doesn't exist, create a new file and write header and data
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Wins"])
            writer.writerow([player_name, player_wins])


# Function to display high scores from a CSV file
def display_high_scores(filename="high_scores.csv"):
    if os.path.exists(filename):
        # If the file exists, open it in read mode and display high scores
        with open(filename, "r", newline='') as file:
            reader = csv.reader(file)
            print("\n--- High Scores ---")

            # Skip the header row when displaying high scores
            next(reader)

            for row in reader:
                print(f"{row[0]}: {row[1]} wins")
    else:
        print("\nNo high scores yet.")


# Main function
def main():
    player_name = input("Enter your name: ")
    chosen_stat = choose_stat()

    rounds = int(input("Enter the number of rounds: "))
    player_wins = 0
    opponent_wins = 0

    for _ in range(rounds):
        print("\n--- Round", _ + 1, "---")
        result = play_round(chosen_stat)

        if "You" in result:
            player_wins += 1
        elif "Computer" in result:
            opponent_wins += 1

    print("\n--- Game Results ---")
    print(f"You win {player_wins} rounds")
    print(f"Computer wins {opponent_wins} rounds")

    if player_wins > opponent_wins:
        print("\nYou win the game!")
        update_high_scores(player_name, player_wins)
    elif player_wins < opponent_wins:
        print("\nComputer wins the game!")
    else:
        print("\nIt's a tie!")

    display_high_scores()

print(art.logo)
main()
print(art.hat)
