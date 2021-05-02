from tkinter import *
from PIL import ImageTk,Image
import tkinter.font as TkFont
from tkinter.filedialog import askopenfilename
from message_box_popup import messagebox_popup

import os
import csv
import pandas as pd



class edit_recipe:
    def __init__(self, parent, dataFrame):
        self.parent = parent
        self.df = dataFrame
        self.bg_color = "blanched almond"
        self.image_path = []
        
    def create_page(self, column):
        self.column = column
        self.ingredient_list = []
        ## get the location of our dataframe
        try:
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        except:
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        recipe_folder = desktop + "/Recipes"
        self.recipe_file = recipe_folder + "/recipes.csv"
        
        self.edit_window = Toplevel(self.parent)
        self.edit_window.attributes("-fullscreen", True)
        self.edit_window.bind("<Escape>", self.exit_screen)
        self.new_messagebox_popup = messagebox_popup(self.edit_window)
        
        self.info_font = TkFont.Font(family="Helvetica", size= 36, weight="bold", underline = True)
        self.label_font = TkFont.Font(family="Helvetica", size= 30, weight="bold", underline = True)
        self.text_font = TkFont.Font(family="Helvetica", size= 30, weight="bold", underline = False)
        self.btn_font = TkFont.Font(family="Helvetica", size= 36, weight="bold", underline = False)
        
        ########### make a scrollable window ###########
        ################################################
        
        # Create A Main Frame
        self.main_frame_1 = Frame(self.edit_window)
        self.main_frame_1.pack(fill=BOTH, expand=1)

        # Create A Canvas
        self.my_canvas_1 = Canvas(self.main_frame_1, bg = self.bg_color)
        self.my_canvas_1.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        self.my_scrollbar_1 = Scrollbar(self.main_frame_1, orient=VERTICAL, command=self.my_canvas_1.yview)
        self.my_scrollbar_1.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas_1.configure(yscrollcommand=self.my_scrollbar_1.set)
        self.my_canvas_1.bind('<Configure>', lambda e: self.my_canvas_1.configure(scrollregion = self.my_canvas_1.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame_1 = Frame(self.my_canvas_1, bg = "blanched almond")
        self.my_canvas_1.create_window((0,0), window=self.second_frame_1, anchor="nw")
        
        #select our recipe info
        self.selected_recipe = self.df[self.df.columns[column]]
        
        
        ########### DELETE RECIPE ##################
        ############################################
        delete_btn = Button(self.second_frame_1, text = " Delete Recipe ", fg = 'Red',
                                font = self.btn_font, command = self.delete_recipe,
                             width = 15, height = 2)
        delete_btn.grid(row = 0, column = 1, ipadx = 2, ipady = 2, padx = 2, pady = 2)
       
       
        ########### RECIPE NAME ####################
        ############################################
        name_frame= Frame(self.second_frame_1, bg = self.bg_color)
        name_frame.grid(row = 0, column = 0, pady = 10, padx = 5, sticky = "nw")
        self.recipe_label = Label(name_frame, text = " Recipe Name: ", bg = self.bg_color,
                                  font = self.text_font).grid(row = 0, column = 0,
                                                              padx = 5, pady = (0, 2),
                                                                sticky = 'ew')
        self.recipe_name = StringVar()
        self.recipe_name_entry = Entry(name_frame, textvariable = self.recipe_name, 
                                       font = self.text_font).grid(row = 0, column = 1,
                                                                   padx = 5, pady = (0, 2),
                                                                   sticky = 'ew')
        self.ingredient_frame = Frame(self.second_frame_1, bg = self.bg_color,
                                          highlightcolor="black", highlightthickness=2, highlightbackground="black")
        self.recipe_name.set(str(self.df.columns[column]))
        
        ########## selection box for dish type #################
        ####################################################################
        type_frame = Frame(self.second_frame_1, bg = self.bg_color)
        type_frame.grid(row = 1, column=0, sticky = 'nw', padx = (5, 2))
        self.dishtype = StringVar(self.second_frame_1, str(self.selected_recipe.iloc[0]))
        # Dictionary to create multiple buttons 
        values = {"Breakfast" : "Breakfast", 
                    "Appetizer" : "Appetizer", 
                    "Entree" : "Entree", 
                    "Dessert" : "Dessert"} 
  
        # Loop is used to create multiple Radiobuttons 
        # rather than creating each button separately
        x = 0
        for (text, value) in values.items(): 
            Radiobutton(type_frame, text = text, variable = self.dishtype,  
                    value = value,background = self.bg_color).grid(row = 2, column = x,
                                                                padx = 5, pady = 2)
            x = x+1
        
        ############## description box ##############
        ############## ############## ############## ############## 
        description_frame = Frame(self.second_frame_1, bg = self.bg_color,
                                  highlightbackground="black", highlightcolor="black", highlightthickness=2)
        description_frame.grid(row = 3, column = 0, pady = 1, padx = 5, sticky = 'nw')
        
        self.description_label = Label(description_frame,
                                  text = "Recipe Description/Instructions: ",
                                  font = self.info_font, bg = self.bg_color).grid(row =0, column =0, sticky = 'nw')
        self.description_box = Text(description_frame, width= 75,
                               height = 25)
        self.description_box.grid(row = 1, column = 0,
                                                  padx = 5, pady = 5, sticky = 'nw')
        #insert the description text
        self.description_box.insert('1.0', str(self.selected_recipe.iloc[1]))
        
        
        ## add a save button
        save_recipe = Button(self.second_frame_1, text = " Update Recipe ", fg = 'green',
                                font = self.btn_font, command = self.save_updated_recipe,
                             width = 15, height = 3)
        save_recipe.grid(row = 4, column = 0, ipadx = 2, ipady = 2, padx = 5, sticky = 'nw', pady = 2)
        
        
        #### add image button
        try:
            self.add_image_img = PhotoImage(file = str(self.selected_recipe.iloc[3]))
        except:
            self.add_image_img = PhotoImage(file = "/Users/Alexander/Documents/Thonny_Projects/Recipe_book/insert_button.png")
        self.add_image = Button(self.second_frame_1, 
                                image = self.add_image_img, 
                                font = self.info_font, command = self.add_image_btn)
        self.add_image.grid(row = 2, column = 0, sticky = 'nw', padx = 5)
        
        ### paste the ingredient list 
        self.paste_ingredients()
        
    def save_updated_recipe(self):  
        window = self.new_messagebox_popup.call_popup("Are you sure you want to Save??")
        if window:
            ### locate all the recipe info
            self.description = self.description_box.get("1.0",END)
            self.new_recipe_name_type = self.recipe_name.get()
            self.type = self.dishtype.get()
            
            ## actually save it 
            new_one = pd.DataFrame([[self.type],
                                    [self.description],
                                    [",".join(self.ingredient_list)],
                                    [self.image_path]])
            
            self.df[self.new_recipe_name_type] = new_one
    
            self.df.to_csv(self.recipe_file, index = False, mode = 'w')
            
            
            self.exit_screen(None)
            
    def add_image_btn(self):
        self.new_image = askopenfilename(title='Please select one: ',
                           filetypes=[('Image Files', ['.jpeg', '.jpg', '.png',
                                                       '.tiff', '.tif', '.bmp'])])
        image_size = 200, 150
        self.image_path = self.new_image
        self.im = Image.open(self.image_path)
        self.im.thumbnail(image_size, Image.ANTIALIAS)
        self.recipe_image = ImageTk.PhotoImage(self.im)
        #self.recipe_image = PhotoImage(file = self.new_image)
        self.add_image.configure(image = self.recipe_image) 
        self.image_path = str(self.new_image)

    
    def update_ingredients(self):
        self.ingredient_list = []
        ######## do something like this to get the non empty entries for incredients
        for x in range(len(self.entry_variable)):
            self.ingredient_list += [str(self.entry_variable[x].get())]
            
        #save string of new values then repaste the ingredients
        self.ingredient_list = str(",".join(string for string in self.ingredient_list if len(string) > 0))
        
        
        self.paste_ingredients()
        
        
    def paste_ingredients(self):
        
        
        self.ingredient_frame.destroy()
       
        
        ############### Recipe Ingredients and directions ##############
        ############## ############## ############## ##############
        self.new_ingredient = StringVar()
        self.ingredient_frame = Frame(self.second_frame_1, bg = self.bg_color,
                                          highlightcolor="black", highlightthickness=2, highlightbackground="black")
        self.ingredient_frame.grid(row = 1, column = 1, rowspan =6, sticky = 'nwse', pady = 3, padx = 20)
        
        add_ingredient_lbl = Label(self.ingredient_frame, text ="Ingredients:",
                                    font = self.label_font, bg = self.bg_color).grid(row = 0, column = 0, columnspan = 2,
                                                                padx = 5, pady =1, ipadx = 3,
                                                                 ipady = 3, sticky = 'ew')
        add_ingredient_btn = Button(self.ingredient_frame, text = " Add Ingredient: ",
                                    font = self.label_font, bg = self.bg_color,
                                    command = self.add_ingredients).grid(row = 1, column= 0,
                                                                            pady = 1, ipadx = 3,
                                                                            ipady = 3, sticky = 'ew')
        
        add_ingredient_entry = Entry(self.ingredient_frame, textvariable = self.new_ingredient,
                                     font = self.label_font).grid(row = 1, column = 1,
                                                                 ipadx = 3, ipady = 3,
                                                                 pady = 1, padx = 10, sticky = 'ew')
        
        update_btn = Button(self.ingredient_frame, text ="Update Ingredients", font = self.label_font,
                                    command = self.update_ingredients).grid(row = 2, column = 0, columnspan = 2,
                                                                padx = 2, pady =1, ipadx = 3, ipady = 3, sticky = 'ew')
        
        
        self.ingredient_list = str(self.selected_recipe.iloc[2]).split(",")
        self.entry_variable = list(range(len(self.ingredient_list)))
        
        
        x = 1
        for labels in self.ingredient_list:
            self.entry_variable[x-1] = StringVar()
            
            ingredient_entry = Entry(self.ingredient_frame,
                                     textvariable = self.entry_variable[x-1],
                                     width = 40).grid(row =x+2,column = 0, columnspan = 2,
                                                                     sticky = 'n',
                                                                     padx = 1, pady = 2)
                
            self.entry_variable[x-1].set(labels)
                
            x+=1
            self.entry_length = x
            
    def add_ingredients(self):
        self.selected_recipe.iloc[2] += "," + self.new_ingredient.get()
        self.paste_ingredients()
    
    def delete_recipe(self):
        # delete the correpsonding col then save the df and quit window
        
        window = self.new_messagebox_popup.call_popup("Are you sure you want to quit??")
        if window:
            self.df = self.df.drop([str(self.df.columns[self.column])], axis=1) 
            self.df.to_csv(self.recipe_file, index = False, mode = 'w')
            self.parent.destroy()
            
    def exit_screen(self, _event):
        # check to see if user wants to quick out of program
        window = self.new_messagebox_popup.call_popup("Are you sure you want to quit??")
        if window:
            self.edit_window.quit()
            self.edit_window.destroy()