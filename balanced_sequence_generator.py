# Python script to generate a homogeneous set of sequences, where the transition probability is balanced between all possible transitions.
#
# Inputs:
# - Size of each sequence (N)
# - Number of sequences to generate (M)
#
# Outputs:
# - The M generated sequences of size N
#     - CSV file
# - The Transition Probability Matrix of the generated sequences (N x N)
#     - CSV file
#     - Image file (heatmap)
#
# Markov-based method
# The method used to generate the sequences is based on a transition matrix (similar to a markov chain), whose lines represent the 'current element', and the columns represent the 'next element'. The value of each cell represent the number of times that the transition from the current element to the next element has been made.
#
# Constraints
# Repetition of elements are not allowed, therefore it is expected that the diagonal of the resulting transition matrix is filled with zeros. 
#
# The algorithm
# 1. Initialize the transition matrix with random noise (small values between 0 and 1)
# 2. Search for the minimum value in the transition matrix (its row is the first element of the sequence, and its column is the second element of the sequence) - note that the elements on the diagonal are ignored.
# 3. Increment the value of that cell in the transition matrix _(actually we round up the value to the next integer and add a small random value between 0 and 1, in order to generate variability in the next iteration)_
# 4. Find the smallest value of the line of the last element of the sequence _(its column is the next element of the sequence)_ - note that the elements on the diagonal are ignored.
# 5. Repeat steps 3 and 4 until the sequence is complete (reached lenght N)
# 6. Repeat steps 2 to 5 until all sequences are generated (reached lenght M)
# 7. Calculate the _real_ transition probability matrix from the generated sequences (where the values represent the probability of the transition)
# 8. Save the generated sequences in a CSV file
# 9. Save the transition probability matrix in a CSV file
# 10. Save the transition probability matrix in an image file (heatmap)
#
# Usage
# ```
# python3 balanced_sequence_generator.py <size of each sequence> <number of sequences> <name of the subfolder where the files will be stored>
# ```
#
# Example
# ```
# python3 balanced_sequence_generator.py 12 72 example
# ```
#
# Results
# - example/sequences.csv
# - example/sequences_transition_matrix.csv
# - example/sequences_transition_matrix.png

from math import ceil
import random
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

# Function to initialize a Markov chain, represented by a square matrix of size N.
# The numpy Markov chain is initialized with random values between 0 and 1, the diagonal is filled with zeros. 
def initialize_markov_chain(N):
    markov_chain = np.random.rand(N, N)
    np.fill_diagonal(markov_chain, 0)
    return markov_chain

# Function to generate a sequence of size N, based on a Markov chain.
# The minimal values of the Markov chain are used to determine the next element of the sequence.
# The Markov chain is updated after each element is added to the sequence.
def generate_sequence(N, markov_chain):
    sequence = []
    # Find the first and second element of the sequence, corresponding to the coordinates of the minimum value of the Markov chain (the diagonal is ignored)
    min_value = np.min(markov_chain[np.nonzero(markov_chain)])
    min_value_coordinates = np.argwhere(markov_chain == min_value)[0]
    sequence.append(min_value_coordinates[0])
    sequence.append(min_value_coordinates[1])
    # Update the Markov chain
    markov_chain[min_value_coordinates[0], min_value_coordinates[1]] = ceil(markov_chain[min_value_coordinates[0], min_value_coordinates[1]]) + random.random()
    # Find the next elements of the sequence, corresponding to the coordinates of the minimum value of the line corresponding to the last element of the sequence. The diagonal is ignored and repeated elements are not allowed.
    for i in range(2, N):
        min_value = np.min(markov_chain[sequence[i-1], np.nonzero(markov_chain[sequence[i-1]])])
        min_value_coordinates = np.argwhere(markov_chain[sequence[i-1]] == min_value)[0]
        sequence.append(min_value_coordinates[0])
        markov_chain[sequence[i-1], min_value_coordinates[0]] = ceil(markov_chain[sequence[i-1], min_value_coordinates[0]]) + random.random()
    return sequence

# Function to generate M sequences of size N, based on a Markov chain.
# The Markov chain is updated after each sequence is generated.
def generate_sequences(N, M, markov_chain):
    sequences = []
    for i in range(M):
        sequences.append(generate_sequence(N, markov_chain))
    return sequences

# Function to calculate the transition probability matrix from a set of sequences.
# The transition probability matrix is a square matrix of size N, where the value of each cell represents the probability of the transition from the current element to the next element.
def calculate_transition_probability_matrix(sequences):
    N = len(sequences[0])
    transition_probability_matrix = np.zeros((N, N))
    for sequence in sequences:
        for i in range(N-1):
            transition_probability_matrix[sequence[i], sequence[i+1]] += 1
    for i in range(N):
        transition_probability_matrix[i] = transition_probability_matrix[i] / np.sum(transition_probability_matrix[i])
    return transition_probability_matrix

# Function to save a set of sequences in a CSV file.
def save_sequences(sequences, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sequence in sequences:
            writer.writerow(sequence)

# Function to save a transition probability matrix in a CSV file.
def save_transition_probability_matrix(transition_probability_matrix, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in transition_probability_matrix:
            writer.writerow(row)

# Function to save a transition probability matrix in an image file (heatmap).
def save_transition_probability_matrix_image(transition_probability_matrix, filename):
    plt.imshow(transition_probability_matrix, cmap='hot', interpolation='nearest')
    plt.xlabel('Next element')
    plt.ylabel('Current element')
    plt.title('Transition probability matrix')
    plt.colorbar()
    plt.savefig(filename)

# Function to create a subfolder if it does not exist.
def create_subfolder(subfolder):
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

# Function to generate a set of balanced sequences.
def generate_balanced_sequences(N, M, subfolder):
    # Initialize the Markov chain
    markov_chain = initialize_markov_chain(N)
    # Generate the sequences
    sequences = generate_sequences(N, M, markov_chain)
    # Calculate the transition probability matrix
    transition_probability_matrix = calculate_transition_probability_matrix(sequences)
    # Save the sequences
    create_subfolder(subfolder)
    save_sequences(sequences, subfolder + '/sequences.csv')
    # Save the transition probability matrix
    save_transition_probability_matrix(transition_probability_matrix, subfolder + '/sequences_transition_matrix.csv')
    # Save the transition probability matrix in an image file (heatmap)
    save_transition_probability_matrix_image(transition_probability_matrix, subfolder + '/sequences_transition_matrix.png')

# Main function
def main():
    # Get the arguments
    N = int(sys.argv[1])
    M = int(sys.argv[2])
    subfolder = sys.argv[3]
    # Generate the balanced sequences
    generate_balanced_sequences(N, M, subfolder)

if __name__ == "__main__":
    main()
