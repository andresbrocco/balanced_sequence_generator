# Balanced Sequence Generator
Python script to generate a homogeneous set of sequences, where the transition probability is balanced between all possible transitions.

Inputs:
- Size of each sequence (N)
- Number of sequences to generate (M)

Outputs:
- The **M** generated sequences of size **N**
    - CSV file
- The Transition Probability Matrix of the generated sequences (N x N)
    - CSV file
    - Image file (heatmap)

## Markov-based method
I'm not aware that the method used is described in the literature, so I'll explain it here. _(and please contact me if you know of a similar method)_

The method used to generate the sequences is based on a transition matrix (similar to a markov chain), whose lines represent the 'current element', and the columns represent the 'next element'. The value of each cell represent the number of times that the transition from the current element to the next element has been made.

The idea is to iteratively generate the sequence and update the transition matrix accordingly on the go, so that the transition matrix is balanced at the end of the generation. The minimum value of a given row of the transition matrix gives us the next element to add to the sequence.

### Constraints
Repetition of elements are not allowed, therefore it is expected that the diagonal of the resulting transition matrix is filled with zeros. 

### The algorithm
1. Initialize the transition matrix with random noise (small values between 0 and 1)
2. Search for the minimum value in the transition matrix (its row is the first element of the sequence, and its column is the second element of the sequence) - note that the elements on the diagonal are ignored.
3. Increment the value of that cell in the transition matrix _(actually we round up the value to the next integer and add a small random value between 0 and 1, in order to generate variability in the next iteration)_
4. Find the smallest value of the line of the last element of the sequence _(its column is the next element of the sequence)_ - note that the elements on the diagonal are ignored.
5. Repeat steps 3 and 4 until the sequence is complete (reached lenght N)
6. Repeat steps 2 to 5 until all sequences are generated (reached lenght M)
7. Calculate the _real_ transition probability matrix from the generated sequences (where the values represent the probability of the transition)
8. Save the generated sequences and the transition probability matrix

## Usage
```
python3 balanced_sequence_generator.py <size of each sequence> <number of sequences> <name of the subfolder where the files will be stored>
```

## Example
```
python3 balanced_sequence_generator.py 12 72 example
```

### Results
- example/sequences.csv
- example/sequences_transition_matrix.csv
- example/sequences_transition_matrix.png


## Requirements
- Python 3
- Matplotlib
- Numpy

## Installation
1. Clone this repo (or download the files)
```bash
git clone git@github.com:andresbrocco/balanced_sequence_generator.git
```
2. Install the requirements
```bash
pip3 install -r requirements.txt
```

## License
MIT License
