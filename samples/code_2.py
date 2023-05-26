import numpy as np

def initialize_population(population_size, num_genes):
    """Initialize the population of chromosomes
    
    Parameters:
        population_size (int): The number of chromosomes in the population
        num_genes (int): The number of genes in each chromosome
        
    Returns:
        population (ndarray): An array of shape (population_size, num_genes) representing the population
    """
    population = np.random.randint(2, size=(population_size, num_genes))
    return population


def calculate_fitness(chromosome):
    """Calculate the fitness of a single chromosome.
    
    Parameters:
        chromosome (ndarray): An array of shape (num_genes,) representing the chromosome
        
    Returns:
        fitness (float): The fitness of the chromosome
    """
    # Fitness Function
    # Here we are trying to maximize the number of ones in the chromosome
    fitness = np.sum(chromosome)
    return fitness


def selection(population, fitness):
    """Select the two best chromosomes for the next generation
    
    Parameters:
        population (ndarray): An array of shape (population_size, num_genes) representing the population
        fitness (ndarray): An array of shape (population_size,) representing the fitness of each chromosome
        
    Returns:
        parents (ndarray): An array of shape (2, num_genes) representing the selected parents
    """
    # Select the two best chromosomes to be parents
    best_chromosome_indices = np.argsort(fitness)[-2:]
    parents = population[best_chromosome_indices]
    return parents


def crossover(parents):
    """Crossover the genes of the selected parents
    
    Parameters:
        parents (ndarray): An array of shape (2, num_genes) representing the selected parents
        
    Returns:
        offspring (ndarray): An array of shape (2, num_genes) representing the offspring
    """
    # Crossover the genes of the selected parents
    offspring = np.zeros_like(parents)
    crossover_point = np.random.randint(1, parents.shape[1] - 1)
    offspring[0, :crossover_point] = parents[0, :crossover_point]
    offspring[0, crossover_point:] = parents[1, crossover_point:]
    offspring[1, :crossover_point] = parents[1, :crossover_point]
    offspring[1, crossover_point:] = parents[0, crossover_point:]
    return offspring


def mutation(offspring):
    """Mutate the offspring
    
    Parameters:
        offspring (ndarray): An array of shape (population_size, num_genes) representing the offspring
        
    Returns:
        mutated_offspring (ndarray): An array of shape (population_size, num_genes) representing the mutated offspring
    """
    # Flip the bits of the offspring with probability 1/num_genes
    mutated_offspring = np.copy(offspring)
    prob_gene_mutate = 1 / offspring.shape[1]
    for gene in range(offspring.shape[1]):
        if np.random.uniform(0, 1) <= prob_gene_mutate:
            mutated_offspring[:, gene] = 1 - offspring[:, gene]
    return mutated_offspring


def genetic_algorithm(population_size, num_genes, max_generations):
    """Create a genetic algorithm to maximize the given fitness function
    
    Parameters:
        population_size (int): The number of chromosomes in the population
        num_genes (int): The number of genes in each chromosome
        max_generations (int): The number of generations the algorithm creates
        
    Returns:
        best_fitness (float): The fitness of the best individual
    """
    # Initialize the population
    population = initialize_population(population_size, num_genes)

    # Run the genetic algorithm for the specified number of generations
    for generation in range(max_generations):
        # Calculate the fitness of each chromosome
        fitness = np.apply_along_axis(calculate_fitness, axis=1, arr=population)

        # Select the best chromosomes for the next generation
        parents = selection(population, fitness)

        # Crossover the genes of the selected parents
        offspring = crossover(parents)

        # Mutate the offspring
        offspring = mutation(offspring)

        # Replace the previous generation with the new generation
        population[-2:] = offspring

    # Return the fitness of the best individual
    return np.max(np.apply_along_axis(calculate_fitness, axis=1, arr=population))


# Example function call 1
best_fitness_1 = genetic_algorithm(20, 6, 150)
print("Best fitness for function call 1:", best_fitness_1)

# Example function call 2
best_fitness_2 = genetic_algorithm(50, 8, 300)
print("Best fitness for function call 2:", best_fitness_2)
