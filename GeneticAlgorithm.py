import math
import random

def convertToRGB(string):
    rString, gString, bString = string[0:8], string[8:16], string[16:] #variables holding 8 bits per color (r,g,b)
    rgbStrings = [rString, gString, bString] #list of each color's bit value
    if(type(string) is str): #if the input is a string
        rgbValues = [sum([math.pow(2, y) for y in range(len(x)) if x[-(y+1)] == '1']) for x in rgbStrings]
        #run backwards through the string and sum the values where there are 1 bits to convert from binary to base 10
    else:
        rgbValues = [sum([math.pow(2, y) for y in range(len(x)) if x[-(y+1)] == 1]) for x in rgbStrings]
        #do the same as above except when the input is not a string but a list of numbers
    return rgbValues

def getFitness(chromosomeRGB, targetRGB):
    return math.sqrt(math.pow((targetRGB[0] - chromosomeRGB[0]),2) + math.pow((targetRGB[1] - chromosomeRGB[1]),2) + math.pow((targetRGB[2] - chromosomeRGB[2]),2))
    #the 3-dimensional euclidean distance formula given in the homework

def generatePopulation(numChromosomes):
    i = 0
    population = []
    while i < numChromosomes: #to create each chromosome
        population.append([]) #append an empty list which will hold this chromosome's bit values
        for j in range(24): #for every bit in the chromosome
            if random.random() > 0.5: #if the random number is above .5 (to ensure equal probability of getting 1 or 0)
                population[i].append(1) #append a 1
            else: #otherwise
                population[i].append(0) #append a 0
        i+=1
    return population #return population: the list of chromosomes

def crossover(population, numCrossoverPairs):
    crossoverPairs = [] #a list of tuples that contains crossover pairs that have already been done
    i = 0
    while i < numCrossoverPairs: #for every pair of chromosomes to be crossed over
        chromeIndex1, chromeIndex2 = tournamentSelect(population), tournamentSelect(population)
        #make a variable with the index of each of the two randomely generated chromosomes indexes in population
        crossoverIndex = random.randint(0,23) #get the random crossover index where the chromosomes will cross over
        chromosome1, chromosome2 = population[chromeIndex1], population[chromeIndex2]
        #store each original chromosome in variables
        if (chromeIndex1, chromeIndex2) or (chromeIndex2, chromeIndex1) not in crossoverPairs:
            #if the randomely generated chromosome pair has not already been visited
            population[chromeIndex1] = chromosome1[:crossoverIndex+1] + chromosome2[crossoverIndex+1:]
            #switch the front of chromosome1 with that of chromosome2 depending on its crossover index
            population[chromeIndex2] = chromosome2[:crossoverIndex+1] + chromosome1[crossoverIndex+1:]
            #switch the front of chromosome2 with that of chromosome1 depending on its crossover index
            crossoverPairs.append((chromeIndex1, chromeIndex2)) #append the pair of indexes for chromosomes used in the crossover
            i+=1
    return population

def mutate(population, MUTATION_RATE, numMutation, indexsMutated):
    for i in range(numMutation): #for every chromosome to be mutated
        chromosomeNum = tournamentSelect(population) #get the randomely generated chromosome index to be mutated
        if(chromosomeNum not in indexsMutated):
            j = 0
            bitIndicesMutated = []
            indexsMutated.append(chromosomeNum)
            if MUTATION_RATE == 24:
                population[chromosomeNum] = generatePopulation(1)[0] #newBlood
            else:
                while j < MUTATION_RATE: #do the following depending on how many mutations per chromosome (number of bit changes)
                    mutationIndex = random.randint(0,23) #get the randomely generated bit index to be mutated
                    if mutationIndex not in bitIndicesMutated: #if the current bit has not already been mutated
                        bitIndicesMutated.append(mutationIndex) #add the bit index to this list
                        if population[chromosomeNum][mutationIndex] == 0: #if the current chromosome's bit is 0
                            population[chromosomeNum][mutationIndex] = 1 #change it to 1
                        else: #otherwise
                            population[chromosomeNum][mutationIndex] = 0 #change it to 0
                        j+=1
    return population

def tournamentSelect(population):
    population = sorted(population, key=lambda x: getFitness(convertToRGB(x), targetRGB)) #sort the population based on fitness (high to low)
    int1 = random.randint(0, len(population)-1)
    int2 = random.randint(0, len(population)-1) #randomely generate the two indexes of chromosomes to compare
    if(getFitness(convertToRGB(population[int1]), targetRGB) < getFitness(convertToRGB(population[int2]), targetRGB)):
        #select the chromosome with the highest fitness
        return int1
    else:
        return int2

def isValidString(inputString):
    return all([True if x in ['1','0'] else False for x in inputString]) and len(inputString) == 24
    #if the length of the inputString is 24 and it only contains 1s and 0s, return true that is is a valid inputString
    #otherwise return false that it is invalid

if __name__ == "__main__": #main function
    while True:
        targetString = input("Enter a target 24 bit string (in quotes)\nyou want me to guess: ")
        if(isValidString(targetString)): #if the inputedString is valid continue through program
            break
        print("Must input a 24 bit string with only 1s and 0s. Try Again.")
        #otherwise ask user to try a different input

    targetRGB = convertToRGB(targetString) #convert the input bit String to its associated RGB values

    numChromosomes = int(input("Enter number of chromosomes: ")) #enter number of chromosomes in the population

    while(True):
        numSelection = int(input("Enter number of chromosomes to undergo selection: "))
        numMutation = int(input("Enter number of chromosomes to undergo mutation: "))
        numNewblood = int(input("Enter number of 'newblood' chromosomes: "))
        numCrossoverPairs = int(input("Enter number of crossover pairs: "))
        #ask for each of these required parameters for the program
        if(sum([numSelection, numMutation, numNewblood, 2*numCrossoverPairs]) == numChromosomes):
            #if the number of chromosomes undergoing changes equals the total number of chromosomes continue through program
            break
        print("Total number of selected, mutated, newblood, and 2*crossoverpairs\nshould equal number of chromosomes. Try again.")
        #otherwise ask for these inputs again

    numGenerations = int(input("Enter number of generations to be run: "))

    print("--------------------------------------------------------------------------")
    population = generatePopulation(numChromosomes) #generate that number of random chromosomes
    population = sorted(population, key=lambda x: getFitness(convertToRGB(x), targetRGB))
    # sort this population of chromosomes in terms of fitness from high to low
    bestFitness = getFitness(convertToRGB(population[0]), targetRGB)
    bestChromosome = "".join([str(x) for x in population[0]]) #to keep bestChromosome from changing, make it an immutable object (string rather than list)

    for i in range(numGenerations): #for every generation
        indexsMutated = [] #create an empty mutated list to keep track of chromosome indices that have already been changed by the program
        population = crossover(population, numCrossoverPairs) #crossover 010110100111101001001110 101001011000010110110001
        population = mutate(population, 1, numMutation, indexsMutated) #mutation
        population = mutate(population, 0, numSelection, indexsMutated) #selection
        population = mutate(population, 24, numNewblood, indexsMutated) #newblood
        population = sorted(population, key=lambda x: getFitness(convertToRGB(x), targetRGB))
        if getFitness(convertToRGB(population[0]), targetRGB) < bestFitness:
            #if the fitness of the new generation's best chromosome is better than the previous best
            bestChromosome = "".join([str(x) for x in population[0]])
            bestFitness = getFitness(convertToRGB(bestChromosome), targetRGB)
            #make the new bestChromosome and bestFitness reflect the new best
        else: #otherwise
            population[0] = [int(x) for x in bestChromosome] #change the best chromosome to the last generation's best chromosome
        print("After generation {0}, the best chromosome is {1},\nwith a fitness of: {2}".format(i, "".join([str(x) for x in bestChromosome]), bestFitness))
        #print the current generation's 'best' chromosome and its relevant information
        print("--------------------------------------------------------------------------")
        if bestFitness == 0:
            break #if you got the target chromosome, end loop
