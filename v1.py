import itertools
import random
import csv
from boolean import Symbol, AND, OR, NOT

# Define our own Implies function since it's not available in the boolean module
def Implies(a, b):
    return OR(NOT(a), b)

# Function to convert boolean expressions to natural language
def expr_to_natural_language(expr):
    """Convert a boolean expression to natural language format themed around Clue."""
    if isinstance(expr, Symbol):
        var_name = str(expr.obj)
        if var_name.startswith('A'):
            character = character_names[var_name]
            return f"the murderer was {character},"
        elif var_name.startswith('B'):
            location = location_names[var_name]
            return f"the murder happened in {location},"
        elif var_name.startswith('C'):
            weapon = weapon_names[var_name]
            return f"{weapon} was the murder weapon,"
        return str(expr.obj)
    
    elif expr.__class__.__name__ == 'NOT':
        # NOT operation
        inner_expr = expr.args[0]
        var_name = str(inner_expr.obj) if isinstance(inner_expr, Symbol) else None
        
        if isinstance(inner_expr, Symbol):
            if var_name.startswith('A'):
                character = character_names[var_name]
                return f"the murderer was not {character},"
            elif var_name.startswith('B'):
                location = location_names[var_name]
                return f"the murder did not happen in {location},"
            elif var_name.startswith('C'):
                weapon = weapon_names[var_name]
                return f"{weapon} was not the murder weapon,"
        
        # Fall back to general case
        inner_text = expr_to_natural_language(inner_expr)
        # Remove comma if it's at the end of inner_text
        if inner_text.endswith(','):
            inner_text = inner_text[:-1]
        return f"NOT ({inner_text}),"
    
    elif expr.__class__.__name__ == 'AND':
        # AND operation
        terms = []
        for arg in expr.args:
            term = expr_to_natural_language(arg)
            # Remove comma if present
            if term.endswith(','):
                term = term[:-1]
            terms.append(term)
        return f"({' AND '.join(terms)}),"
    
    elif expr.__class__.__name__ == 'OR':
        # OR operation
        terms = []
        for arg in expr.args:
            term = expr_to_natural_language(arg)
            # Remove comma if present
            if term.endswith(','):
                term = term[:-1]
            terms.append(term)
        return f"({' OR '.join(terms)}),"
    
    # For our custom Implies function
    elif isinstance(expr, OR) and len(expr.args) == 2 and isinstance(expr.args[0], NOT):
        # This is our Implies function: OR(NOT(a), b)
        # Extract the first argument (the antecedent) which is inside the NOT
        antecedent = expr_to_natural_language(expr.args[0].args[0])
        # Remove comma if present
        if antecedent.endswith(','):
            antecedent = antecedent[:-1]
        
        # Extract the second argument (the consequent)
        consequent = expr_to_natural_language(expr.args[1])
        # Remove comma if present
        if consequent.endswith(','):
            consequent = consequent[:-1]
        
        return f"(IF {antecedent} THEN {consequent}),"
    
    # Other operations as needed
    else:
        # For any other type of expression
        return str(expr)

# Initialize all variables
variables = {
    # A variables are characters
    'A1': Symbol('A1'), 'A2': Symbol('A2'), 'A3': Symbol('A3'),
    # B variables are locations
    'B1': Symbol('B1'), 'B2': Symbol('B2'), 'B3': Symbol('B3'),
    # C variables are weapons
    'C1': Symbol('C1'), 'C2': Symbol('C2'), 'C3': Symbol('C3')
}

# Define the names for better natural language expression
character_names = {
    'A1': 'Professor Plum',
    'A2': 'Colonel Mustard',
    'A3': 'Mrs. Peacock'
}

location_names = {
    'B1': 'the Kitchen',
    'B2': 'the Library',
    'B3': 'the Conservatory'
}

weapon_names = {
    'C1': 'the Knife',
    'C2': 'the Revolver',
    'C3': 'the Candlestick'
}

def print_assignment(assignment):
    """Helper function to print truth assignments in a readable format"""
    # Find the true character (murderer)
    murderer = None
    for i in range(1, 4):
        if assignment[f'A{i}']:
            murderer = character_names[f'A{i}']
    
    # Find the true location (crime scene)
    crime_scene = None
    for i in range(1, 4):
        if assignment[f'B{i}']:
            crime_scene = location_names[f'B{i}']
    
    # Find the true weapon
    murder_weapon = None
    for i in range(1, 4):
        if assignment[f'C{i}']:
            murder_weapon = weapon_names[f'C{i}']
    
    print(f"🔍 The murder was committed by {murderer} in {crime_scene} with {murder_weapon}.")
    
    # Also print the raw assignment values for debugging
    print("\nDetailed assignment values:")
    print("Characters:  ", end="")
    for i in range(1, 4):
        var = f'A{i}'
        val = assignment[var]
        name = character_names[var]
        print(f"{name}={'✓' if val else '✗'}  ", end="")
    
    print("\nLocations:   ", end="")
    for i in range(1, 4):
        var = f'B{i}'
        val = assignment[var]
        name = location_names[var]
        print(f"{name}={'✓' if val else '✗'}  ", end="")
    
    print("\nWeapons:     ", end="")
    for i in range(1, 4):
        var = f'C{i}'
        val = assignment[var]
        name = weapon_names[var]
        print(f"{name}={'✓' if val else '✗'}  ", end="")
    print()

# Setup the truth values - in each column, only one variable is True (1)
possible_assignments = []

# Generate all possible combinations where one variable per column is True
for a_idx in range(1, 4):
    for b_idx in range(1, 4):
        for c_idx in range(1, 4):
            assignment = {}
            # Set all variables to False initially
            for var in variables.keys():
                assignment[var] = False
            
            # Set one variable in each column to True
            assignment[f'A{a_idx}'] = True
            assignment[f'B{b_idx}'] = True
            assignment[f'C{c_idx}'] = True
            
            possible_assignments.append(assignment)

# Pick one assignment as our "actual" solution to the murder
actual_assignment = random.choice(possible_assignments)

# Print the actual solution
print("="*60)
print("🔍 ACTUAL MURDER SOLUTION (HIDDEN FROM PLAYERS)")
print("="*60)
print_assignment(actual_assignment)
print("="*60)

def count_propositions(expr):
    """Count the number of propositions (variables) in an expression."""
    if isinstance(expr, Symbol):
        return 1
    elif expr.__class__.__name__ == 'NOT':
        return count_propositions(expr.args[0])
    elif expr.__class__.__name__ in ['AND', 'OR']:
        # Count propositions in each argument
        return sum(count_propositions(arg) for arg in expr.args)
    else:
        # For any other type, return 0
        return 0

def generate_random_expression(variables, actual_assignment, max_propositions=4, current_depth=0):
    """Generate a random boolean expression that evaluates to True under the actual assignment.
    Ensures no more than max_propositions variables are used."""
    # Different types of expressions to generate
    expression_types = [
        "direct",       # A variable is True/False
        "negation",     # NOT a variable
        "implication",  # One variable implies another
        "and",          # AND between two expressions
        "or"            # OR between two expressions
    ]
    
    # If we're at depth > 2, increase chances of simpler expressions
    if current_depth > 2:
        expression_types = ["direct", "direct", "negation", "negation", "implication"] + expression_types
    
    expr_type = random.choice(expression_types)
    
    if expr_type == "direct":
        # Pick a random variable
        var_name = random.choice(list(variables.keys()))
        var = variables[var_name]
        # If it's true in the actual assignment, return the variable, otherwise its negation
        return var if actual_assignment[var_name] else NOT(var)
    
    elif expr_type == "negation":
        # Pick a random variable
        var_name = random.choice(list(variables.keys()))
        var = variables[var_name]
        # If it's false in the actual assignment, return NOT(var), otherwise var
        return NOT(var) if not actual_assignment[var_name] else var
    
    elif expr_type == "implication":
        # Pick two random variables
        var1_name, var2_name = random.sample(list(variables.keys()), 2)
        var1, var2 = variables[var1_name], variables[var2_name]
        
        # Determine if var1 => var2 is true under the assignment
        if not actual_assignment[var1_name] or actual_assignment[var2_name]:
            # var1 => var2 is true (when var1 is false or var2 is true)
            return Implies(var1, var2)
        else:
            # var1 => var2 is false, so we need to modify it
            # We can use NOT(var1) => var2 instead if that works
            if not actual_assignment[var1_name] or actual_assignment[var2_name]:
                return Implies(NOT(var1), var2)
            # Or try var1 => NOT(var2)
            elif not actual_assignment[var1_name] or not actual_assignment[var2_name]:
                return Implies(var1, NOT(var2))
            # Or try NOT(var1) => NOT(var2)
            else:
                return Implies(NOT(var1), NOT(var2))
    
    elif expr_type == "and":
        # Generate two sub-expressions that evaluate to True, but ensure we don't exceed max_propositions
        # We'll allocate propositions for each branch proportionally
        max_props_per_branch = max(1, max_propositions // 2)
        
        expr1 = generate_random_expression(variables, actual_assignment, max_props_per_branch, current_depth + 1)
        props_used = count_propositions(expr1)
        remaining_props = max(1, max_propositions - props_used)
        
        expr2 = generate_random_expression(variables, actual_assignment, remaining_props, current_depth + 1)
        
        # Check if the combined expression exceeds max_propositions
        combined_expr = AND(expr1, expr2)
        if count_propositions(combined_expr) > max_propositions:
            # If it does, just return one of the sub-expressions
            return expr1
        return combined_expr
    
    elif expr_type == "or":
        # Generate sub-expressions similar to AND case
        max_props_per_branch = max(1, max_propositions // 2)
        
        expr1 = generate_random_expression(variables, actual_assignment, max_props_per_branch, current_depth + 1)
        props_used = count_propositions(expr1)
        remaining_props = max(1, max_propositions - props_used)
        
        # For the second expression, we can either generate one that's True or False
        if random.choice([True, False]):
            expr2 = generate_random_expression(variables, actual_assignment, remaining_props, current_depth + 1)
        else:
            # Generate a likely False expression (opposite of a True one)
            true_expr = generate_random_expression(variables, actual_assignment, remaining_props, current_depth + 1)
            expr2 = NOT(true_expr)
        
        # Check if the combined expression exceeds max_propositions
        combined_expr = OR(expr1, expr2)
        if count_propositions(combined_expr) > max_propositions:
            # If it does, just return one of the sub-expressions
            return expr1
        return combined_expr

# Generate 50 unique conditional statements
conditional_statements = []
for _ in range(50):
    # Generate a new expression that evaluates to True with max 4 propositions
    expr = generate_random_expression(variables, actual_assignment, max_propositions=4)
    
    # Convert to string for easier comparison to avoid duplicates
    expr_str = str(expr)
    
    # Check if this expression or a simplified version is already in our list
    if expr_str not in [str(e) for e in conditional_statements]:
        conditional_statements.append(expr)

# Print the conditional statements
print("="*60)
print("📜 WITNESS STATEMENTS AND CLUES")
print("="*60)
for i, expr in enumerate(conditional_statements, 1):
    natural_lang_expr = expr_to_natural_language(expr)
    print(f"{i:2d}. {natural_lang_expr}")
print()

# Write the statements to a CSV file in natural language format
with open('logical_statements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Statement Number', 'Logical Statement'])
    for i, expr in enumerate(conditional_statements, 1):
        natural_lang_expr = expr_to_natural_language(expr)
        writer.writerow([i, natural_lang_expr])

print("✅ Logical statements have been written to 'logical_statements.csv'")

# 3. Evaluate which combination of statements can determine the murderer, location, and weapon
def can_determine_truth_values(statements_subset, possible_assignments):
    """
    Check if a subset of statements can uniquely determine who committed the crime, where, and with what.
    Returns True if the statements can uniquely identify the actual assignment.
    """
    # Start with all possible assignments
    consistent_assignments = possible_assignments.copy()
    
    # Filter out assignments that don't satisfy all statements in the subset
    for assignment in list(possible_assignments):  # Create a copy to iterate over
        is_consistent = True
        for expr in statements_subset:
            # Manually evaluate the expression for this assignment
            result = evaluate_expression(expr, assignment)
            if not result:
                if assignment in consistent_assignments:
                    consistent_assignments.remove(assignment)
                is_consistent = False
                break
                
        # If we've already determined it's inconsistent, we can move on
        if not is_consistent:
            continue
    
    # If only one assignment is left, we've uniquely determined the murderer, location, and weapon
    return len(consistent_assignments) == 1, consistent_assignments

def evaluate_expression(expr, assignment):
    """
    Manually evaluate a boolean expression given an assignment of variable values.
    This avoids the issue with the boolean library's substitution mechanism.
    """
    if isinstance(expr, Symbol):
        var_name = expr.obj
        return assignment[var_name]
    
    elif expr.__class__.__name__ == 'NOT':
        # NOT operation
        return not evaluate_expression(expr.args[0], assignment)
    
    elif expr.__class__.__name__ == 'AND':
        # AND operation
        return all(evaluate_expression(arg, assignment) for arg in expr.args)
    
    elif expr.__class__.__name__ == 'OR':
        # OR operation
        return any(evaluate_expression(arg, assignment) for arg in expr.args)
    
    # For our custom Implies function
    elif isinstance(expr, OR) and len(expr.args) == 2 and isinstance(expr.args[0], NOT):
        # This is our Implies function: OR(NOT(a), b)
        # It's equivalent to: NOT a OR b
        return (not evaluate_expression(expr.args[0].args[0], assignment)) or evaluate_expression(expr.args[1], assignment)
    
    # Other operations as needed
    else:
        # For any other type of expression
        raise ValueError(f"Unsupported expression type: {type(expr)} - {expr}")

# New approach: reveal statements one by one
print("="*60)
print("🔍 CLUE: THE LOGICAL DEDUCTION MURDER MYSTERY GAME 🕵️")
print("="*60)
print("You have a murder to solve! Statements from witnesses will be revealed one by one.")
print("In each round, we'll check if the currently available statements")
print("are enough to determine who committed the crime, where, and with what weapon.\n")

# Shuffle the statements to reveal them in random order
random.shuffle(conditional_statements)

# Start with only 1 statement available
available_statements = []
determined = False
round_num = 0

# Continue revealing statements until we find a solution or run out of statements
while round_num < len(conditional_statements) and not determined:
    round_num += 1
    
    # Reveal one more statement
    available_statements.append(conditional_statements[round_num - 1])
    
    print("\n" + "-"*60)
    print(f"🔄 INVESTIGATION ROUND {round_num}")
    print("-"*60)
    print(f"Available witness testimonies ({len(available_statements)}):")
    for i, stmt in enumerate(available_statements, 1):
        natural_lang_stmt = expr_to_natural_language(stmt)
        print(f"{i:2d}. {natural_lang_stmt}")
    
    # Check all possible subsets of the available statements
    print("\nAnalyzing witness testimonies to solve the case...")
    
    determined_combinations = []
    all_combinations_checked = []
    
    # Generate all possible combinations of the available statements, starting from smaller sizes
    for r in range(1, len(available_statements) + 1):
        for subset in itertools.combinations(available_statements, r):
            # Skip any subset that contains an already found solution
            should_skip = False
            for found_size, found_subset, _ in determined_combinations:
                if all(stmt in subset for stmt in found_subset):
                    should_skip = True
                    break
            if should_skip:
                continue
                
            # Store the combination being checked
            combination_info = {
                'size': len(subset),
                'statements': subset,
                'indices': [available_statements.index(stmt) + 1 for stmt in subset]
            }
            all_combinations_checked.append(combination_info)
            
            success, remaining = can_determine_truth_values(subset, possible_assignments)
            if success:
                determined_combinations.append((len(subset), subset, remaining[0]))
    
    if determined_combinations:
        determined = True
        print("\n" + "*"*60)
        print("✅ SUCCESS! Found minimal combinations that can solve the murder case:")
        print("*"*60)
        
        # Sort solutions by size to show smallest first
        determined_combinations.sort(key=lambda x: x[0])
        
        # Show the successful combinations discovered
        for i, (size, subset, assignment) in enumerate(determined_combinations, 1):
            print(f"\n📋 Solution #{i}: {size} testimony/testimonies")
            print("-"*60)
            for stmt in subset:
                stmt_idx = available_statements.index(stmt) + 1
                natural_lang_stmt = expr_to_natural_language(stmt)
                print(f"  Testimony #{stmt_idx}: {natural_lang_stmt}")
            
            print("\n🔍 The murderer has been caught!")
            print_assignment(assignment)
        
        # Show all combinations that were checked
        print(f"\nTotal testimony combinations analyzed: {len(all_combinations_checked)}")
        print("\n📊 Sample of testimony combinations analyzed:")
        print("-"*60)
        for i, combo in enumerate(all_combinations_checked[:10], 1):
            print(f"{i:2d}. Size {combo['size']}, Testimony indices: {combo['indices']}")
        if len(all_combinations_checked) > 10:
            print(f"... and {len(all_combinations_checked)-10} more combinations")
    else:
        print("\n⏳ The case remains unsolved. We need more witness testimonies.")
        print(f"\nTotal testimony combinations analyzed this round: {len(all_combinations_checked)}")
        print("\n📊 Sample of testimony combinations analyzed this round:")
        print("-"*60)
        for i, combo in enumerate(all_combinations_checked[:10], 1):
            print(f"{i:2d}. Size {combo['size']}, Testimony indices: {combo['indices']}")
        if len(all_combinations_checked) > 10:
            print(f"... and {len(all_combinations_checked)-10} more combinations")

if not determined:
    print("\n❌ The case remains unsolved even after gathering all available testimonies.")