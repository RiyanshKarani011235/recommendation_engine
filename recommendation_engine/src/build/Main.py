import Tkinter as tk   # python
import tkMessageBox
import RecommendationEngine
import sadfgsd as sad
import os
TITLE_FONT = ("Helvetica", 18, "bold")

# GLOBAL 
RECOMMENDED_MOVIES = RecommendationEngine.recommend(10)

class SampleApp(tk.Tk):

	# def __init__(self, *args, **kwargs):
	# 	tk.Tk.__init__(self, *args, **kwargs)

	# 	# the container is where we'll stack a bunch of frames
	# 	# on top of each other, then the one we want visible
	# 	# will be raised above the others
	# 	self.container = tk.Frame(self)
	# 	self.container.pack(side="top", fill="both", expand=True)
	# 	self.container.grid_rowconfigure(0, weight=1)
	# 	self.container.grid_columnconfigure(0, weight=1)

	# 	self.frames = {}
	# 	for F in (StartPage, existing_user_1,Recommendations):
	# 		page_name = F.__name__
	# 		frame = F(parent=self.container, controller=self)
	# 		self.frames[page_name] = frame

	# 		# put all of the pages in the same location;
	# 		# the one on the top of the stacking order
	# 		# will be the one that is visible.
	# 		frame.grid(row=0, column=0, sticky="nsew")

	# 	self.show_frame("StartPage")

	# def show_frame(self, page_name):
	# 	for F in (StartPage, existing_user_1,Recommendations) :
	# 		if page_name == F.__name__ :
	# 			frame = F(parent=self.container, controller=self)

	# 			'''Show a frame for the given page name'''
	# 			frame = self.frames[page_name]
	# 			frame.tkraise()

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (StartPage, existing_user, NewUser, RecommendationsNewUser, Recommendations):
			page_name = F.__name__
			# frame = F(parent=container, controller=self)
			self.frames[page_name] = F

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			# frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name](parent=self.container, controller=self)
		frame.grid(row=0, column=0, sticky="nsew")
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		Label = tk.Label(self, text="MovieMender", font=TITLE_FONT)
		Label.pack(side="top", fill="x", pady=10)

		self.button1 = tk.Button(self, text="New User", command=lambda: controller.show_frame("NewUser"))
		self.button2 = tk.Button(self, text="Existing User",
							command=self.onRecommendButtonClicked)
		self.button1.pack()
		self.button2.pack()

	def onRecommendButtonClicked(self) :
		print(self.button2)
		self.controller.show_frame("existing_user")

str=os.path.join('.', '')
file_path=[str+'Action.txt',str+'Adventure.txt',str+'Animation.txt',str+'Childrens.txt',str+'Comedy.txt',str+'Crime.txt',
		   str+'Documentary.txt',str+'Drama.txt',str + 'Fantasy.txt',str+'Film-noir.txt',str+'Horror.txt',str+'Musical.txt',
		   str+'Mystery.txt',str+'Romance.txt',str+'Sci-Fi.txt',str+'Thriller.txt',str+'War.txt',str+'Western.txt']
genre=['Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary',
		'Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
check_variables=[]
title = []
counter=0
output=[]

class NewUser(tk.Frame):
	
	def cb(self):
		global counter
		global output
		counter = 0
		output = []
		for x in range(len(check_variables)):
			if check_variables[x].get() == 1:
				counter += 1
		print(counter)
		for x in range(len(check_variables)):
			if check_variables[x].get() == 1:
				from itertools import islice
				with open(file_path[x]) as myfile:
					head = list(islice(myfile, int(10 / counter)))
					for idx, lines in enumerate(head):
						line = lines.split()
						print('hello')
						print(line[0])
						output.append(line[0])
				myfile.close()

		print(output)

	def showframe(self):
		movies = []
		with open(os.path.join('data-small', 'movies.csv'), 'r') as f : 
			movies = f.read().split('\n')[1:]
		for x in range(len(output)):
			for element in movies : 
				if int(element.split(',')[0]) == int(output[x]) : 
					title.append(element.split(',')[1])
					break
		print('------------')
		print(title)
		print(output)
		print(counter)
		self.controller.show_frame("RecommendationsNewUser")

	def __init__(self, parent, controller ):
		self.controller=controller
		tk.Frame.__init__(self, parent)
		for i in range(len(genre)):
			check_variables.append(tk.IntVar())
		Label = tk.Label(self, text="Select your favourite genres", font=TITLE_FONT)
		Label.pack(side="top", fill="x", pady=10)

		for x in range(len(genre)):
			l = tk.Checkbutton(self, text=genre[x], variable=check_variables[x], command=self.cb)
			l.pack(anchor=tk.W)

		button = tk.Button(self, text="Go Back",
						   command=lambda: controller.show_frame("StartPage"))
		button2 = tk.Button(self, text="See Recommendations",
						   command=self.showframe)
		button2.pack()
		button.pack()

class existing_user(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		self.Label = tk.Label(self, text="Existing user login", font=TITLE_FONT)
		self.Label.pack(side="top", fill="x", pady=10)
		
		self.user_id = tk.Label (self, text= "User Id")
		self.user_id.pack()

		self.entry1 = tk.Entry (self)
		self.entry1.pack()

		self.button = tk.Button(self, text="Login", command=self.onRecommendButtonClicked)
		self.button.pack()

		self.button2 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("StartPage"))
		self.button2.pack()

	def onRecommendButtonClicked(self) : 
		userId = -1
		try :
			userId = int(self.entry1.get())
		except : 
			pass
		if(not(userId >= 0 and userId < 943)) : 
			tkMessageBox.showwarning(
				"Invalid User ID",
				"User Id should be an integer between 0 and 942"
			)
			return

		global RECOMMENDED_MOVIES
		RECOMMENDED_MOVIES = RecommendationEngine.recommend(userId)
		print(RECOMMENDED_MOVIES)
		self.controller.show_frame("Recommendations")
	
class Recommendations(tk.Frame):

	def __init__(self, parent, controller):
		print('recommendations : init : called')
		tk.Frame.__init__(self, parent)
		self.controller = controller
		Label = tk.Label(self, text="Movie Recommendations", font=TITLE_FONT)
		Label.pack(side="top", fill="x", pady=10)
		your = tk.Label (self, text= "Recommendations for you", fg="RED")
		top = tk.Label (self, text= "Top rated movies", fg ="RED")
		picks = tk.Label (self, text= "Our picks", fg="RED")

		self.tmovie1 = tk.Label( self , text = sad.final.iloc[0].name)
		self.tmovie2 = tk.Label(self, text=sad.final.iloc[1].name)
		self.tmovie3 = tk.Label(self, text=sad.final.iloc[2].name)
		self.tmovie4 = tk.Label(self, text=sad.final.iloc[3].name)
		self.tmovie5 = tk.Label(self, text=sad.final.iloc[4].name)

		if len(RECOMMENDED_MOVIES) >= 5 : 
			print('using recommended_movies')
			self.ymovie1 = tk.Label( self , text = RECOMMENDED_MOVIES[0])
			self.ymovie2 = tk.Label(self, text=RECOMMENDED_MOVIES[1])
			self.ymovie3 = tk.Label(self, text=RECOMMENDED_MOVIES[2])
			self.ymovie4 = tk.Label(self, text=RECOMMENDED_MOVIES[3])
			self.ymovie5 = tk.Label(self, text=RECOMMENDED_MOVIES[4])
		else :
			print('not using recommended_movies')
			self.ymovie1 = tk.Label (self, text ="Movie name 1")
			self.ymovie2 = tk.Label (self, text ="Movie name ")
			self.ymovie3 = tk.Label (self, text ="Movie name ")
			self.ymovie4 = tk.Label (self, text ="Movie name ")
			self.ymovie5 = tk.Label (self, text ="Movie name ")

		your.pack(anchor = tk.W)
		self.ymovie1.pack(anchor = tk.W)
		self.ymovie2.pack(anchor = tk.W)
		self.ymovie3.pack(anchor = tk.W)
		self.ymovie4.pack(anchor = tk.W)
		self.ymovie5.pack(anchor = tk.W)
		top.pack(anchor = tk.W)
		self.tmovie1.pack(anchor = tk.W)
		self.tmovie2.pack(anchor = tk.W)
		self.tmovie3.pack(anchor = tk.W)
		self.tmovie4.pack(anchor = tk.W)
		self.tmovie5.pack(anchor = tk.W)
		picks.pack(anchor = tk.W)
		button = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("StartPage"))
		button.pack()

class RecommendationsNewUser(tk.Frame):
    def __init__(self, parent, controller):
        print('RecommendationsNewUser : init : called')
        print(output)
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Movie Recommendations", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        your = tk.Label (self, text= "Recommendations for you", fg="RED")
        top = tk.Label (self, text= "Top rated movies", fg ="RED")
        picks = tk.Label (self, text= "Our picks", fg="RED")
        your.pack(anchor=tk.W)
        print(counter)
        for x in range(int(10/counter)):
            ymovie = tk.Label(self, text=title[x])
            ymovie.pack(anchor = tk.W)
        top.pack(anchor=tk.W)
        for x in range(10):
            tmovie = tk.Label(self, text=sad.final.iloc[x].name)
            tmovie.pack(anchor = tk.W)
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
	app = SampleApp()
	app.mainloop()
