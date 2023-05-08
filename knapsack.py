# AUTHOR:
#
# Dylan
#
# PROBLEM:
#
# We want to collect the most valuable items into our bag (knapsack)
#
# SOLUTION:
#
# Use genetic algorithms to determine which items should be collected into the bag
#

# EXAMPLE:
#
#
# BAG:
#
#     [          ]
#     [          ]
#     [          ]
#     [          ]    can only hold 15kg
#
#
# BOXES:
#            Box 1           Box 2           Box 3           Box 4
#        [weight: 7kg]     [weight: 2kg]      [weight: 1kg]     [weight: 9kg]
#        [value:  $5 ]     [value:  $4]       [value:   $7]     [value:   $2]
#
#
# SOLUTION:
#
# We can define the solution as a 4-bit array where each bit corresponds to a box
#
# [0 1 1 0] -> Fits in bag: 3kg < 15kg -> Fitness function: 11$
# [1 1 0 1] -> Doesn't fit in bag 18kg > 15kg -> Fitness function: 0$
#
#
#
import numpy as np
import random

boxes = [
    {
        "weight": 7,
        "value": 5
    },
    {
        "weight": 2,
        "value": 4
    }, {
        "weight": 1,
        "value": 7
    }, {
        "weight": 9,
        "value": 2
    },
]

bagWeightLimit = 15

population = np.array([[0, 1, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [
    0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])

population_scores = [{"solution": population[0], "fitness_score": 0},
                     {"solution": population[1], "fitness_score": 0},
                     {"solution": population[2], "fitness_score": 0},
                     {"solution": population[3], "fitness_score": 0},
                     {"solution": population[4], "fitness_score": 0},
                     {"solution": population[5], "fitness_score": 0},
                     {"solution": population[6], "fitness_score": 0},
                     {"solution": population[7], "fitness_score": 0}]

# Best solution is: [1,1,1,0], fitness_score = 16
# population = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [
#                       0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0],
#     [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]])

initialSolution = {"solution": population[0], "fitness_score": 0}

bestSolution = initialSolution


def run_simulation(debug: False):
    global bestSolution
    global population_scores
    count = 0

    for i in population_scores:
        fitness = 0
        totalWeight = 0
        boxArray = i["solution"]

        for index, boxBit in enumerate(boxArray):
            boxWeight = boxes[index]['weight']
            boxValue = boxes[index]['value']

            totalWeight = totalWeight + (boxBit * boxWeight)
            fitness = fitness + (boxBit * boxValue)

            if totalWeight > bagWeightLimit:
                fitness = 0

            if debug:
                print(
                    f"index: {index}, box number: {boxBit}, weight: {boxWeight}, value: {boxValue}, current fitness: {fitness}, totalWeight {totalWeight}, box array: {boxArray}")

        newSolution = {"solution": boxArray, "fitness_score": fitness}

        if newSolution["fitness_score"] > bestSolution["fitness_score"]:
            # print(newSolution)
            bestSolution = newSolution.copy()

        population_scores[count] = newSolution
        count += 1

        if debug:
            print("__________________________________________________")


def roulette_wheel_selection():
    return False


def tournament_selection():
    # get 4 random parents
    parents = []

    global population_scores

    choiceArray = [0, 1, 2, 3, 4, 5, 6, 7]
    candidatePos = random.choice(choiceArray)
    choiceArray.remove(candidatePos)
    candidatePos1 = random.choice(choiceArray)
    choiceArray.remove(candidatePos1)
    candidatePos2 = random.choice(choiceArray)
    choiceArray.remove(candidatePos2)
    candidatePos3 = random.choice(choiceArray)

    if population_scores[candidatePos]["fitness_score"] > population_scores[candidatePos1]["fitness_score"]:
        parents.append(population_scores[candidatePos]["solution"])
    else:
        parents.append(population_scores[candidatePos1]["solution"])

    if population_scores[candidatePos2]["fitness_score"] > population_scores[candidatePos3]["fitness_score"]:
        parents.append(population_scores[candidatePos2]["solution"])
    else:
        parents.append(population_scores[candidatePos3]["solution"])

    return parents


def crossover(parents):
    parent1 = np.array(parents[0])
    parent2 = np.array(parents[1])

    crossover_point = len(parent1) // 2
    child1 = np.concatenate(
        (parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate(
        (parent2[:crossover_point], parent1[crossover_point:]))

    return [child1, child2]


def mutation(new_generation):
    mutation_rate = 2

    chance = random.randint(0, 100)

    if chance <= mutation_rate:
        mutate_index = random.randint(0, 7)
        current = new_generation[mutate_index].copy()
        bit_index = random.randint(0, 3)
        currentBit = current[bit_index]

        if currentBit == 0:
            current[bit_index] = 1
        else:
            current[bit_index] = 0

        new_generation[mutate_index] = current

    return new_generation


def reproduction():
    # this is inspired by nature
    # where evolutionary there is a very high chance
    # that the genes of the fittest individuals are passed as is to the next generation
    # e.g. 50% of population

    # find the four best solutions...

    global population_scores

    sorted_list = sorted(
        population_scores, key=lambda x: x['fitness_score'], reverse=True)

    children = [sorted_list[0]["solution"], sorted_list[1]["solution"],
                sorted_list[2]["solution"], sorted_list[3]["solution"]]

    return children


def generation_creation():
    # cross-over should be 50-70% of new population
    parents = tournament_selection()
    children = crossover(parents)
    # print(f"Cross-over 1: {children}")

    parents = tournament_selection()
    children2 = crossover(parents)
    # print(f"Cross-over 2: {children2}")

    # reproduction should be 50% of the new population
    children3 = reproduction()
    # print(f"Reproduction: {children3}")

    new_generation = children + children2 + children3

    new_generation = mutation(new_generation)

    return new_generation
    # print(f"\n\nNew generation: {new_generation}\n\n")


def print_population_scores():
    for i in population_scores:
        print(i)


def reset_population_scores(new_generation):
    global population_scores

    new_pop_scores = []
    for i in new_generation:
        new_pop_scores.append({
            "solution": i,
            "fitness_score": 0
        })

    population_scores = new_pop_scores


def simulation_loop(debug: False):
    generations = 10000
    count = 1
    while generations > 0:
        if debug:
            print("________________________________________")
            print(f"\n\nGeneration: {count} \n\n")
        run_simulation(debug)
        generations = generations - 1
        count += 1
        new_generation = generation_creation()
        reset_population_scores(new_generation)
    print_best_solution()


def print_best_solution():
    print(f"Best solution: {bestSolution}")


def start_simulation():
    debug = debug_prompt()
    simulation_loop(debug)
    # find_best_solution()


def debug_prompt():
    response = input("Would you like to run in debug mode? (y/n) ")

    if response.lower() == 'y':
        print("Debug mode enabled.\n")
        return True

    print("Debug mode disabled.\n")
    return False


start_simulation()
