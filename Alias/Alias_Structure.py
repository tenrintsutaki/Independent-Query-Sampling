import random


class Urn():
    def __init__(self,count,e1,i1,e2 = None,i2 = None):
        self.count = count
        self.e1 = e1
        self.i1 = i1
        self.e2 = e2
        self.i2 = i2
        if count == 2:
            avg = self.e1 + self.e2
            self.e1 = e1 * (1 / avg)
            self.e2 = e2 * (1 / avg)

    def sample(self,repeat_index):
        if(self.count == 1):
            # When sample from the urn only contains 1 element, return the index1
            return self.i1
        else:
            repeat_index = random.random()
            # Sample a value from e1 and e2, assume e1 < e2
            if(repeat_index >= self.e1):
                return self.i2
            elif (repeat_index < self.e1):
                return self.i1

class AliasStructure():
    # Alias Structure Class
    def __init__(self,probs):
        # if(sum(probs) != 1.0):
        #     raise RuntimeError(f"Probabilities must sum to 1.0, but now is {sum(probs)}")
        self.probs = probs
        self.UrnSet = []
        self.avg = 1/len(self.probs)
        self.e1List = []
        self.e2List = []
        self.avgList = []
    def initialize(self):
        for i in range(len(self.probs)): # Scan the index and put them into different sets
            element = self.probs[i]
            if(element < self.avg):
                self.e1List.append(i)
            elif element == self.avg:
                self.avgList.append(i)
            else:
                self.e2List.append(i)

        while len(self.e1List) > 0 and len(self.e2List) > 0: # sample the index from the sets when there are values in e1 set

            i1 = self.e1List.pop()
            e1 = self.probs[i1]

            i2 = self.e2List.pop()
            e2 = self.probs[i2]

            self.UrnSet.append(Urn(count = 2, e1 = e1, i1 = i1, e2 =self.avg - e1, i2 = i2)) # Create Urn
            rest = e2 - (self.avg - e1)
            # rest_round = round(e2 - (self.avg - e1), 2)
            # print(rest <= rest_round + 0.01 * rest and rest >= rest_round - 0.01 * rest)
            if(rest == 0): # e2 = 0 after operation
                pass
            elif (rest <= self.avg + 0.01 * rest and rest >= self.avg - 0.01 * rest): # e2 become avg
                self.avgList.append(i2)
            elif (rest > 0 and rest < self.avg): # e2 become e1
                self.e1List.append(i2)
            elif (rest > self.avg):
                self.e2List.append(i2)
            self.probs[i2] = rest

        for i in self.avgList: # Traverse the avg set eventually
            self.UrnSet.append(Urn(count = 1, e1 = self.probs[i], i1 = i))

        # Due to the computational error, we need to put the last value into a single URN
        if len(self.e1List) != 0:
            last_index = self.e1List.pop()
            self.UrnSet.append(Urn(count = 1, e1 = self.avg, i1 = last_index))

    def sample(self):
        # Choose an urn first
        index = random.randint(0,len(self.UrnSet)-1) # Create a repeatable index
        urn = self.UrnSet[index]
        repeat_index = index / (len(self.UrnSet) - 1) # Repeatable number from [0,1]
        return urn.sample(repeat_index)

class AliasStructure_List():
    # Alias Structure Class
    def __init__(self,probs):
        # if(sum(probs) != 1.0):
        #     raise RuntimeError(f"Probabilities must sum to 1.0, but now is {sum(probs)}")
        self.probs = probs
        self.UrnList = []
        self.avg = 1/len(self.probs)
        self.e1Set = set()
        self.e2Set = set()
        self.avgSet = set()
        # self.e1Set = []
        # self.e2Set = []
        # self.avgSet = []
    def initialize(self):
        for i in range(len(self.probs)): # Scan the index and put them into different sets
            element = self.probs[i]
            if(element < self.avg):
                self.e1Set.add(i)
            elif element == self.avg:
                self.avgSet.add(i)
            else:
                self.e2Set.add(i)

        while len(self.e1Set) > 0 and len(self.e2Set) > 0: # sample the index from the sets when there are values in e1 set

            i1 = self.e1Set.pop()
            self.e1Set.add(i1)
            e1 = self.probs[i1]

            i2 = self.e2Set.pop()
            self.e2Set.add(i2)
            e2 = self.probs[i2]

            self.UrnList.append(Urn(count = 2, e1 = e1, i1 = i1, e2 =self.avg - e1, i2 = i2)) # Create Urn
            self.e1Set.remove(i1)

            rest = e2 - (self.avg - e1)
            # rest_round = round(e2 - (self.avg - e1), 2)
            # print(rest <= rest_round + 0.01 * rest and rest >= rest_round - 0.01 * rest)
            if(rest == 0): # e2 = 0 after operation
                self.e2Set.remove(i2)
            elif (rest <= self.avg + 0.01 * rest and rest >= self.avg - 0.01 * rest): # e2 become avg
                self.avgSet.add(i2)
            elif (rest > 0 and rest < self.avg): # e2 become e1
                self.e2Set.remove(i2)
                self.e1Set.add(i2)
            self.probs[i2] = rest

        for i in self.avgSet: # Traverse the avg set eventually
            self.UrnList.append(Urn(count = 1, e1 = self.probs[i], i1 = i))

        # Due to the computational error, we need to put the last value into a single URN
        if len(self.e1Set) != 0:
            last_index = self.e1Set.pop()
            self.UrnList.append(Urn(count = 1, e1 = self.avg, i1 = last_index))

    def sample(self):
        urn = random.choice(self.UrnList)
        return urn.sample()

class AliasStructure_Direct_Nodes():
    # Alias Structure Class
    def __init__(self,probs,nodes):
        # if(sum(probs) != 1.0):
        #     raise RuntimeError(f"Probabilities must sum to 1.0, but now is {sum(probs)}")
        self.probs = probs
        self.nodes = nodes
        self.UrnList = []
        self.avg = 1/len(self.probs)
        self.e1Set = set()
        self.e2Set = set()
        self.avgSet = set()
        # self.e1Set = []
        # self.e2Set = []
        # self.avgSet = []
    def initialize(self):
        for i in range(len(self.probs)): # Scan the index and put them into different sets
            element = self.probs[i]
            if(element < self.avg):
                self.e1Set.add(i)
            elif element == self.avg:
                self.avgSet.add(i)
            else:
                self.e2Set.add(i)

        while len(self.e1Set) > 0 and len(self.e2Set) > 0: # sample the index from the sets when there are values in e1 set

            i1 = self.e1Set.pop()
            self.e1Set.add(i1)
            e1 = self.probs[i1]

            i2 = self.e2Set.pop()
            self.e2Set.add(i2)
            e2 = self.probs[i2]

            self.UrnList.append(Urn(count = 2, e1 = e1, i1 = self.nodes[i1], e2 = self.avg - e1, i2 = self.nodes[i2])) # Create Urn
            self.e1Set.remove(i1)

            rest = e2 - (self.avg - e1)
            # rest_round = round(e2 - (self.avg - e1), 2)
            # print(rest <= rest_round + 0.01 * rest and rest >= rest_round - 0.01 * rest)
            if(rest == 0): # e2 = 0 after operation
                self.e2Set.remove(i2)
            elif (rest <= self.avg + 0.01 * rest and rest >= self.avg - 0.01 * rest): # e2 become avg
                self.avgSet.add(i2)
            elif (rest > 0 and rest < self.avg): # e2 become e1
                self.e2Set.remove(i2)
                self.e1Set.add(i2)
            self.probs[i2] = rest

        for i in self.avgSet: # Traverse the avg set eventually
            self.UrnList.append(Urn(count = 1, e1 = self.probs[i], i1 = self.nodes[i]))

        # Due to the computational error, we need to put the last value into a single URN
        if len(self.e1Set) != 0:
            last_index = self.e1Set.pop()
            self.UrnList.append(Urn(count = 1, e1 = self.avg, i1 = self.nodes[last_index]))

    def sample(self):
        urn = random.choice(self.UrnList)
        return urn.sample()