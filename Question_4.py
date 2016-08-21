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

User_rating = Ratings.groupby(['UserID']).count()
User_rating.reset_index(inplace=True)
User_rating = User_rating[['UserID','Rating']]


User_rating_40 = User_rating.loc[User_rating["Rating"] > 39]
Rating_sum_ = pd.DataFrame(Ratings.groupby('UserID')['Rating'].sum())
Rating_sum_.reset_index(inplace=True)
User_rated_movies = pd.merge(User_rating_40,Rating_sum_, on='UserID', how='inner')
top_10_low_rate = User_rated_movies.sort_values("Rating_y")[:10]
top_10_low_rate.rename(columns={'Rating_x':'Rating_count','Rating_y':'Rating_sum'}, inplace=True)
print(top_10_low_rate)
