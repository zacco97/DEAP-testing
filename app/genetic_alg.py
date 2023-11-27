from deap import base, creator, tools
import numpy as np
import random
import subprocess
import json
import pandas as pd


def create_individuals(df):
    size = 1        # sample size
    replace = True  # with replacement
    ind = df.loc[np.random.choice(df.index, size, replace), :].to_numpy()[0]
    return creator.Individual(ind)


def evaluate(individual, id):
    subprocess.call(["py", "app/func.py", f"{individual}", f"{id}"])
    f = open('saves/data.json', "r")
    data = json.loads(f.read())
    fitness = data["val"]
    return fitness,


def varAnd(population, toolbox, cxpb, mutpb):
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


def eaSimple_modified(population, toolbox, cxpb, mutpb, ngen, stats=None,
                      halloffame=None, logger=None):
   
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
        
    if halloffame is not None:
        halloffame.update(population)

    # record = stats.compile(population) if stats else {}
    # logbook.record(gen=0, nevals=len(invalid_ind), **record)
    
    if logger:
        logger.info({"gen":0, "nevals":len(invalid_ind), "hof":halloffame.items})
    
    # Begin the generational process
    df = pd.DataFrame([])
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if logger:
            logger.info({"gen":gen, "nevals":len(invalid_ind), "hof":halloffame.items})
        temp_df = pd.DataFrame({
            "gen":gen,
            "individuals":halloffame.items
        })
        df = pd.concat([df, temp_df])
        
    return population, df


def genetic_algorithm(df, population_size=20, num_bests=10, ngen=4, CXPB=0.2, MUTPB=0.2, logger=None, id=None):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", create_individuals, df)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, id)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)

    population = toolbox.population(n=population_size)

    hof = tools.HallOfFame(num_bests)
    population, df = eaSimple_modified(
        population, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=ngen, halloffame=hof, logger=logger)

    # Get the best individuals found.
    best_individuals = hof.items

    # Return the best individuals.
    return best_individuals, df
