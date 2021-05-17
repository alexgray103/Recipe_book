from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as TkFont
import pandas as pd
from recipe_scrapers import scrape_me
from tkinter.filedialog import askopenfilename

### create pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import Image as pdfImage
from reportlab.platypus import SimpleDocTemplate
import textwrap

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
        self.pdf_location = '/Users/Alexander/Desktop/Recipe_book/Recipes.pdf'
        
        self.df = pd.read_csv(self.csv_location, encoding = "ISO-8859-1")
        self.recipe_handler = []
        self.df = self.df.sort_index(axis = 1)
        # create all the fonts needed for the recipe window
        self.helv72 = TkFont.Font(family="Helvetica", size=72, weight="bold")
        self.helv15 = TkFont.Font(family="Helvetica", size=26, weight="bold")
        self.recipe_title = TkFont.Font(family="Helvetica", size=72, weight="bold", underline = True)
        self.labels = TkFont.Font(family="Helvetica", size=30, weight="bold", underline = True)
    
    def open_window(self, recipe_type):
        self.recipe_handler = []
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
        self.my_canvas.bind("<Down>",  lambda event: self.my_canvas.yview_scroll(1, "units"))
        self.my_canvas.bind("<Up>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind("<Button-4>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind("<Button-5>", lambda event: self.my_canvas.yview_scroll(1, "units"))
        
        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame = Frame(self.my_canvas, bg = self.background_color)
        
        self.my_canvas.focus_set()
       
       # Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        
        
        back_btn = Button(self.second_frame, text = "Back", fg = "red", command = lambda: self.exit_screen(None), font = self.helv15)
        back_btn.grid(row= 0, column = 0, padx = 80, pady = 2, sticky = 'nsew')
        #### start to create all of the buttons and stuff based on the recipe type
        title_lbl = Label(self.second_frame, text = str(self.type), font = self.helv72)
        title_lbl.grid(row= 1, column = 0, padx = 80, pady = 2, sticky = 'nsew')
        
        
        total_frame = Frame(self.second_frame, bg = "blanched almond")
        total_frame.grid(row = 2, column = 0, padx = 80, pady = 2, sticky = 'nsew')
        
        ### allow up to 250 elements in the recipes page
        self.recipe_frame = list(range(250)) 
        self.item_btn = list(range(250))
        self.btn_image = list(range(250))
        self.item_lbl = list(range(250))
        
        # get the number of rows for that type of recipe.
        self.row = len(self.df.index)
        typed = self.df.iloc[0,:]
        
        #Find all recipes for the specific button
        for y in range(len(self.df.columns)):
            if str(self.df.iloc[0,y]) == self.type:
                self.recipe_handler += [y]
        
        # start to create the actual recipe book 
        r = 2
        c = 0
        
        x = 0
        for val in self.recipe_handler:
            print(self.df.columns[val])
            self.recipe_frame[x] = Frame(total_frame, bg = self.background_color)
            self.recipe_frame[x].grid(row = r, column = c, sticky = "nsew", padx = 25, pady = 1)
            
            try:
                location = self.df.iloc[3,val]
                #get image
                image = Image.open(location)
                new = image.resize((200,150), Image.ANTIALIAS)
                self.btn_image[x] =  ImageTk.PhotoImage(new)
            except:
                location = "/Users/Alexander/Documents/Thonny_projects/Recipe_book/insert_button.png"
                #get image
                image = Image.open(location)
                new = image.resize((200,150), Image.ANTIALIAS)
                self.btn_image[x] =  ImageTk.PhotoImage(new)
            
            self.item_btn[x] = Button(self.recipe_frame[x], image = self.btn_image[x],
                                      command = lambda val=val: self.open_recipe(self.df.columns[val]))
            self.item_btn[x].grid(row = 0, column = 0, sticky = 'nsew', padx = 1, pady = 1)
            
            self.item_lbl[x] = Label(self.recipe_frame[x], text = self.df.columns[val])
            self.item_lbl[x].grid(row = 1, column = 0, sticky = 'nsew', padx=1, pady=1)
            
            c+=1
            if c >5:
                c=0
                r+=1
            x +=1
        button_width = 4
        padding = 12
        button_height = 1
        
    def open_recipe(self, recipe_name):
        self.recipe_window = Toplevel(self.window, background = "blanched almond")
        self.recipe_window.attributes('-fullscreen', True)
        self.recipe_window.bind("<Escape>", self.exit_recipe_window)
        
        self.recipe = self.df[[str(recipe_name)]]
        # Create A Main Frame
        self.main_frame_1 = Frame(self.recipe_window)
        self.main_frame_1.pack(fill=BOTH, expand=1)
        # Create A Canvas
        self.my_canvas_1 = Canvas(self.main_frame_1, bg = self.background_color)
        self.my_canvas_1.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        self.my_scrollbar_1 = Scrollbar(self.main_frame_1, orient=VERTICAL, command=self.my_canvas_1.yview)
        self.my_scrollbar_1.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas_1.configure(yscrollcommand=self.my_scrollbar_1.set)

        self.my_canvas_1.bind('<Configure>', lambda e: self.my_canvas_1.configure(scrollregion = self.my_canvas_1.bbox("all")))
        self.my_canvas_1.bind("<Down>",  lambda event: self.my_canvas_1.yview_scroll(1, "units"))
        self.my_canvas_1.bind("<Up>", lambda event: self.my_canvas_1.yview_scroll(-1, "units"))
        self.my_canvas_1.bind("<Button-4>", lambda event: self.my_canvas_1.yview_scroll(-1, "units"))
        self.my_canvas_1.bind("<Button-5>", lambda event: self.my_canvas_1.yview_scroll(1, "units"))
        
        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame_1 = Frame(self.my_canvas_1, bg = self.background_color)
        
        self.my_canvas_1.focus_set()
       
       # Add that New frame To a Window In The Canvas
        self.my_canvas_1.create_window((0,0), window=self.second_frame_1, anchor="nw")
        
        self.back_btn = Button(self.second_frame_1, text = "Back", fg = "Red", height = 3, width = 35,
                               command = self.recipe_window.destroy, font = self.helv15)
        self.back_btn.grid(row = 0, column = 0, sticky = 'nw')
        
        self.edit_btn = Button(self.second_frame_1, text = "Edit Recipe", fg = "Red", height = 3, width = 35,
                               command = lambda: self.edit_window( self.recipe), font = self.helv15)
        self.edit_btn.grid(row = 0, column = 1, sticky = 'ne')
        
        self.recipe_label = Label(self.second_frame_1, text = self.recipe.columns[0],
                                  bg = self.background_color, font = self.recipe_title)
        self.recipe_label.grid(row = 1, column = 0, padx = 5, pady = 10)
        
        self.email_recipe = Button(self.second_frame_1, text = "Email Recipe", fg = "Red", height = 3, width = 35,
                               command = lambda: self.create_pdf(self.recipe), font = self.helv15)
        self.email_recipe.grid(row = 0, column = 2, sticky = 'nw') 
        
        
        #get image
        image = Image.open(str(self.recipe.iloc[3,0]))
        new = image.resize((400,400), Image.ANTIALIAS)
        self.img =  ImageTk.PhotoImage(new)
        
        self.image_lbl = Label(self.second_frame_1, image = self.img)
        self.image_lbl.grid(row = 2, column = 0, padx = 5, sticky = 'nsew')
        
        self.ingredients_frame =  Frame(self.second_frame_1, bg = self.background_color,
                                    highlightbackground="black", highlightthickness = 1)
        self.ingredients_frame.grid(row = 2, column = 1, rowspan = 2, padx = 40, pady = 5,  sticky = 'NW')
        
        self.text = Label(self.ingredients_frame, text = "                        Ingredients                        ",
                     bg = self.background_color, font = self.labels)
        self.text.pack()
        
        ingred_list = self.recipe.iloc[1,0].split(',')
        self.ingred_txt = list(range(len(ingred_list)))
        for x  in range(len(ingred_list)):
            ingred_txt = "- " + str(ingred_list[x])
            self.ingred_txt[x] = Label(self.ingredients_frame, text= ingred_txt, wraplength = 600,
                                       bg = self.background_color, font = self.helv15)
            self.ingred_txt[x].pack(anchor = NW)
        
        #self.ingred_txt = Label(self.ingredients_frame, text= self.recipe.iloc[1,0], wraplength = 600, bg = self.background_color, font = self.helv15)
        #self.ingred_txt.pack(anchor = NW)
        
        self.description_frame = Frame(self.second_frame_1, bg = self.background_color,
                                  highlightbackground="black", highlightthickness = 1)
        self.description_frame.grid(row = 3, column = 0, pady = 5, padx = 5, sticky = 'nsew')
        
        self.description_label = Label(self.description_frame, text = "                        Instructions:                        ",
                                  bg = self.background_color, font = self.labels)
        self.description_label.pack()
        
        self.description_txt = Label(self.description_frame, text= self.recipe.iloc[2,0], wraplength = 600,
                                     bg = self.background_color, font = self.helv15)
        self.description_txt.pack(anchor = NW)
        
    def edit_window(self, recipe):
        print(recipe)
        
        
    def add_recipe_online(self):
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
            temp_list = [self.recipe_type_var.get(), ','.join(scraper.ingredients()), scraper.instructions(),
                                      filename,  self.chef_name, str(self.recipe_url.get())]
           
            self.df[str(scraper.title())] = temp_list
            
            #self.df.insert(1, str(scraper.title()), [self.recipe_type_var.get(), ','.join(scraper.ingredients()), scraper.instructions(),
                     #filename,  self.chef_name, str(self.recipe_url.get())], True)
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
    
    def add_recipe(self):
        self.add_recipe_window = Toplevel(self.master, bg = "blanched almond")
        self.add_recipe_window.attributes('-fullscreen', True)
        self.add_recipe_window.bind("<Escape>", self.exit_add_recipe_window)
        self.ingredient_list_new = []
        self.lbl_counter = 2
        
        
        ###########################################################################
        recipe_frame = Frame(self.add_recipe_window, bg = "blanched almond",
                             highlightthickness = 2, highlightbackground = "black")
        recipe_frame.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = 'nsew')
        
        
        
        ###########################################################################
        title_lbl = Label(recipe_frame, text = "Recipe Name: ", font = self.helv15)
        title_lbl.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = 'nsew')
        self.title_entry = StringVar()
        self.title = Entry(recipe_frame, width = 20, textvariable =self.title_entry)
        self.title.grid(row = 2, column = 0, pady = 5,padx = 5, sticky = 'nsew')
        
       
       
        ###########################################################################
        #get image
        image = Image.open("/Users/Alexander/Documents/Thonny_projects/Recipe_book/insert_button.png")
        new = image.resize((200,200), Image.ANTIALIAS)
        self.added_image =  ImageTk.PhotoImage(new)
        
        self.add_photo_location = Button(recipe_frame, text = "ADD PHOTO", image = self.added_image,
                                         command = self.add_photo)
        self.add_photo_location.grid(row = 3, column = 0, padx = 5)
        
        
        ###########################################################################
        descr_lbl = Label(recipe_frame, font = self.helv15, text = "Description:")
        descr_lbl.grid(row = 4, column = 0, sticky = 'nsew',padx = 5, pady = (20,2))
        self.description_text = Text(recipe_frame, height = 20, width = 100)
        self.description_text.grid(row = 5, column = 0, padx = 5, pady =5, sticky = 'nsew')
        
        
        ###########################################################################
        self.ingredient_frame = Frame(recipe_frame, bg = 'blanched almond')
        self.ingredient_frame.grid(row = 0, column = 1, rowspan = 6, padx = 50, pady =5, sticky = 'nsew')
        ingred_lbl = Label(self.ingredient_frame, text = "Ingredients:", font = self.helv15)
        ingred_lbl.grid(row = 0, column = 0, pady = 5, sticky = 'nsew', columnspan = 2)
        
        add_ingredient = Button(self.ingredient_frame, text = "Add Ingredient",
                                command = self.add_ingredient, font = self.helv15)
        add_ingredient.grid(row = 1, column = 0, pady = 5, sticky = 'nsew')
        
        self.get_ingred = StringVar()
        ingred_entry = Entry(self.ingredient_frame, textvariable = self.get_ingred, width = 30)
        ingred_entry.grid(row = 1, column = 1, pady = 5, sticky = 'nsew')
        
        
        ###########################################################################
        save_recipe = Button(self.add_recipe_window, text = "Save Recipe", height = 3, width = 40, font = self.helv15,
                             command = self.save_recipe)
        save_recipe.grid(row = 0, column = 0, pady = 30, padx = 5, sticky = 'nsew')
        
        
        ###########################################################################
        radio_frame = Frame(recipe_frame, bg = "blanched almond")
        radio_frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        languages = [("Appetizer", "Appetizer"),("Breakfast", "Breakfast"),("Entree", "Entree"),
                    ("Dessert", "Dessert")]
        self.recipe_type_new = StringVar()
        self.recipe_type_new.set("Appetizer")
        

        Label(radio_frame, 
                 text="""Choose your Recipe Type:""",
                 justify = LEFT,
                 padx = 20).pack()

        for language, val in languages:
            Radiobutton(radio_frame, bg = "blanched almond",
                           text=language,
                           padx = 20, 
                           variable=self.recipe_type_new, 
                           value=val).pack(side = LEFT, anchor = W)
        self.recipe_type_new
        
    def add_ingredient(self):
        self.ingredient_list_new += [self.get_ingred.get()]
        lbl_str = '- ' + self.get_ingred.get() 
        self.label = Label(self.ingredient_frame, text = lbl_str, bg = 'blanched almond')
        self.label.grid(row = self.lbl_counter, column = 0, columnspan = 2, padx = 1, sticky = 'nw')
        
        self.add_recipe_window.update()
        self.add_recipe_window.update_idletasks()
        self.lbl_counter = self.lbl_counter + 1
        
        
    def add_photo(self):
        try:
            self.image_location_new = askopenfilename(initialdir="/Users/Alexander/Documents/Thonny_projects/Recipe_book/",
                                    filetypes =(("JPEG file", "*.jpg"),("PNG file", "*.png"),("All Files","*.*")),
                                    title = "Choose a file.")
            image = Image.open(self.image_location_new)
            new = image.resize((200,200), Image.ANTIALIAS)
            self.added_image =  ImageTk.PhotoImage(new)
            self.add_photo_location.config(image = self.added_image)
        except:
            pass
    
    def save_recipe(self):
        temp_list = [self.recipe_type_new.get(), ','.join(self.ingredient_list_new), self.description_text.get(1.0, "end-1c"),
                                      self.image_location_new,  self.chef_name, "Homemade Recipe"]
        
        
        self.df[self.title_entry.get()] = temp_list
        self.df.to_csv(self.csv_location, mode = 'w', index = False)
        
    def create_pdf(self, recipe):
        # help to wrap words to the page size 
        wrapper = textwrap.TextWrapper(width=80)
        pdf = canvas.Canvas(self.pdf_location, pagesize = letter)
        
        pdf.setFont('Helvetica-Bold', 48)
        pdf.drawCentredString(300, 700, str(recipe.columns[0]))
        
        
        pdf.drawImage(recipe.iloc[3,0], 50, 350, width=500,height=300,mask='auto', anchor= 'c')
        
        label_txt = 'Document Created By: Alex Grays Recipe App'
        
        pdf.setFont('Helvetica-Bold', 16)
        
        pdf.drawCentredString(300, 300, label_txt)

        
        pdf.drawCentredString(300, 10, "Visit https://github.com/alexgray103/Recipe_book for more information")
        
        ## create description page
        pdf.showPage()
        
        pdf.setFont('Helvetica-Bold', 48)
        pdf.drawCentredString(300, 700, "Description:")
      
          
        # Wrap this text.
        
        wrapper_2 = textwrap.TextWrapper(width=75)
        word_list = wrapper_2.wrap(text=recipe.iloc[2,0])
        
        ### margins for the text
        
        margin = 30
        
        
        y = 675
        pdf.setFont('Helvetica', 16)
        # Print each line.
        for element in word_list:
            pdf.drawString(35, y, element)
            y-=20
            if y<margin:
                pdf.showPage()
                pdf.setFont('Helvetica', 16)
                y = 700
        y -=45
        if y <0:
            pdf.showPage()
            y = 650
        
        
        ## create ingredients page
        pdf.setFont('Helvetica-Bold', 48)
        pdf.drawCentredString(300, y, "Ingredients:")
        y -= 30
        pdf.setFont('Helvetica', 16)
        ingred_list = recipe.iloc[1,0].split(',')
        for ingred in range(len(ingred_list)):
            ingred_txt = "- " + str(ingred_list[ingred])
            pdf.drawString(35, y, ingred_txt)
            y-=margin
            if y<30:
                pdf.showPage()
                pdf.setFont('Helvetica', 16)
                y = 700
        
        pdf.save()
        
    def exit_add_recipe_window(self, event):
        self.add_recipe_window.quit()
        self.add_recipe_window.destroy()
        
    def exit_recipe_window(self, event):
        self.recipe_window.quit()
        self.recipe_window.destroy()
        
    
    def exit_add_window(self, _event):
        self.new_recipe_window.quit()
        self.new_recipe_window.destroy()
        
    def exit_screen(self, _event):
        self.window.quit()
        self.window.destroy()