import re
import string
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
input_number = 6
file_address = "Q4\\input"+str(input_number)+".txt"
f = open(file_address, 'r')
lenght_of_DNA = int(f.readline())
size_of_population = int(f.readline())
exponential = 2.5
states = []
n_iteration = int(f.readline())
nucleotides = list(f.readline().split())
constraints = dict()
can_be_fitness_more_than_1 = False
for line in f:
    c = line.split()
    constraints[c[0]] = int(c[1])
    if(constraints[c[0]]) > 1:
        can_be_fitness_more_than_1 = True
if can_be_fitness_more_than_1:
    size_of_population = 2*size_of_population
    exponential = 1.3
f.close()
for i in range(size_of_population):
    states.append(''.join(random.choice(nucleotides) for _ in range(lenght_of_DNA)))
def fitness():
    fitness_amount = []
    maximum = -np.inf
    best_string = None
    for dna_string in states:
        temp = 0
        for key, value in constraints.items():
            temp += len(re.findall(str(key), (dna_string)))*value
        if temp > maximum:
            maximum = temp
            temp = 0 if temp < 0 else temp
            best_string = dna_string
        fitness_amount.append(exponential**temp)
    return fitness_amount,maximum,best_string
best_fitness_arr = []
best_string_fitness = None
#startting time
starting_time = datetime.now()
current_time = starting_time.strftime("%H:%M:%S")
print("start time =", current_time)

for i in range(n_iteration):
    fitness_amount,maximum,best_string = fitness()
    best_fitness_arr.append(maximum)
    best_string_fitness = best_string
    #selection
    states = random.choices(states,fitness_amount ,cum_weights=None, k=size_of_population)
    #cross over
    for i in range(0,size_of_population, 2):
        first_state,second_state =states[i] ,states[i+1]
        random_index = random.randint(0, lenght_of_DNA - 1)
        temp1 = first_state[:random_index]+second_state[random_index:]
        temp2 = second_state[:random_index]+first_state[random_index:]
        states[i],states[i+1] = temp1,temp2
    # mutation
    for i in range(size_of_population):
        if random.random() <= 0.01:
            temp = list( states[i])
            temp[random.randint(0, lenght_of_DNA - 1)] = random.choice(nucleotides)
            states[i] = ''.join(temp)
#finishing time
finish_time = datetime.now()
current_time = finish_time.strftime("%H:%M:%S")
print("finish time =", current_time)
print(str(best_fitness_arr[len(best_fitness_arr)-1]))

f = open("A"+str(input_number)+".txt", "w")
f.write(best_string_fitness +"\n"+"fitness : "+str(best_fitness_arr[len(best_fitness_arr)-1]) + "\n"+
        "time : "+str(finish_time - starting_time))
f.close()
plt.title("test "+str(input_number))
plt.scatter(range(1, n_iteration+1), best_fitness_arr)
plt.savefig("A"+str(input_number)+".png")




