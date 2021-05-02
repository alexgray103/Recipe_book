from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as TkFont
import pandas as pd
from recipe_scrapers import scrape_me

# allows to get images and stuff
import requests # to get image from the web
import shutil # to save it locally
import os

# Recipe Functions
class recipe_functions:
    def __init__(self, parent):
        self.master = parent
        self.chef_name = "Algray103"
        self.csv_location = '/Users/Alexander/Desktop/Recipe_book/Recipes.csv'
        
        self.df = pd.read_csv(self.csv_location, encoding = "ISO-8859-1", index_col = 0)
        self.recipe_handler = []
        
        # create all the fonts needed for the recipe window
        self.helv72 = TkFont.Font(family="Helvetica", size=72, weight="bold")
        self.helv15 = TkFont.Font(family="Helvetica", size=26, weight="bold")
        
    
    def open_window(self, recipe_type):
        self.window = Toplevel(self.master)
        
        self.type = recipe_type
        
        self.window.configure(bg="blanched almond")
        self.window.bind("<Escape>", self.exit_screen)
        self.window.attributes('-fullscreen', True)
        
        # Create A Main Frame
        self.main_frame = Frame(self.window)
        self.main_frame.pack(fill=BOTH, expand=1)
        
        self.background_color = "blanched almond"
        self.dark_background = 'sky blue'
        
        # Create A Canvas
        self.my_canvas = Canvas(self.main_frame, bg = self.background_color)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        self.my_scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)

        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))
        self.my_canvas.bind_all("<Down>",  lambda event: self.my_canvas.yview_scroll(1, "units"))
        self.my_canvas.bind_all("<Up>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind_all("<Button-4>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind_all("<Button-5>", lambda event: self.my_canvas.yview_scroll(1, "units"))
        
        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame = Frame(self.my_canvas, bg = self.background_color)
        
        self.my_canvas.focus_set()
       
       # Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        
        #### start to create all of the buttons and stuff based on the recipe type
        title_lbl = Label(self.second_frame, text = str(self.type), font = self.helv72)
        title_lbl.grid(row= 0, column = 0, columnspan = 4, padx = 2, pady = 2, sticky = 'nsew')
        
        ### allow up to 250 elements in the recipes page
        self.recipe_frame = list(range(250)) 
        self.item_btn = list(range(250))
        self.btn_image = list(range(250))
        self.item_lbl = list(range(250))
        
        # get the number of rows for that type of recipe.
        self.row = len(self.df.index)
        typed = self.df.iloc[0,:]
        
        #Find all recipes for the specific button
        for x in range(len(self.df.columns)):
            if str(self.df.iloc[0,x]) == self.type:
                self.recipe_handler += [x]
        
        # start to create the actual recipe book 
        r = 1
        c = 0
        
        for x in range(len(self.recipe_handler)):
            
            print(self.df.iloc[1,self.recipe_handler[x]])
            self.recipe_frame[x] = Frame(self.second_frame, bg = self.background_color)
            self.recipe_frame[x].grid(row = r, column = c, sticky = "nsew", padx = 1, pady = 1)
            
            #get image
            image = Image.open("/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")
            new = image.resize((200,150), Image.ANTIALIAS)
            self.btn_image[x] =  ImageTk.PhotoImage(new)
            
            self.item_btn[x] = Button(self.recipe_frame[x], image = self.btn_image[x])
            self.item_btn[x].grid(row = 0, column = 0, sticky = 'nsew', padx = 1, pady = 1)
            
            self.item_lbl[x] = Label(self.recipe_frame[x], text = self.df.iloc[1,self.recipe_handler[x]])
            self.item_lbl[x].grid(row = 1, column = 0, sticky = 'nsew', padx=1, pady=1)
        
        
        
        button_width = 4
        padding = 12
        button_height = 1
        
        
    def add_recipe(self):
        self.new_recipe_window = Toplevel(self.master)
        self.new_recipe_window.attributes('-fullscreen', True)
        self.new_recipe_window.configure(bg="sky blue")
        self.new_recipe_window.bind("<Escape>", self.exit_add_window)
        
        label = Label(self.new_recipe_window, text = "Find Online Recipe Here:", font = self.helv15)
        label.grid(row = 0, column = 0, columnspan = 2)
        
    
        self.url_btn = Button(self.new_recipe_window, text = "Find Recipe", command = self.scrape_recipe, height = 3, width = 50)
        self.url_btn.grid(row = 1, column = 0, padx = 4, pady = 2)
        
        self.recipe_url = StringVar()
        self.entry = Entry(self.new_recipe_window, textvariable = self.recipe_url, width = 100)
        self.entry.grid(row = 1, column = 1, padx = 2, pady = 2, sticky = 'nsew')
        
        radio_frame = Frame(self.new_recipe_window, bg = "sky blue")
        radio_frame.grid(row = 2, column = 0, columnspan = 2, sticky = 'nsew')
        
        languages = [("Appetizer", "Appetizer"),("Breakfast", "Breakfast"),("   Entree  ", "Entree"),
                    (" Dessert ", "Dessert")]
        self.recipe_type_var = StringVar()
        self.recipe_type_var.set("Appetizer")
        

        Label(radio_frame, 
                 text="""Choose your Recipe Type:""",
                 justify = LEFT,
                 padx = 20).pack()

        for language, val in languages:
            Radiobutton(radio_frame, bg = "sky blue",
                           text=language,
                           padx = 20, 
                           variable=self.recipe_type_var, 
                           value=val).pack()

        
        internal = 4
        self.inventory_needed = []
    
    def scrape_recipe(self):
        try:
            scraper = scrape_me(str(self.recipe_url.get()))
            filename = self.get_image(scraper.image(), scraper.title()) # save the image to proper directoy
            temp_list = pd.DataFrame([self.recipe_type_var.get(), ','.join(scraper.ingredients()), scraper.instructions(),
                                      filename,  self.chef_name, str(self.recipe_url.get())], columns = [str(scraper.title())])
            self.df.insert(1, str(scraper.title()), [self.recipe_type_var.get(), ','.join(scraper.ingredients()), scraper.instructions(),
                     filename,  self.chef_name, str(self.recipe_url.get())], True)
            self.df.to_csv(self.csv_location, mode = 'w', index = False)
                         
        except:
            self.error_window()
            
    def error_window(self):
        error_top = Toplevel(self.new_recipe_window)
        error_top.geometry("600x100")
        error_top.configure(background = "sky blue")
        message = Label(error_top, text = "Could not locate the Recipe, Please check URL or try different website",
                        font = self.helv15, wraplength = 600, bg = "sky blue")
        message.grid(row = 0, column = 0, padx = 10)
        
        error_top.after(3000, self.new_recipe_window.destroy)
        
    
    def get_image(self, url, title):
  
        pathname_tuple = os.path.splitext(url)
        file_extension = pathname_tuple[1]
        
        ## Set up the image URL and filename
        image_url = url
        filename = "/Users/Alexander/Documents/Thonny_Projects/Recipe_book/" + str(title) + str(file_extension)
        filename = filename.replace(" ", "")
        
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
            print('Image sucessfully Downloaded: ',filename)
            
        else:
            print('Image Couldn\'t be retreived')
            filename = "Not located"
            
        return filename
    def exit_add_window(self, _event):
        self.new_recipe_window.quit()
        self.new_recipe_window.destroy()
        
    def exit_screen(self, _event):
        self.window.quit()
        self.window.destroy()