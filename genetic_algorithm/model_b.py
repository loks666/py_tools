import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms

data = pd.read_csv('b.csv')


def expand_rows(data):
    expanded_rows = []
    for _, row in data.iterrows():
        gate_ids = row['停机位编号']
        if '—' in gate_ids:
            start, end = map(int, gate_ids.split('—'))
            for i in range(start, end + 1):
                expanded_rows.append({'停机位编号': i, '滑行距离（KM）': row['滑行距离（KM）'],
                                      '机位远近分类': row['机位远近分类'], '机位尺寸分类': row['机位尺寸分类']})
        elif '、' in gate_ids:
            for i in map(int, gate_ids.split('、')):
                expanded_rows.append({'停机位编号': i, '滑行距离（KM）': row['滑行距离（KM）'],
                                      '机位远近分类': row['机位远近分类'], '机位尺寸分类': row['机位尺寸分类']})
        else:
            expanded_rows.append({'停机位编号': int(gate_ids), '滑行距离（KM）': row['滑行距离（KM）'],
                                  '机位远近分类': row['机位远近分类'], '机位尺寸分类': row['机位尺寸分类']})
    return pd.DataFrame(expanded_rows)


expanded_data = expand_rows(data)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
num_gates = expanded_data.shape[0]


def evaluate(individual):
    total_distance = sum(expanded_data.iloc[ind]['滑行距离（KM）'] for ind in individual)
    return total_distance,


toolbox.register("evaluate", evaluate)
toolbox.register("attr_int", random.randint, 0, num_gates - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=num_gates)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

stats = tools.Statistics(lambda ind: ind.fitness.values[0])  # 这里取元组的第一个元素，即适应度值
stats.register("min", np.min)

population = toolbox.population(n=50)
ngen = 40
result = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, stats=stats, verbose=True)

best_individual = tools.selBest(population, 1)[0]
logbook = result[1]
best_fitness = evaluate(best_individual)
print("Best individual is:", best_individual)
print("With fitness:", best_fitness)


def plot_gantt_chart(individual):
    fig, ax = plt.subplots(figsize=(60, 30))
    for i, gene in enumerate(individual):
        ax.broken_barh([(i, 0.8)], (gene, 1), facecolors='tab:blue')
    ax.set_yticks([g + 0.5 for g in range(num_gates)])
    ax.set_yticklabels(range(1, num_gates + 1))
    ax.set_xlabel('Flights')
    ax.set_ylabel('Gates')
    ax.set_title('Gantt Chart of Flight Gate Assignments')
    plt.savefig('b_gantt.jpeg', format='jpeg')
    plt.show()


plot_gantt_chart(best_individual)


def plot_iterations(logbook):
    gen = logbook.select("gen")
    fit_mins = logbook.select("min")
    if len(gen) == len(fit_mins):
        fig, ax1 = plt.subplots()
        line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness", color="b")
        ax1.tick_params(axis='y', labelcolor="b")
        ax1.set_title("Fitness over Generations")
        plt.savefig('b_fitness.jpeg', format='jpeg')
        plt.show()
    else:
        print("Error: Generation and fitness data lengths do not match.")


plot_iterations(logbook)
