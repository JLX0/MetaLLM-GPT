import numpy as np


class GeneticAlgorithm:
    """
    A genetic algorithm class.

    Parameters
    ----------
    population_size : int
        The size of the population.
    num_genes : int
        The number of genes in an individual.
    mutation_rate : float
        The probability of mutation.
    stop_fit : float or None, optional
        The fitness value at which the optimization stops. If None, the optimization runs for the specified number of
        generations.
    seed : int or None, optional
        The random seed used for the genetic algorithm.
    lower_bound : float or None, optional
        The lower bound for the genes of individuals. If None, defaults to 0.
    upper_bound : float or None, optional
        The upper bound for the genes of individuals. If None, defaults to 20.

    Attributes
    ----------
    population : ndarray
        A 2D array of shape `(population_size, num_genes)` that represents the population of individuals.
    best_individual : ndarray
        A 1D array of shape `(num_genes,)` that represents the best individual found by the genetic algorithm.
    best_fitness : float
        The fitness value of the best individual.
    """

    def __init__(self, population_size, num_genes, mutation_rate, stop_fit=None, seed=None, lower_bound=0, upper_bound=20):
        self.population_size = population_size
        self.num_genes = num_genes
        self.mutation_rate = mutation_rate
        self.stop_fit = stop_fit
        self.population = np.array([self.generate_individual(lower_bound, upper_bound) for _ in range(self.population_size)])
        self.best_individual = None
        self.best_fitness = None
        np.random.seed(seed)

    def generate_individual(self, lower_bound, upper_bound):
        """
        Generate a random individual using uniform distribution.

        Parameters
        ----------
        lower_bound : float
            The lower bound for the genes of the individual.
        upper_bound : float
            The upper bound for the genes of the individual.

        Returns
        -------
        ndarray
            A 1D array of shape `(num_genes,)` that represents an individual.
        """
        return np.random.uniform(lower_bound, upper_bound, size=self.num_genes)

    def fitness(self, individual):
        """
        Calculate the fitness of an individual. The objective of the function is to maximize the output of the function: f(x) = sum(x_i * sin(x_i)),
        where x is the input array and i is the index from 1 to n of the input array.

        Parameters
        ----------
        individual : ndarray
            A 1D array of shape `(num_genes,)` that represents an individual.

        Returns
        -------
        float
            The fitness value of the individual.
        """
        return np.sum(individual * np.sin(individual))

    def stochastic_universal_sampling(self, fitness_values, selection_size):
        total_fitness = np.sum(fitness_values)
        probabilities = fitness_values / total_fitness
        cumulative_probabilities = np.cumsum(probabilities)
        pointer_dist = total_fitness / selection_size
        start_at = np.random.uniform(0, pointer_dist)
        pointers = np.linspace(start_at, start_at + selection_size * pointer_dist, selection_size, endpoint=False)
        pointers += np.random.uniform(0, pointer_dist, size=pointers.shape)
        index = 0
        selected_indices = []
        for p in pointers:
            while cumulative_probabilities[index] < p:
                index += 1
            selected_indices.append(index)
        return self.population[selected_indices]

    def crossover(self, parents, children_size):
        children = np.zeros((children_size, self.num_genes))
        for i in range(children_size):
            parent1_idx = i % parents.shape[0]
            parent2_idx = (i + 1) % parents.shape[0]
            crossover_point = np.random.randint(1, self.num_genes - 1)
            children[i, :crossover_point] = parents[parent1_idx, :crossover_point]
            children[i, crossover_point:] = parents[parent2_idx, crossover_point:]
        return children

    def mutation(self, children):
        mutation_mask = np.random.random(size=children.shape) < self.mutation_rate
        mutation_array = np.random.uniform(low=-1, high=1, size=children.shape) * mutation_mask
        return children + mutation_array

    def run(self, max_generation):
        for generation in range(max_generation):
            # calculate fitness
            fitness_values = np.array([self.fitness(individual) for individual in self.population])

            # store the best individual
            best_individual_index = np.argmax(fitness_values)
            self.best_individual = self.population[best_individual_index].copy()
            self.best_fitness = fitness_values[best_individual_index]

            # check for solution
            if self.stop_fit is not None and self.best_fitness >= self.stop_fit:
                return self.best_fitness, self.best_individual

            # select individuals
            parents = self.stochastic_universal_sampling(fitness_values, self.population_size // 2)

            # crossover
            children_size = self.population_size - parents.shape[0]
            children = self.crossover(parents, children_size)

            # mutation
            mutated_children = self.mutation(children)

            # elitism - keep the best individual
            all_populations = np.concatenate((parents, mutated_children))
            all_fitness_values = np.array([self.fitness(individual) for individual in all_populations])
            elitism_index = np.argmax(all_fitness_values)
            self.population[0, :] = all_populations[elitism_index, :].copy()

            # update population
            self.population[1:, :] = all_populations[np.random.choice(
                np.arange(1, len(all_populations)), size=self.population.shape[0] - 1, replace=False), :]

        # store the best individual
        best_individual_index = np.argmax(np.array([self.fitness(individual) for individual in self.population]))
        self.best_individual = self.population[best_individual_index].copy()
        self.best_fitness = self.fitness(self.best_individual)

        return self.best_fitness, self.best_individual

# Example use of GeneticAlgorithm
ga = GeneticAlgorithm(50, 10, 0.01, 19, 100, 1)
best_fitness, best_individual = ga.run(ga.stop_fit)
print("Best individual:", best_individual)
print("Best fitness:", best_fitness)
