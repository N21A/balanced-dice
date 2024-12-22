"""
balanced-dice-gui
----------------
Author: Nida Anis
Date: 22/12/2024
----------------
Description:
This program compares two dice rolling algorithms:
1. Standard dice: Fully random rolls.
2. Balanced dice: Ensures rolls follow expected probabilities.
 
Features:
- Guided User Interface (GUI) program.
- Simulates and compares both algorithms.
- Analyses roll distributions for both algorithms.
- Visualises comparison results.
""" 

# Import relevant modules
import random
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    return random.randint(1, 6) + random.randint(1, 6)

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

def plot_results(results, label, ax):
    """
    Plots dice roll results on a given axis.
    """
    counts = {i: results.count(i) for i in range(2, 13)}
    ax.bar(counts.keys(), counts.values(), label=label, alpha=0.7)
    ax.set_xlabel("Dice roll")
    ax.set_ylabel("Frequency")
    ax.set_title("Dice roll simulation")
    ax.legend(loc="upper right")

"""
Main program
"""

class BalancedDiceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Balanced dice simulator")

        # Active overlay flag
        self.overlay_active = False

        # Number of rolls input
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)
        tk.Label(frame_input, text="Number of rolls:").pack(side=tk.LEFT)
        self.entry_rolls = tk.Entry(frame_input)
        self.entry_rolls.pack(side=tk.LEFT)

        # Dice type selection
        frame_choice = tk.Frame(root)
        frame_choice.pack(pady=10)
        self.dice_choice = tk.StringVar(value="Standard")
        tk.Radiobutton(frame_choice, text="Standard dice", variable=self.dice_choice, value="Standard").pack(side=tk.LEFT)
        tk.Radiobutton(frame_choice, text="Balanced dice", variable=self.dice_choice, value="Balanced").pack(side=tk.LEFT)

        # Overlay checkbox
        frame_overlay = tk.Frame(self.root)
        frame_overlay.pack(pady=10)
        self.overlay_choice = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_overlay, text="Overlay with other dice type", variable=self.overlay_choice).pack()

        # Button to start the simulation
        btn_simulate = tk.Button(root, text="Start simulation", command=self.start_simulation)
        btn_simulate.pack(pady=10)

        # Matplotlib canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Frequency display area
        self.text_freq = tk.Text(root, height=10, width=40, state=tk.DISABLED)
        self.text_freq.pack(pady=10)

        # Clear button to reset the graph
        btn_clear = tk.Button(root, text="Clear graphs and frequencies", command=self.clear_graph)
        btn_clear.pack(pady=5)

    def clear_graph(self):
        """
        Clears the graph and resets overlay options.
        """
        # Clear graph
        self.ax.clear()
        self.canvas.draw()
        self.plotted_dice = set()
        self.overlay_choice.set(False)
        self.overlay_active = False

        # Clear frequencies
        self.text_freq.config(state=tk.NORMAL)
        self.text_freq.delete("1.0", tk.END)
        self.text_freq.config(state=tk.DISABLED)

        # Display messagebox
        messagebox.showinfo(
            "Graphs and frequencies cleared",
            "Graphs and frequencies have been cleared. You can now plot new simulations."
        )

    def calculate_frequencies(self, results):
        """
        Calculates the frequency of dice rolls.
        """
        frequencies = {i: 0 for i in range(2, 13)}
        for result in results:
            if result in frequencies:
                frequencies[result] += 1
        return frequencies
    
    def display_frequencies(self, frequencies_dict):
        """
        Display frequencies of dice rolls in the GUI.
        """
        # Enable a text widget for editing
        self.text_freq.config(state=tk.NORMAL)
        if not self.overlay_choice.get():
            self.text_freq.delete("1.0", tk.END)
        
        if frequencies_dict:
            for dice_type, frequencies in frequencies_dict.items():
                self.text_freq.insert(tk.END, f"Frequencies for {dice_type}:\n")
                for number, frequency in sorted(frequencies.items()):
                    self.text_freq.insert(tk.END, f" {number}: {frequency}\n")
                self.text_freq.insert(tk.END, "\n") # Spacing between sections

        # Disable the text widget to prevent editing
        self.text_freq.config(state=tk.DISABLED)

    def start_simulation(self):
        """
        Starts the simulation and plots the results.
        """
        try:
            num_rolls = int(self.entry_rolls.get())
            if num_rolls <= 0:
                raise ValueError("Number of rolls must be positive.")
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: Please input a valid number of rolls.")
            return
        
        # Prevent plotting if overlays already exist
        if self.overlay_active:
            messagebox.showerror(
                "Clear required",
                "Please clear the graph before plotting again."
            )

        # Clear the graph unless the overlay option is checked
        if not self.overlay_choice.get():
            self.ax.clear()
            self.overlay_active = False # Reset overlay flag
            self.plotted_dice = set() # Clear the record of plotted dice types

        # Track which dice types have already been plotted
        if not hasattr(self, "plotted_dice"):
            self.plotted_dice = set()

        displayed_frequencies = {}

        # Run the simulations
        if self.dice_choice.get() == "Standard":
            if "Standard" not in self.plotted_dice:
                standard_results = simulate_rolls(roll_standard_dice, num_rolls)
                displayed_frequencies["Standard dice"] = self.calculate_frequencies(standard_results)
                plot_results(standard_results, "Standard dice", self.ax)
                self.plotted_dice.add("Standard")

            if self.overlay_choice.get():
                if "Balanced" not in self.plotted_dice:
                    balanced_queue = create_balanced_queue(EXPECTED_DIST_2_12)
                    balanced_results = simulate_rolls(roll_balanced_dice, num_rolls, balanced_queue)
                    displayed_frequencies["Balanced dice"] = self.calculate_frequencies(balanced_results)
                    plot_results(balanced_results, "Balanced dice", self.ax)
                    self.plotted_dice.add("Balanced")
                    self.overlay_active = True

        elif self.dice_choice.get() == "Balanced":
            if "Balanced" not in self.plotted_dice:
                balanced_queue = create_balanced_queue(EXPECTED_DIST_2_12)
                balanced_results = simulate_rolls(roll_balanced_dice, num_rolls, balanced_queue)
                displayed_frequencies["Balanced dice"] = self.calculate_frequencies(balanced_results)
                plot_results(balanced_results, "Balanced dice", self.ax)
                self.plotted_dice.add("Balanced")

            if self.overlay_choice.get():
                if "Standard" not in self.plotted_dice:
                    standard_results = simulate_rolls(roll_standard_dice, num_rolls)
                    displayed_frequencies["Standard dice"] = self.calculate_frequencies(standard_results)
                    plot_results(standard_results, "Standard dice", self.ax)
                    self.plotted_dice.add("Standard")
                    self.overlay_active = True

        # Display frequencies
        self.display_frequencies(displayed_frequencies)

        # Update the graph
        self.canvas.draw()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BalancedDiceGUI(root)
    root.mainloop()