"""
balanced-dice
----------------
Author: Nida Anis
Date: 21/12/2024
----------------
Description:
This program compares two dice rolling algorithms:
1. Standard dice: Fully random rolls.
2. Balanced dice: Ensures rolls follow expected probabilities.
 
Features:
- Simulates and compares both algorithms.
- Analyses roll distributions for both algorithms.
- Visualises comparison results.
""" 

# Import relevant modules
import random
import matplotlib.pyplot as plt

"""
----------------
Constants
----------------
"""

# Expected distribution of dice rolls (2-12)
EXPECTED_DIST_2_12 = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1
}

"""
----------------
Functions
----------------
"""

def roll_standard_dice():
    """
    Rolls standard dice.
    """
    return random.randint(1,6) + random.randint(1, 6)

def create_balanced_queue(dist):
    """
    Creates a balanced queue of dice rolls.
    The queue is shuffled to introduce randomness.
    """
    queue = []
    for number, count in dist.items():
        queue.extend([number]*count)
    random.shuffle(queue)
    return queue

def roll_balanced_dice(queue):
    """
    Rolls balanced dice.
    If the queue is empty, it will be regenerated.
    """
    if queue == []:
        queue = create_balanced_queue(EXPECTED_DIST_2_12)
    return queue.pop(), queue

def simulate_rolls(roll_function, num_rolls, *args):
    """
    Simulates dice rolls.
    Takes a given roll algorithm and returns results.
    """
    results = []
    args = list(args)
    for i in range(num_rolls):
        if args:
            roll, args[0] = roll_function(*args)
            results.append(roll)
        else:
            roll = roll_function()
            results.append(roll)
    return results

def visualise_results(*args):
    """
    Visualises simulation results using bar charts.
    Each argument is a tuple of (results, title), where:
    - "results": A list of dice roll results.
    - "label": The legend label for the dataset.
    """

    width = 0.8 / len(args) # Adjust bar width based on number of datasets
    positions = -0.4 + width / 2 # Starting position offset for each bar

    # For each set of results and titles:
    for results, label in args:
        counts = {i: results.count(i) for i in range(2, 13)}

        # Plot the graphs
        plt.bar(
            [k + positions for k in counts.keys()], # Offset k positions
            counts.values(),
            width = width,
            edgecolor = "black",
            alpha = 0.7,
            label = label
        )
        positions += width # Shift positions for next dataset

    # Add labels
    plt.title("Simulation results")
    plt.xlabel("Dice roll")
    plt.ylabel("Frequency")
    plt.xticks(range(2,13)) # Add ticks for each dice roll
    plt.legend()
    plt.show()

"""
----------------
Main program
----------------
"""

# Main program
def main():
    print("----------------")
    print("BALANCED DICE SIMULATION")
    print("----------------")
    try:
        num_rolls = int(input("\nEnter the number of rolls: "))
        if num_rolls <= 0:
            raise ValueError("Number of rolls must be positive.")
    except ValueError as error:
        print(f"Error: {error}")
        return

    choice = input("Choose your algorithm: (S)tandard or (B)alanced? ")

    # If user chooses standard, run standard dice logic
    if choice.lower() in ("s", "standard"):
        standard_results = simulate_rolls(roll_standard_dice, num_rolls)
        visualise_results((standard_results, "Standard dice distribution"))

        # Ask the user if they would like to overlay with a balanced dice graph
        choice = input("Would you like to overlay with a balanced dice graph? (Y)es or (N)o: ")
        
        # If user chooses yes, overlay the graphs
        if choice.lower() in ("y", "yes"):
            balanced_queue = create_balanced_queue(EXPECTED_DIST_2_12)
            balanced_results = simulate_rolls(roll_balanced_dice, num_rolls, balanced_queue)
            visualise_results(
                (standard_results, "Standard dice"),
                (balanced_results, "Balanced dice")
            )

    # If user chooses balanced, run balanced dice logic
    elif choice.lower() in ("b", "balanced"):
        balanced_queue = create_balanced_queue(EXPECTED_DIST_2_12)
        balanced_results = simulate_rolls(roll_balanced_dice, num_rolls, balanced_queue)
        visualise_results((balanced_results, "Balanced dice distribution"))

        # Ask the user if they would like to overlay with a standard dice graph
        choice = input("Would you like to overlay with a standard dice graph? (Y)es or (N)o: ")
        
        # If user chooses yes, overlay the graphs
        if choice.lower() in ("y", "yes"):
            standard_results = simulate_rolls(roll_standard_dice, num_rolls)
            visualise_results(
                (balanced_results, "Balanced dice"),
                (standard_results, "Standard dice")
            )
    
    else:
        print("You have made an invalid choice.")
        print("Please choose (S)tandard or (B)alanced.")

if __name__ == "__main__":
    main()