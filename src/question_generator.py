import random

def generate_math_question(attacker, target, damage, categories):
    
    # Get some random numbers
    a1 = random.randint(1,10)
    a2 = random.randint(1,10)
    tt1 = random.randint(1, 12)
    tt2 = random.randint(1, 12)
    
    questions = {
        "Carson": [
            (f"What is {a1} + {a2}?", a1 + a2),
            (f"What is {a1 + a2} - {a1}?", a2)
        ],
        "add_sub": [
            (f"{attacker.name} dealt {damage} damage to {target.name}. "
             f"How much health does {target.name} have now?", target.health),
            (f"What is {a1} + {a2} + {tt1}?", a1 + a2 + tt1),
            (f"What is {a1 * a2} + {tt1 * tt2}?", a1*a2 + tt1*tt2),
            (f"What is {a1 +a2 + tt1 + tt2} - {tt1 +tt2}?", a1 + a2)

        ],
        "percentage": [
            (f"Now with only {target.health} health remaining, what percentage of {target.name}'s original {target.original_health} health remains?", 
             (target.health / target.original_health) * 100)
        ],
        "mul_div": [
            (f"What is {tt1} x { tt2}?", tt1 * tt2)
        ]
    }
    
    if damage != 0:  # Avoid division by zero
        attacks_needed = -(-target.health // damage)  # Ceiling division
        questions["mul_div"].append(
            (f"If each attack deals {damage} damage, how many more attacks are needed to defeat {target.name} with {target.health} health?",
             attacks_needed)
        )
    
    # Filter questions based on selected categories
    available_questions = [q for cat in categories for q in questions[cat]]
    
    return random.choice(available_questions)
