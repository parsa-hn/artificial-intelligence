import re
import string
import random

class Decoder:
    def __init__(self, encodedText):
        self.encodedText = encodedText
        self.populationSize = 500
        self.crossoverProbability = 0.65
        self.carryPercentage = 0.2
        self.correctChromosome = ''
        self.dictionary = self.fillDict()
        self.population = self.makeFirstPopulation()
        self.encodedTextNumOfWords = self.calcNumOfWords()

    def decode(self):
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            for i in range(self.populationSize):
                fitness = self.calcFitness(self.population[i])
                if (fitness == -1):
                    self.correctChromosome = self.population[i]
                    return self.decodedText()
                else:
                    fitnesses.append([fitness, i])
            fitnesses.sort(key=lambda x:x[0])
            matingPool = self.makeMatingPool(fitnesses)

            crossoverPool = self.makeCrossoverPool(matingPool)

            carry = []
            for i in range(1, int(self.populationSize*self.carryPercentage) + 1):
                carry.append(self.population[fitnesses[-i][1]])

            self.population.clear()
            for i in range(self.populationSize - int(self.populationSize*self.carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))
                
            self.population.extend(carry)

    def fillDict(self):
        text = open("global_text.txt").read()
        words = re.split('[^a-zA-Z]', text)
        dictionary = set()
        for word in words:
            if word:
                dictionary.add(word.lower())
        return dictionary

    def makeFirstPopulation(self):
        firstPopulation = []
        for i in range(self.populationSize):
            newStr = self.makeRandomChromosome()
            firstPopulation.append(newStr)
        return firstPopulation

    def makeRandomChromosome(self):
        alphabet = list(string.ascii_lowercase)
        out = ''
        for i in range(len(alphabet)):
            randomChar = random.choice(alphabet)
            alphabet.remove(randomChar)
            out += randomChar
        return out

    def calcFitness(self, chromosome):
        fitness = 0
        encodedWords = re.split('[^a-zA-Z]', self.encodedText)
        for word in encodedWords:
            if not word:
                continue
            word = word.lower()
            newWord = ''
            for char in word:
                newWord += chromosome[ord(char) - ord('a')]
            if newWord in self.dictionary:
                fitness += 1
        if fitness == self.encodedTextNumOfWords:
            return -1
        return fitness

    def calcNumOfWords(self):
        counter = 0
        words = re.split('[^a-zA-Z]', self.encodedText)
        for word in words:
            if word:
                counter += 1
        return counter

    def makeMatingPool(self, fitnesses):
        matingPool = []
        probabalityPool = []
        for i in range(1, self.populationSize + 1):
            for j in range(i):
                probabalityPool.append(fitnesses[i - 1])
        random.shuffle(probabalityPool)
        for i in range(self.populationSize - int(self.populationSize*self.carryPercentage)):
            matingPool.append(self.population[probabalityPool[random.randint(0, len(probabalityPool) - 1)][1]])
        return matingPool

    def makeCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(int(len(matingPool) / 2)):
            if random.random() > self.crossoverProbability:
                crossoverPool.append(matingPool[i*2])
                crossoverPool.append(matingPool[i*2 + 1])
            else:
                parent1 = list(matingPool[i*2])
                parent2 = list(matingPool[i*2 + 1])
                child1 = list(string.ascii_lowercase)
                child2 = list(string.ascii_lowercase)
                selectedPositions = []
                charsInChild1 = []
                charsInChild2 = []
                while len(selectedPositions) < 13:
                    selectedPosition = random.randint(0, 25)
                    if selectedPosition in selectedPositions:
                        continue
                    selectedPositions.append(selectedPosition)
                    child1[selectedPosition] = parent1[selectedPosition][0]
                    charsInChild1.append(child1[selectedPosition])
                    child2[selectedPosition] = parent2[selectedPosition][0]
                    charsInChild2.append(child2[selectedPosition])
                selectedPositions.sort()
                for j in range(len(selectedPositions)):
                    parent2.remove(charsInChild1[j])
                    parent1.remove(charsInChild2[j])
                parent1It = 0
                parent2It = 0
                for j in range(26):
                    if not (j in selectedPositions):
                        child1[j] = parent2[parent2It][0]
                        parent2It += 1
                        child2[j] = parent1[parent1It][0]
                        parent1It += 1
                crossoverPool.append(''.join(child1))
                crossoverPool.append(''.join(child2))

        return crossoverPool

    def mutate(self, chromosome):
        rand1 = random.randint(0, 25)
        rand2 = random.randint(0, 25)
        while (rand1 == rand2):
            rand2 = random.randint(0, 25)
        out = list(chromosome)
        out[rand1], out[rand2] = out[rand2], out[rand1]
        return ''.join(out)

    def decodedText(self):
        correctChromosome = self.correctChromosome
        decodedText = ''
        for i in range(len(self.encodedText)):
            newChar = self.encodedText[i]
            if (newChar.isalpha()):
                if newChar.islower():
                    decodedText += correctChromosome[ord(newChar) - ord('a')]
                else:
                    decodedText += (correctChromosome[ord(newChar) - ord('A')]).upper()
            else:
                decodedText += newChar
        return decodedText
