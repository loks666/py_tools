import random
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms

num_gates = 96

model_a_data = pd.read_csv('a.csv')
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(model_a_data)), len(model_a_data))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def fitness(individual):
    score = sum(1 for i in individual if model_a_data.loc[i, '机位位置（靠桥1非靠桥2）'] == '近1')
    return (score,)


toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population_size = 100
crossover_prob = 0.7
mutation_prob = 0.2
generations = 50

pop = toolbox.population(n=population_size)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)
stats.register("max", np.max)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=crossover_prob, mutpb=mutation_prob, ngen=generations, stats=stats,
                               halloffame=hof, verbose=True)

fitness_values = log.select("max")
plt.figure()
plt.plot(fitness_values, color='red')
plt.xlabel('Generation')
plt.ylabel('Max Fitness')
plt.title('Max Fitness over Generations for Model A')
plt.grid(True)
plt.savefig('a_fitness.png')
plt.show()


def plot_gantt_chart(data, best_individual):
    gate_schedule = {i: [] for i in range(num_gates)}
    for idx, gate in enumerate(best_individual):
        flight = data.iloc[idx]
        arrival = datetime.strptime(flight['计划到港时间'], '%H:%M')
        departure = datetime.strptime(flight['计划离港时间'], '%H:%M')
        gate_schedule[gate].append((arrival, departure, 'Flight ' + str(flight['航班序号'])))

    fig, ax = plt.subplots(figsize=(60, 32))
    yticks = []
    yticklabels = []
    for gate, schedules in gate_schedule.items():
        for schedule in schedules:
            start = mdates.date2num(schedule[0])
            end = mdates.date2num(schedule[1])
            width = end - start
            ax.barh(gate, width, left=start, height=0.4, align='center', edgecolor='black', color='skyblue')
            yticks.append(gate)
            yticklabels.append(schedule[2])

    ax.set_yticks(list(range(num_gates)))
    ax.set_yticklabels(list(range(num_gates)))
    ax.set_xlabel('Time')
    ax.set_ylabel('Gate')
    ax.set_title('Gate Allocation Gantt Chart')
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.savefig('a_gantt.png')
    plt.show()


best_individual = hof.items[0] if hof.items else None
if best_individual:
    plot_gantt_chart(model_a_data, best_individual)
