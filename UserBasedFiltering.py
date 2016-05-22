# -*- coding: utf-8 -*-
"""
Mining Assignment 1
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # YOUR CODE HERE
        
        # for given userX, get the sorted list of users - by most similar to least similar        
        
        self.userX = userX #Assign userX to this()
        userXItemRatings = self.usersItemRatings[userX] #Get the ratings dictionary for the given user        
        similarity = []
        users =[]
        
        for i in self.usersItemRatings.keys(): #Assign userYs by running a for loop through the dictionary
            if (i != userX):
                userYItemRatings = self.usersItemRatings[i]
                #print("This is pusht rating: \n", i, userYItemRatings)
            else:
                continue
            if(self.similarityFn(userXItemRatings, userYItemRatings) != -2):
                similarity.append(self.similarityFn(userXItemRatings, userYItemRatings))
            else:
                similarity.append(0)
            users.append(i)
        dict_similarity = dict(zip(users,similarity)) # This is how you zip two files to form key value pairs in a dictionary. VERY IMPORTANT!
        temp_list = sorted(dict_similarity, key = dict_similarity.get) #Sort the keys by value.
        if (self.metric.lower() != 'minkowski'): # check if it is not minkowski
            temp_list = temp_list[::-1] #Sort in descending order, reverse the list. For Cosine and Pearson
        temp_list = temp_list[:self.k] #Select only k nearest neighbors
        print("Similarity to User X: \n", temp_list) #block 1 ends here
        
        '''for v in temp_list:
            print("Pusht userYItemRatings \n",v, self.usersItemRatings[v])'''
        
        # calcualte the weighted average item recommendations for userX from userX's k NNs
  
        sum_denom = 0 #Denominator for weighted averages
        print("Dictionary of similarity: \n", dict_similarity.items())
        if( self.k > 1):
            for i in temp_list : # Adjust the scale from [-1,1] to [0,1]
                dict_similarity[i] = (dict_similarity[i] + 1)/2
                sum_denom += dict_similarity[i]
            print(sum_denom)
        
            for i in temp_list: # Calculate the weights
                dict_similarity[i] = round(dict_similarity[i]/sum_denom,2)
        #print("Updated dict: \n", dict_similarity)
        
        # return sorted list of recommendations (sorted highest to lowest ratings)
        
        temp_dict = dict()
        temp_dict.update(userYItemRatings.items())
        for i,v in self.usersItemRatings.items():
            for j,l in v.items():
                temp_dict[j] = 0
        
        for v in temp_list:
            print("Updated userYItemRatings \n",v, self.usersItemRatings[v])
        
       
        for v in temp_list:
            userYItemRatings = self.usersItemRatings[v]
            #print("Very New userYItemRatings \n",v, self.usersItemRatings[v])        
            for band in userYItemRatings.keys():
                if band not in userXItemRatings.keys():
                    if self.k > 1:
                        temp_dict[band] = round(temp_dict[band] + (userYItemRatings[band] * dict_similarity[v]),2)
                    else:
                        temp_dict[band] = round(temp_dict[band] + userYItemRatings[band],2)
        recommendation = []
        for i,v in temp_dict.items():
            if v == 0:
                continue
            else:
                recommendation.append((i,v))
        recommendation = sorted(recommendation, key=lambda x: -x[1])
        print("Recommendations: \n", recommendation)
        
        # example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]
        # once you are done coding this method, delete the pass statement below

        
