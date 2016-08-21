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

movie_count = pd.DataFrame(Ratings.groupby('MovieID')['UserID'].count())
movie_count.reset_index(inplace=True)
movie_count = movie_count[["MovieID","UserID"]].rename(columns={'UserID': 'Views'}, inplace=False)

top_10_movies = pd.DataFrame(movie_count.sort_values("Views",ascending=False)[:10])
top_10_movies_with_names = pd.merge(top_10_movies, Movies, on='MovieID', how='inner')

print("Top ten most viewed movies with their  Name")
print(top_10_movies_with_names[['MovieID','Views','Title']])
