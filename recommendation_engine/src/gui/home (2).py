import Tkinter as tk   # python
import sadfgsd as sad
TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, existing_user_1,Recommendations):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="MovieMender", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="New User",
                            command=lambda: controller.show_frame("Recommendations"))
        button2 = tk.Button(self, text="Existing User",
                            command=lambda: controller.show_frame("existing_user_1"))
        button1.pack()
        button2.pack()


'''class NewUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="New user registration", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        user_id = tk.Label (self, text= "User Id")

        entry1 = tk.Entry (self)



        user_id.pack()

        entry1.pack()


        button2 = tk.Button(self, text="Register",
                        command=lambda: controller.show_frame("NewUser2"))
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button2.pack()
        button.pack()
'''


class existing_user_1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Existing user login", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        user_id = tk.Label (self, text= "User Id")

        entry1 = tk.Entry (self)



        user_id.pack()

        entry1.pack()



        button = tk.Button(self, text="Login",
                           command=lambda: controller.show_frame("Recommendations"))

        button2 = tk.Button(self, text="Go Back",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()
        button2.pack()

'''class NewUser2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Select your favourite genres", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        Label1 = tk.Label (self, text = "Select your favourite genres.")
        genre0 = tk.Checkbutton (self, text ="Action")
        genre1= tk.Checkbutton (self, text ="Adventure")
        genre2 = tk.Checkbutton (self, text ="Animation")
        genre3 = tk.Checkbutton (self, text ="Children's")
        genre4 = tk.Checkbutton (self, text ="Comedy")
        genre5 = tk.Checkbutton (self, text ="Crime")
        genre6 = tk.Checkbutton (self, text ="Documentary")
        genre7 = tk.Checkbutton (self, text ="Drama")
        genre8 = tk.Checkbutton (self, text ="Fantasy")
        genre9 = tk.Checkbutton (self, text ="Film-Noir")
        genre10 = tk.Checkbutton (self, text ="Horror")
        genre11 = tk.Checkbutton (self, text ="Musical")
        genre12 = tk.Checkbutton (self, text ="Mystery")
        genre13 = tk.Checkbutton (self, text ="Romance")
        genre14 = tk.Checkbutton (self, text ="Sci-Fi")
        genre15 = tk.Checkbutton (self, text ="Thriller")
        genre16 = tk.Checkbutton (self, text ="War")
        genre17 = tk.Checkbutton (self, text ="Western")
        next = tk.Button(self, text = "Next->")

        Label1.pack(anchor = tk.W)
        genre0.pack(anchor = tk.W)
        genre1.pack(anchor = tk.W)
        genre2.pack(anchor = tk.W)
        genre3.pack(anchor = tk.W)
        genre4.pack(anchor = tk.W)
        genre5.pack(anchor = tk.W)
        genre6.pack(anchor = tk.W)
        genre7.pack(anchor = tk.W)
        genre8.pack(anchor = tk.W)
        genre9.pack(anchor = tk.W)
        genre10.pack(anchor = tk.W)
        genre11.pack(anchor = tk.W)
        genre12.pack(anchor = tk.W)
        genre13.pack(anchor = tk.W)
        genre14.pack(anchor = tk.W)
        genre15.pack(anchor = tk.W)
        genre16.pack(anchor = tk.W)
        genre17.pack(anchor = tk.W)
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="See Recommendations",
                           command=lambda: controller.show_frame("Recommendations"))
        button2.pack()
        button.pack()
'''

class Recommendations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label = tk.Label(self, text="Movie Recommendations", font=TITLE_FONT)
        Label.pack(side="top", fill="x", pady=10)
        your = tk.Label (self, text= "Recommendations for you", fg="RED")
        top = tk.Label (self, text= "Top rated movies", fg ="RED")
        picks = tk.Label (self, text= "Our picks", fg="RED")
        ymovie1 = tk.Label (self, text ="Movie name ")
        ymovie2= tk.Label (self, text ="Movie name ")
        ymovie3 = tk.Label (self, text ="Movie name ")
        ymovie4 = tk.Label (self, text ="Movie name ")
        ymovie5 = tk.Label (self, text ="Movie name ")


        tmovie1 = tk.Label( self , text = sad.final.iloc[0].name)
        tmovie2 = tk.Label(self, text=sad.final.iloc[1].name)
        tmovie3 = tk.Label(self, text=sad.final.iloc[2].name)
        tmovie4 = tk.Label(self, text=sad.final.iloc[3].name)
        tmovie5 = tk.Label(self, text=sad.final.iloc[4].name)

        omovie1 = tk.Label (self, text ="Movie name ")
        omovie2 = tk.Label (self, text ="Movie name ")
        omovie3 = tk.Label (self, text ="Movie name ")
        omovie4 = tk.Label (self, text ="Movie name ")
        omovie5 = tk.Label (self, text ="Movie name ")
        your.pack(anchor = tk.W)
        ymovie1.pack(anchor = tk.W)
        ymovie2.pack(anchor = tk.W)
        ymovie3.pack(anchor = tk.W)
        ymovie4.pack(anchor = tk.W)
        ymovie5.pack(anchor = tk.W)
        top.pack(anchor = tk.W)
        tmovie1.pack(anchor = tk.W)
        tmovie2.pack(anchor = tk.W)
        tmovie3.pack(anchor = tk.W)
        tmovie4.pack(anchor = tk.W)
        tmovie5.pack(anchor = tk.W)
        picks.pack(anchor = tk.W)
        #omovie[1].pack(anchor = tk.W)
        #omovie[2].pack(anchor = tk.W)
        #omovie[3].pack(anchor = tk.W)
        #omovie[4].pack(anchor = tk.W)
        #omovie[5].pack(anchor = tk.W)
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
