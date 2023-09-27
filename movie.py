import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv(r'/Users/ashishdagar/Documents/Projects/Movie Recommendation/u.data', sep='\t', names=r_cols, usecols=range(3))

import numpy as np

movieProperties = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})

movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

l1=[]
movieDict={}
movieDict1={}
with open(r'/Users/ashishdagar/Documents/Projects/Movie Recommendation/u.item', encoding = "ISO-8859-1") as f:
    temp = ''
    for line in f:
        fields = line.rstrip('\n').split('|')
        movieID = int(fields[0])
        name = fields[1]
        l1=name.split("(")
        l1[0]=l1[0].rstrip()
        name=l1[0].lower()
        genres = fields[5:25]
        genres = map(int, genres)  
        movieDict1[name] = movieID
        movieDict[movieID] = (name,np.array(list(genres)), movieNormalizedNumRatings.loc[movieID].get('size'), movieProperties.loc[movieID].rating.get('mean'))
        
print("Enter movie name : ",end="")
m=input()
mi=movieDict1[m]

from scipy import spatial

def ComputeDistance(a, b): 
    genresA = a[1]
    genresB = b[1]
    genreDistance = spatial.distance.cosine(genresA, genresB)
    popularityA = a[2]
    popularityB = b[2]
    popularityDistance = abs(popularityA - popularityB)
    return genreDistance + popularityDistance

import operator
def getNeibhors(mi,k):
    
    distances=[]
    for movie in movieDict:
        if movie!=mi:
            dist= ComputeDistance(movieDict[mi], movieDict[movie])
            distances.append((movie, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors=[]
    for x in range(k):
        neighbors.append(distances[x][0])
    for c in range(1,k+1):
        qq=neighbors[c-1]
        md=list(movieDict[qq])
        print("RECOMMEDATion ",c," : ",md[0])
k=10 
getNeibhors(mi,10)
