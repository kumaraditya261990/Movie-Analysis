#importing pandas package as pd
import pandas as pd 

#reading all file 
MoviesData = pd.read_table("movies.dat", sep='::', names = ["MovieID", "Title", "Genres"], engine='python') 
RatingsData = pd.read_table("ratings.dat", sep='::', names = [ "UserID","MovieID", "Rating", "Timestamp"], engine='python')
UsersData = pd.read_table("users.dat", sep='::', names = [ "UserID","Gender", "Age", "Occupation","ZipCode"], engine='python')

# converting files in form of Data Frame
Movies = pd.DataFrame(MoviesData, columns = ["MovieID", "Title", "Genres"])   
Ratings = pd.DataFrame(RatingsData, columns = [ "UserID","MovieID", "Rating", "Timestamp"])
Users = pd.DataFrame(UsersData, columns = [ "UserID","Gender", "Age", "Occupation","ZipCode"])

Rating_count = pd.DataFrame(Ratings.groupby('MovieID')['Rating'].count())
Rating_count.reset_index(inplace=True)
Rating_count_gt_40 = Rating_count.loc[Rating_count["Rating"] > 39]
Rating_count_gt_40 = Rating_count_gt_40.rename(columns={'Rating': 'Rating_Count'}, inplace=False)

Rating_sum = pd.DataFrame(Ratings.groupby('MovieID')['Rating'].sum())
Rating_sum.reset_index(inplace=True)
Rating_sum = Rating_sum.rename(columns={'Rating': 'Rating_Sum'}, inplace=False)

movie_rate_greater40 = pd.merge(Rating_count_gt_40, Rating_sum, on='MovieID', how='inner')
movie_rate_greater40["New_Rating"] = movie_rate_greater40["Rating_Sum"]/movie_rate_greater40["Rating_Count"]
top_20_rated_movies_with_name = pd.merge(movie_rate_greater40, Movies, on='MovieID', how='inner').sort_values("New_Rating",ascending=False)[:20]
print("top 20 view/rated movie")
print(top_20_rated_movies_with_name[['MovieID','Title']])
top_20_rated_movies_with_name = top_20_rated_movies_with_name[['MovieID','Rating_Count']] 

Young_users = Users[Users.Age < 20]
Young_adult = Users[(Users.Age >= 20) & (Users.Age <= 40)]
Adult = Users[Users.Age > 40]

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

totalView_YoungUserView = pd.merge(top_20_rated_movies_with_name,Young_users_movie_ratings, on='MovieID')
YoungAdultView_AdultView = pd.merge(Young_adult_movie_ratings,Adult_movie_ratings, on='MovieID')
result = pd.merge(totalView_YoungUserView,YoungAdultView_AdultView, on='MovieID')
result.rename(columns={'Rating_Count':'Total_Views','Views':"Views_By_Young",'Views_x':'Views_By_Young_Adult','Views_y':'Views_By_Adult'} , inplace=True)
print(result)
