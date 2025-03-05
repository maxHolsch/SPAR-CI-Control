Here's a concise and clear README for your project:

---

# 🔍 Clue: Logical Deduction Murder Mystery Game 🕵️

## Overview

This Python script simulates a logical deduction murder mystery game inspired by the classic board game "Clue." Players are presented with a series of logical statements (witness testimonies) and must deduce the murderer, the location of the crime, and the murder weapon.

## Features

- **Randomized Murder Scenario**: Each game randomly selects a murderer, location, and weapon.
- **Logical Statements Generation**: Automatically generates logical statements that are guaranteed to be true based on the actual murder scenario.
- **Natural Language Conversion**: Converts logical expressions into easy-to-understand natural language clues.
- **Incremental Deduction**: Reveals clues one by one, checking at each step if the available clues are sufficient to solve the mystery.
- **CSV Export**: Saves generated logical statements to a CSV file (`logical_statements.csv`) for external analysis or record-keeping.

## How to Run

1. **Install Dependencies**:

```bash
pip install boolean.py
```

2. **Run the Script**:

```bash
python v1.py
```

## Output

- **Console Output**: Displays the actual murder scenario (hidden from players), generated witness statements, and step-by-step deduction rounds.
- **CSV File**: `logical_statements.csv` containing all generated logical statements in natural language.

## Dependencies

- Python 3.x
- [boolean.py](https://pypi.org/project/boolean.py/)

## Example Output

```
🔍 ACTUAL MURDER SOLUTION (HIDDEN FROM PLAYERS)
============================================================
🔍 The murder was committed by Colonel Mustard in the Library with the Revolver.

📜 WITNESS STATEMENTS AND CLUES
============================================================
 1. (IF the murderer was Professor Plum THEN the murder weapon was not the Knife),
 2. (the murder did not happen in the Conservatory OR the murderer was Colonel Mustard),
 ...
✅ Logical statements have been written to 'logical_statements.csv'
```

Enjoy solving the mystery! 🕵️‍♂️
