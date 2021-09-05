import random
from typing import TextIO
import requests
from bs4 import BeautifulSoup
import pandas as pd

url='https://www.imdb.com/chart/top'

# request the url
response=requests.get(url)
html=response.text
soup=BeautifulSoup(html,'html.parser')
movietags=soup.select('td.titleColumn')

# scrape all tabel data with class titleColumn
innermovie_tags=soup.select('td.titleColumn a')

# select all span with name==ir (the film rating)
rating_tags=soup.select('td.posterColumn span[name=ir]')
movetag0=movietags[0]

print(movetag0)
movesplit=movetag0.text.split()

print(movesplit)

#function aim to return the year of each film 
def get_year(movie_tag):
    moviesplit=movie_tag.text.split()
    print(moviesplit)
    year=moviesplit[-1]
    return year
    
    
years=[get_year(tag) for tag in movietags]
print(movietags)
actors=[tag['title'] for tag in innermovie_tags]
titles=[tag.text for tag in innermovie_tags]
rating=[float(rate['data-value']) for rate in rating_tags]
n_movies=len(titles)

#convert this lists to series to make the dataframe
years=pd.Series(years)
actors=pd.Series(actors)
titles=pd.Series(titles)
rating=pd.Series(rating)

# making the dataframe
imdb_df=pd.concat([titles,years,actors,rating],axis=1)
imdb_df.columns=['Title',"Year",'Actors','Rating']
imdb_df['rank'] = imdb_df.index + 1
print(imdb_df)

#save the dataframe into csv file
imdb_df.to_csv("imdbdataexport.csv")

print(imdb_df.index)

# Here you can ask for random film
while True:
    idx=random.randrange(0,n_movies)
    print(f'{titles[idx]} {years[idx]} rating: {rating[idx]:.1f} starring: {actors[idx]}')
    answer=input("do you want another movie (y/[n]) ?")
    if answer !='y':
        break
    
    
    

    
