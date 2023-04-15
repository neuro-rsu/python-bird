# python bird

## Game "Bird in a cage"

## Description and purpose

* In this game, bird sprites, divided by 10 in height, move across the screen in a horizontal direction.
* When colliding with the walls of the playing space, the birds are removed from the screen.
* The goal of the game is to teach the birds to roll over in front of the walls and increase their lifespan accordingly.

## Machine learning

The learning process of the game is based on the use of a neural network with a single-layer perceptron architecture. To obtain the result, reinforcement learning and a genetic mutation algorithm are used.

### How to train a neural network

Each bird has its own neural network with topology (2, 2). The distance between the bird and the corresponding wall is fed to the first neuron of the input layer, the second neuron is the bias. The ReLU(x) function is used as an activation function, and the signals of two neurons are compared at the output. If the second signal exceeds the first, then the bird flips in the opposite direction.

When creating a new population, the weights of the neural networks of birds are cloned each time from the "best brain", which is the neural network of the bird that scored the most points at the previous stage. In addition, the weights of each neural network are mutated with a certain probability (usually 40%), which allows adding variability to the birds to improve the solution.

The proposed method makes it possible to complete training in a finite time.
