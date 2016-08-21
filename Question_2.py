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
