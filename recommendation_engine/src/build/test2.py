import Tkinter as tk   # python
import display as sad
import newuser as new
import os

TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

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
        for F in (StartPage, existing_user,NewUser,RecommendationsExistingUser,RecommendationsNewUser):
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
        button1 = tk.Button(self, text="New User",
                            command=lambda: controller.show_frame("NewUser"))
        button2 = tk.Button(self, text="Existing User",
                            command=lambda: controller.show_frame("existing_user"))
        button1.pack()
        button2.pack()

class existing_user(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Existing user login", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        user_id = tk.Label (self, text= "User Id")
        entry1 = tk.Entry (self)
        user_id.pack()
        entry1.pack()
        button = tk.Button(self, text="See Recommendations",
                           command=lambda: controller.show_frame("RecommendationsExistingUser"))
        button2 = tk.Button(self, text="Go Back",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()
        button2.pack()

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
        print('------------')
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

class RecommendationsExistingUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Movie Recommendations", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        your = tk.Label(self, text="Recommendations for you", fg="RED")
        top = tk.Label(self, text="Top rated movies", fg="RED")
        picks = tk.Label(self, text="Our picks", fg="RED")
        your.pack(anchor=tk.W)
        for x in range(10):
            ymovie = tk.Label(self, text="Movie name")
            ymovie.pack(anchor=tk.W)
        top.pack(anchor=tk.W)
        for x in range(10):
            tmovie = tk.Label(self, text=sad.final.iloc[x].name)
            tmovie.pack(anchor=tk.W)
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(    )

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
