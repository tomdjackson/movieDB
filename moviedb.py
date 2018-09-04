import os
from imdb import IMDb
from tinydb import TinyDB, Query

db=TinyDB("Movies/db.json")


def getFromDB():
	return None

def getFromImdb():
	ia = IMDb()
	for filename in os.listdir('Movies'):
		if not (filename.endswith(".DS_Store") or filename.endswith(".py") or filename.endswith(".json")):
			name = os.path.splitext(filename)[0]
			movies = ia.serch_movie(name)
			if movies != None:
				movie = movies[0]
				title = movie['title']
				#TODO: append to list of directors?
				for director in movie['directors']
					director_list = movie['director']
				year = movie['year']
				for actor in movie['cast']
					actors = 
				for genres in movie['genres']
					genre_list = 
				cover_img = movie['cover url']
				runtime = movie['runtimes']


				db.insert({'title':title, 'year':year 'directors':director_list, 'cast':actors, 'genres':genres, 'cover_img':cover_img, 'runtime':runtime})