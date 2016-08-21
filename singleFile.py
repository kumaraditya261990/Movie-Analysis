#importing pandas package as pd
import pandas as pd 
import csv 

#reading all file 
MoviesData = pd.read_table("movies.dat", sep='::', names = ["MovieID", "Title", "Genres"], engine='python') 
RatingsData = pd.read_table("ratings.dat", sep='::', names = [ "UserID","MovieID", "Rating", "Timestamp"], engine='python')
UsersData = pd.read_table("users.dat", sep='::', names = [ "UserID","Gender", "Age", "Occupation","ZipCode"], engine='python')


print("------------------Output of 1st problem------------")
# converting files in form of Data Frame
Movies = pd.DataFrame(MoviesData, columns = ["MovieID", "Title", "Genres"])   
Ratings = pd.DataFrame(RatingsData, columns = [ "UserID","MovieID", "Rating", "Timestamp"])
Users = pd.DataFrame(UsersData, columns = [ "UserID","Gender", "Age", "Occupation","ZipCode"])

movie_count = pd.DataFrame(Ratings.groupby('MovieID')['UserID'].count())     #it count how many time movie viewed
movie_count.reset_index(inplace=True)
movie_count = movie_count[["MovieID","UserID"]].rename(columns={'UserID': 'Views'}, inplace=False)

top_10_movies = pd.DataFrame(movie_count.sort_values("Views",ascending=False)[:10])  #it show only top ten viewed movies
top_10_movies_with_names = pd.merge(top_10_movies, Movies, on='MovieID', how='inner') #with the help of Movies we find name of top  viewed movies 

print("Top ten most viewed movies with their  Name")
#it will print top ten viewed movies with MovieID,Number of time viewed by users and Title of movie 
print(top_10_movies_with_names[['MovieID','Views','Title']])


print("-------------Output of 2nd problem--------------")
#it find list of movies with count of rating
Rating_count = pd.DataFrame(Ratings.groupby('MovieID')['Rating'].count())  
Rating_count.reset_index(inplace=True)
#it filter atleat 40 time rating movies
Rating_count_gt_40 = Rating_count.loc[Rating_count["Rating"] > 39]
Rating_count_gt_40 = Rating_count_gt_40.rename(columns={'Rating': 'Rating_Count'}, inplace=False)

#find the sum of rating according to MovieID
Rating_sum = pd.DataFrame(Ratings.groupby('MovieID')['Rating'].sum())
Rating_sum.reset_index(inplace=True)
Rating_sum = Rating_sum.rename(columns={'Rating': 'Rating_Sum'}, inplace=False)
#joining Movie with how many time it rated and sum of rating
movie_rate_greater40 = pd.merge(Rating_count_gt_40, Rating_sum, on='MovieID', how='inner')
#it will show rating of each movie
movie_rate_greater40["New_Rating"] = movie_rate_greater40["Rating_Sum"]/movie_rate_greater40["Rating_Count"] 
#it will display top 20 rated movies
top_20_rated_movies_with_name = pd.merge(movie_rate_greater40, Movies, on='MovieID', how='inner').sort_values("New_Rating",ascending=False)[:20]
print("top 20 view/rated movie")
print(top_20_rated_movies_with_name[['MovieID','Title']])

print("-------------------------Output of 3rd problem-----------------------")
top_20_rated_movies_with_name = top_20_rated_movies_with_name[['MovieID','Rating_Count']] 

#creating group of users based on Age
Young_users = Users[Users.Age < 20]
Young_adult = Users[(Users.Age >= 20) & (Users.Age <= 40)]
Adult = Users[Users.Age > 40]

#finding how many time a movie viewed by an Age group
Young_users_ratings = pd.merge(Young_users, Ratings, on='UserID', how='inner')
Young_users_ratings_with_top20 = pd.merge(Young_users_ratings, top_20_rated_movies_with_name, on='MovieID', how='inner')
Young_users_movie_ratings = Young_users_ratings_with_top20.groupby(['MovieID']).count()
Young_users_movie_ratings.reset_index(inplace=True)
Young_users_movie_ratings.rename(columns={'UserID': 'Views'}, inplace=True)
Young_users_movie_ratings = Young_users_movie_ratings[['MovieID','Views']]
#print("movie view by young (< 20)")
#print(Young_users_movie_ratings)


Young_adult_ratings = pd.merge(Young_adult, Ratings, on='UserID', how='inner')
Young_adult_ratings_with_top20 = pd.merge(Young_adult_ratings, top_20_rated_movies_with_name, on='MovieID', how='inner')
Young_adult_movie_ratings = Young_adult_ratings_with_top20.groupby(['MovieID']).count()
Young_adult_movie_ratings.reset_index(inplace=True)
Young_adult_movie_ratings.rename(columns={'UserID': 'Views'}, inplace=True)
Young_adult_movie_ratings = Young_adult_movie_ratings[['MovieID','Views']]
#print("movie view by young adult (age >=20 and <= 40)")
#print(Young_adult_movie_ratings)


Adult_ratings = pd.merge(Adult, Ratings, on='UserID', how='inner')
Adult_ratings_with_top20 = pd.merge(Adult_ratings, top_20_rated_movies_with_name, on='MovieID', how='inner')
Adult_movie_ratings = Adult_ratings_with_top20.groupby(['MovieID']).count()
Adult_movie_ratings.reset_index(inplace=True)
Adult_movie_ratings.rename(columns={'UserID': 'Views'}, inplace=True)
Adult_movie_ratings = Adult_movie_ratings[['MovieID','Views']]
#print("movie view by  adult (> 40)")
#print(Adult_movie_ratings)

#showing result in form of MovieID with total viewed and view by Age group
totalView_YoungUserView = pd.merge(top_20_rated_movies_with_name,Young_users_movie_ratings, on='MovieID')
YoungAdultView_AdultView = pd.merge(Young_adult_movie_ratings,Adult_movie_ratings, on='MovieID')
result = pd.merge(totalView_YoungUserView,YoungAdultView_AdultView, on='MovieID')
result.rename(columns={'Rating_Count':'Total_Views','Views':"Views_By_Young",'Views_x':'Views_By_Young_Adult','Views_y':'Views_By_Adult'} , inplace=True)
print("showing result in form of MovieID with total viewed and view by Age group")
print(result)

print("-------------Output of 4th problam-------------------")
#counting rating based on UserId
User_rating = Ratings.groupby(['UserID']).count() 
User_rating.reset_index(inplace=True)
User_rating = User_rating[['UserID','Rating']]

#finding Users who should rated 40 movie
User_rating_40 = User_rating.loc[User_rating["Rating"] > 39]
#finding sum of rating
Rating_sum_ = pd.DataFrame(Ratings.groupby('UserID')['Rating'].sum())
Rating_sum_.reset_index(inplace=True)
User_rated_movies = pd.merge(User_rating_40,Rating_sum_, on='UserID', how='inner')
#it will display top 10 low rated movies
top_10_low_rate = User_rated_movies.sort_values("Rating_y")[:10]
top_10_low_rate.rename(columns={'Rating_x':'Rating_count','Rating_y':'Rating_sum'}, inplace=True)
print("top  10 users who rate movies with low rating")
print(top_10_low_rate)





