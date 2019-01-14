import urllib.parse, urllib.error, urllib.request
import json
import os
import sqlite3


class MovieDb:
	def __init__(self):
		self.apikey = ''
		with open('APIkeys.json') as f:
			keys = json.load(f)
			self.apikey = '&apikey=' + keys['OMDBapi']
		self.serviceurl = 'http://www.omdbapi.com/?'
		self.movie_dir = '/Volumes/SEAGATE/Movies/'
		self.db_name = 'movies.sqlite'

	def addToDownloadList(self, title):
		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()
		cur.execute('''CREATE TABLE IF NOT EXISTS DownloadList
		(Title TEXT)''')

		cur.execute('SELECT Title FROM DownloadList WHERE Title = ? ', (title,))
		row = cur.fetchone()
		if row is None:
			print('Adding ' + title + ' to download list')
			cur.execute('''INSERT INTO DownloadList (Title) VALUES (?)''', (title,))
		else:
			print(title + ' already in download list')

		conn.commit()
		conn.close()

	def removeFromDownloadList(self, title):
		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()

		cur.execute('''DELETE FROM DownloadList WHERE Title=?''', (title,))

		conn.commit()
		conn.close()

	def getDownloadList(self):
		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()
		cur.execute('''SELECT * FROM DownloadList''')
		rows = cur.fetchall()
		downloadList = []
		for row in rows:
			downloadList.append(row[0])
		conn.close()
		return downloadList

	def getMoviesFromDB(self):
		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()

		cur.execute('SELECT * FROM MovieInfo')
		rows = cur.fetchall()
		conn.close()

		return rows

	def updateWatched(self, title, watched):
		conn = sqlite3.connect(str(filename))
		cur=conn.cursor()

		cur.execute('UPDATE MovieInfo SET wached = ? WHERE title = ?', (watched, title))

		conn.commit()
		conn.close()

	def checkForUpdate(self, dir=None):
		if dir is None:
			dir = self.movie_dir
		print('Searching ' + dir + ' for new movies');

		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()

		if os.path.exists(dir):
			#TODO: Recursive through directories.
			for filename in os.listdir(self.movie_dir):
				if not filename.endswith('.DS_Store') and filename[:1] != '.' and filename[:1] != '_':
					if os.path.isdir(filename):
						checkForUpdate(filename)
					else:
						title = os.path.splitext(filename)[0]
						cur.execute('SELECT Title FROM MovieInfo WHERE Title = ? ', (title,))
						row = cur.fetchone()
						if(row is not None):
							filepath = self.movie_dir + filename
							self.searchOMDb(title, filepath)
						else:
							print('Row exisits for ' + title +', skipping...')

		else:
			print('Error encountered: Folder not Found ' + dir)

	def searchOMDb(self, title, filepath):
		#TODO: if title contains special characters, escape them
		if len(title) < 1 or title == 'quit':
			print('Goodbye now...')
			return None
		try:
			print('Retrieving the data of ' + title + '...')
			url = self.serviceurl + urllib.parse.urlencode({'t': title})+self.apikey
			uh = urllib.request.urlopen(url)
			data = uh.read()
			json_data=json.loads(data)

			if json_data['Response']=='True':
				poster_name = self.download_poster(json_data)
				self.save_to_database(json_data, filepath, poster_name)
			else:
				print('Error encountered: ',json_data['Error'])

		except urllib.error.URLError as e:
			print('ERROR: {e.reason}')


	def save_to_database(self, json_data, filepath, poster_name):
		conn = sqlite3.connect(str(self.db_name))
		cur=conn.cursor()

		title = json_data['Title']
		director = genre = actors = 'N/A'
		runtime = year = metascore = imdb_rating = watched = 0

		if json_data['Year']!='N/A':
			year = int(json_data['Year'][:4])
		if json_data['Runtime']!='N/A':
			runtime = int(json_data['Runtime'].split()[0])
		if json_data['Director']!='N/A':
			director = json_data['Director']
		if json_data['Genre']!='N/A':
			genre = json_data['Genre']
		if json_data['Actors']!='N/A':
			actors = json_data['Actors']
		if json_data['Metascore']!='N/A':
			metascore = float(json_data['Metascore'])
		else:
			metascore=-1
		if json_data['imdbRating']!='N/A':
			imdb_rating = float(json_data['imdbRating'])
		else:
			imdb_rating=-1

		cur.execute('''INSERT INTO MovieInfo (Title, Year, Runtime, Director, Genre, Actors, Rating, Metascore, IMDBRating, Watched, Filepath, Postername)
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (title,year,runtime,director,genre,actors,-1,metascore,imdb_rating,watched,filepath, poster_name))

		# Commits the change and close the connection to the database
		conn.commit()
		conn.close()


	def download_poster(self, json_data):
		if json_data['Poster']!='N/A':
			title = json_data['Title']
			poster_url = json_data['Poster']
			# Splits the poster url by '.' and picks up the last string as file extension
			poster_file_extension=poster_url.split('.')[-1]
			# Reads the image file from web
			poster_data = urllib.request.urlopen(poster_url).read()

			savelocation='posters/'
			# Creates new directory if the directory does not exist. Otherwise, just use the existing path.
			if not os.path.isdir(savelocation):
				os.mkdir(savelocation)

			filename=savelocation+str(title)+'.'+poster_file_extension
			f=open(filename,'wb')
			f.write(poster_data)
			f.close()
			return filename