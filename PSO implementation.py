
import random
import math
import matplotlib.pyplot as plt
import time
from numpy.random import default_rng


def objective_function(O):
    x1_1_1= O[0]
    x1_1_2= O[1]
    x1_2_1= O[2]
    x1_2_2= O[3]
    x2_1_1= O[4]
    x2_1_2= O[5]
    x2_2_1= O[6]
    x2_2_2= O[7]
    D1_1=7
    D1_2=6
    D2_1=5
    D2_2=8
    nonlinear_constraint = x1_1_1+ x1_1_2
    nonlinear_constraint2= x1_2_1+ x1_2_2
    nonlinear_constraint3= x2_1_1+ x2_1_2
    nonlinear_constraint4= x2_2_1+ x2_2_2
    if nonlinear_constraint >= D1_1:
        penalty1 = 0
    else:
        penalty1 = 10000
  
    if nonlinear_constraint2 >= D1_2:
        penalty2 = 0
    else:
        penalty2 = 10000
   
    if nonlinear_constraint3 >= D2_1:
        penalty3 = 0
    else:
        penalty3 = 10000
    if nonlinear_constraint4 >= D2_2:
        penalty4 = 0
    else:
        penalty4 = 10000
    
    z = 10+3*(x1_1_1+x1_2_1+x2_1_1+x2_2_1)+ 10+3*(x1_1_2+x1_2_2+x2_1_2+x2_2_2)+ penalty1 + penalty2+penalty3+penalty4
    return z
  
bounds = [(1, 50), (1, 50),(1, 50),(1, 50),
          (1, 50),(1, 50),(1, 50),(1, 50)]  # upper and lower bounds of variables
nv =  8 # number of variables
mm = - 1  # if minimization problem, mm = -1; if maximization problem, mm = 1
  
# PARAMETERS OF PSO
particle_size = 500  # number of particles
iterations = 100  # max number of iterations
w = 0.8  # inertia constant
c1 = 2  # cognative constant
c2 = 0.5  # social constant
  
# Visualization
fig = plt.figure()
ax = fig.add_subplot()
fig.show()
plt.title('Evolutionary process of the objective function value')
plt.xlabel("Iteration")
plt.ylabel("Objective function")
# ------------------------------------------------------------------------------
class Particle:
    def __init__(self, bounds):
        self.particle_position = []  # particle position
        self.particle_velocity = []  # particle velocity
        self.local_best_particle_position = []  # best position of the particle
        self.fitness_local_best_particle_position=initial_fitness
        self.fitness_particle_position=initial_fitness

        for i in range(nv):
            self.particle_position.append(
                random.uniform(bounds[i][0],bounds[i][1]))
            self.particle_velocity.append(random.uniform(-1,1))
            
    def evaluate(self, objective_function):
        self.fitness_particle_position = objective_function(self.particle_position)
        if mm == -1:
            if self.fitness_particle_position < self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.fitness_local_best_particle_position = self.fitness_particle_position  # update the fitness of the local best
        if mm==1:
            if self.fitness_particle_position > self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.fitness_local_best_particle_position = self.fitness_particle_position  # 


  
    def update_velocity(self, global_best_particle_position):
        for i in range(nv):
            r1 = random.random()
            r2 = random.random()
  
            cognitive_velocity = c1 * r1 * (self.local_best_particle_position[i] - self.particle_position[i])
            social_velocity = c2 * r2 * (global_best_particle_position[i] - self.particle_position[i])
            self.particle_velocity[i] = w * self.particle_velocity[i] + cognitive_velocity + social_velocity
  
    def update_position(self, bounds):
        for i in range(nv):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]
  
            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > bounds[i][1]:
                self.particle_position[i] = bounds[i][1]
            # check and repair to satisfy the lower bounds
            if self.particle_position[i] < bounds[i][0]:
                self.particle_position[i] = bounds[i][0]
  
class PSO:
    def __init__(self, objective_function, bounds, particle_size, iterations):
        fitness_global_best_particle_position = initial_fitness
        global_best_particle_position = []
        swarm_particle = []
        for i in range(particle_size):
            swarm_particle.append(Particle(bounds))
        A=[]
          
        for i in range(iterations):
            for j in range(particle_size):
                swarm_particle[j].evaluate(objective_function)        
                
                if mm==-1:
                    if swarm_particle[j].fitness_particle_position < fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(swarm_particle[j].fitness_particle_position)

                if mm==1:
                    if swarm_particle[j].fitness_particle_position>fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position=float(swarm_particle[j].fitness_particle_position)
        
            for j in range(particle_size):
                swarm_particle[j].update_velocity(global_best_particle_position)
                swarm_particle[j].update_position(bounds)
                
            A.append(fitness_global_best_particle_position)
            
        print("Result:")
        print("Optimal solution:",global_best_particle_position)
        print("Objective function",fitness_global_best_particle_position)
        ax.plot(A,color="r")
        fig.canvas.draw()
        ax.set_xlim(left=max(0,i-iterations),right=i+3)
        time.sleep(0.01)

if mm==-1:
    initial_fitness=float("inf")
if mm==1:
    initial_fitness=-float("inf")

PSO(objective_function,bounds,particle_size,iterations)

plt.show()









