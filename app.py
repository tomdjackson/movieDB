from tkinter import *
from moviedb import MovieDb

class App:

	def __init__(self, master):

		leftFrame = Frame(master)
		leftFrame.pack(side=LEFT)

		rightFrame = Frame(master)
		rightFrame.pack(side=RIGHT)

		topFrame = Frame(leftFrame)
		topFrame.pack(side=TOP)

		bottomFrame = Frame(leftFrame)
		bottomFrame.pack(side=BOTTOM)

		self.downloadListLabel = Label(rightFrame, text='Download List')
		self.downloadListLabel.pack(side=TOP)

		self.downloadList = Listbox(rightFrame, selectmode=MULTIPLE)
		movies = db.getDownloadList()
		i = 0;
		for movie in movies:
			i+=1
			self.downloadList.insert(i, movie)
		self.downloadList.pack()

		self.listEntry = Entry(rightFrame, bd=5)
		self.listEntry.pack(side = LEFT)
		self.deleteButton=Button(rightFrame, text='Remove Selected', command=self.removeFromList)
		self.deleteButton.pack()
		self.submitButton = Button(rightFrame, text='Add to list', command=self.addToList)
		self.submitButton.pack(side = RIGHT)

		self.unwatchedButton = Button(leftFrame, text='Un-Watched', command=self.getMovies(unwatched))
		self.unwatchedButton.pack(side=TOP)

		if not os.path.exists(db.movie_dir):
			self.warningLabel = Label(bottomFrame, text='Warning: Movie Directory not found.')

		self.quitButton = Button(bottomFrame, text="QUIT", fg="red", command=bottomFrame.quit)
		self.quitButton.pack(side=BOTTOM)

	def removeFromList(self):
		selected = self.downloadList.curselection()
		print(selected)
		for i in selected:
			self.downloadList.delete(i)
			print(self.downloadList.get(i))
			db.removeFromDownloadList(self.downloadList.get(i))

	def addToList(self):
		print('Submit button clicked')
		entry = self.listEntry.get()
		if entry is not None and entry != '':
			print('adding to download list')
			db.addToDownloadList(self.listEntry.get())
			self.listEntry.select_clear()
			i = self.downloadList.size()+1
			self.downloadList.insert(i, entry)
			self.downloadList.see(i)


class MovieFrame:
	def __init__(self, master, movie):
		self.title
		self.year
		self.runtime
		self.director
		self.genre
		self.actors
		self.rating
		self.metascore
		self.imdb_rating
		self.watched
		self.filepath
		self.poster_name


		self.frame = Frame(master)
		self.poster = Canvas(self.frame, bg = "blue", height = 200, width = 100)
		image = self.poster.create_image(50, 50, anchor=NE, image=PhotoImage(self.poster_name))
		canvas.pack(side=RIGHT)


db = MovieDb()
# db.checkForUpdate()

root = Tk()
app = App(root)
root.mainloop()