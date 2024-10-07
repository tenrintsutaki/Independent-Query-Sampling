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

    def sample(self):
        if(self.count == 1):
            # When sample from the urn only contains 1 element, return the index1
            return self.i1
        else:
            r = random.random()
            # Sample a value from e1 and e2, assume e1 < e2
            if(r >= self.e1):
                return self.i2
            elif (r < self.e1):
                return self.i1

class AliasStructure():
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
    def initialize(self):
        for i in range(len(self.probs)): # Scan the index and put them into different sets
            element = self.probs[i]
            if(element < self.avg):
                self.e1Set.add(i)
            elif element == self.avg:
                self.avgSet.add(i)
            else:
                self.e2Set.add(i)

        while len(self.e1Set) > 0: # sample the index from the sets when there are values in e1 set

            i1 = self.e1Set.pop()
            e1 = self.probs[i1]

            i2 = self.e2Set.pop()
            e2 = self.probs[i2]

            self.UrnList.append(Urn(count = 2,e1 = e1,i1 = i1,e2 = self.avg - e1,i2 = i2)) # Create Urn
            rest = round(e2 - (self.avg - e1),2)
            if (rest == self.avg): # e2 become avg
                self.avgSet.add(i2)
            elif (rest > 0 and rest < self.avg): # e2 become e1
                self.e1Set.add(i2)
            self.probs[i2] = rest

        for i in self.avgSet: # Traverse the avg set eventually
            self.UrnList.append(Urn(count = 1,e1 = self.probs[i], i1 = i))

    def initialize_old(self):
        """
        Another way to implement the AS......
        :return:
        """
        for i in range(len(self.probs)): # Scan the index and put them into different sets
            element = self.probs[i]
            if(element < self.avg):
                self.e1Set.append(i)
            elif element == self.avg:
                self.avgSet.append(i)
            else:
                self.e2Set.append(i)

        while len(self.e1Set) > 0: # sample the index from the sets

            i1 = random.choice(self.e1Set)
            e1 = self.probs[i1]

            i2 = random.choice(self.e2Set)
            e2 = self.probs[i2]

            self.UrnList.append(Urn(count = 2,e1 = e1,i1 = i1,e2 = self.avg - e1,i2 = i2)) # Create Urn
            self.e1Set.remove(i1)
            rest = round(e2 - (self.avg - e1),2)
            if(rest == 0): # e2 = 0 after operation
                self.e2Set.remove(i2)
            elif (rest == self.avg): # e2 become avg
                self.avgSet.append(i2)
            elif (rest > 0 and rest < self.avg): # e2 become e1
                self.e2Set.remove(i2)
                self.e1Set.append(i2)
            self.probs[i2] = rest

        for i in self.avgSet: # Traverse the avg set eventually
            self.UrnList.append(Urn(count = 1,e1 = self.probs[i], i1 = i))

    def sample(self):
        urn = random.choice(self.UrnList)
        return urn.sample()

