import csv
import sys
import math
import operator
import numpy as np

#open and read file depending on file
# Reads in data
with open('movies.csv') as f:
	lines = csv.reader(f, delimiter=',')
  movies={}
  for row in lines:
    movieID= row[0]
    movieTitle= row[1]

    movies[movieID] = str(movieTitle)
f.close()

#open and read csv rating file
# Reads in data
with open('ratings.csv') as f:
	lines = csv.reader(f, delimiter=',')
  ratings_dict={}
  userIDarray = []
  #count = 0
  for row in lines:
    userID=row[0] 
    movieID=row[1]
    rating=row[2]
    userIDarray.append(userID)
    if (movieID == "movieId"): # skips row of labels
      continue
    if not (movieID in ratings_dict): #will enter only if movieID has not been made
      ratings_dict[movieID] =[[int(userID),float(rating)]] 
      #count += 1
      #if(count == 399):
        #break
    else:
      ratings_dict[movieID] = ratings_dict[movieID]+[[int(userID),float(rating)]]
      #count += 1
      #if(count == 399):
        #break
          
                 
f.close()
#print("Ratings Orginal")
#print(ratings_dict)

#User Rating Averages
sum = 0
average ={}
for key in ratings_dict:
    for i in range(len(ratings_dict[key])):
       sum = sum + ratings_dict[key][i][1]
    average[key]=float(sum/len(ratings_dict[key]))
    sum = 0

#print("average")
#print(average)


#Normalizing Data
noramlizedMovieRatings ={}
for key in ratings_dict:
    for i in range(len(ratings_dict[key])):
        #print(ratings_dict[key][i][1])
        ratings_dict[key][i][1] = ratings_dict[key][i][1] - average[key]
        #print(ratings_dict[key][i][1])
    noramlizedMovieRatings[key]= sorted(ratings_dict[key], key=lambda x: x[1], reverse=True)#sorted(ratings_dict[key], key=operator.itemgetter(0), reverse=True)
#print("Normalized")
#print(noramlizedMovieRatings)



numerator = 0
denomenator = 0
denom1 =0
denom2 = 0
#Center Cosine Similarity Calcuation 
cosineSimilarities = {}
for key in ratings_dict:
  for keyTwo in ratings_dict:
    for i in range(len(ratings_dict[key])):   #SOOO, sorry to use nested for loops but I didn't know how to do it any other way because I can't use pandas on my laptop
      for j in range(len(ratings_dict[keyTwo])):
        if(ratings_dict[key][i][0]==(ratings_dict[keyTwo][j][0])):
          numerator += ratings_dict[key][i][1] *ratings_dict[keyTwo][j][1]
          #print(ratings_dict[key][i][1])
          #print(ratings_dict[keyTwo][j][1])
        denom2 += ratings_dict[keyTwo][j][1]**2
      denom1 += ratings_dict[key][i][1]**2
    denomenator = math.sqrt(denom1*denom2)
    
    #print("numer:" + str(numerator))
    if not (key in cosineSimilarities): #will enter only if movieID has not been made
      if(denomenator <= 0):
        continue
      cosineSimilarities[key] =[[keyTwo,numerator/denomenator]] 
    else:
      if(denomenator <= 0):
        continue
      cosineSimilarities[key] = cosineSimilarities[key]+[[keyTwo,numerator/denomenator]]
#print("cosine sim")
#print(cosineSimilarities)


#Finding User's Top Movies
favorites = {}
for key in cosineSimilarities:
    cosineSimilarities[key].sort(reverse=True)

for key in cosineSimilarities:
    i = 0
    if not (key in favorites): #will enter only if movieID has not been made
      favorites[key] = [[cosineSimilarities[key][i][0]]]
      #print(cosineSimilarities[key][i][0])
      i += 1
    else:
      favorites[key] = favorites[key]+[[cosineSimilarities[key][i][0]]]
      #print(cosineSimilarities[key][i][0])
      i += 1
      if(i == 6):
        continue
print("favorites")
print(favorites)
topFiveMovieRecommendations= {}
bestMovie=0
for i in userIDarray:
  for key in noramlizedMovieRatings:
    bestMovie = noramlizedMovieRatings[key][1][0]
    favorites[bestMovie][0]= movies[favorites[bestMovie][0]]
    favorites[bestMovie][1]= movies[favorites[bestMovie][1]]
    favorites[bestMovie][2]= movies[favorites[bestMovie][2]]
    favorites[bestMovie][3]= movies[favorites[bestMovie][3]]
    favorites[bestMovie][4]= movies[favorites[bestMovie][4]]
  topFiveMovieRecommendations[i]= [favorites[bestMovie]]
print(topFiveMovieRecommendations)
#Printing Output to Output File
original_stdout = sys.stdout # Save a reference to the original standard output
with open('output.txt', 'w') as f:
	sys.stdout = f # Change the standard output to the file created.
	#print("Cosine Similarities")
	print("Movie Reccomendations")
	for key in topFiveMovieRecommendations:
		print(key +" : " + topFiveMovieRecommendations[key])
		
	#print("Movie Reccomendations")
	#print(topFiveMovieRecommendations)
	sys.stdout = original_stdout # Reset the standard output to its original value
f.close()
