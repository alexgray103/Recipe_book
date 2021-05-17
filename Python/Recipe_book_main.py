from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as TkFont
from Add_recipe_window import recipe_functions


root = Tk()
global fullscreen_handler
fullscreen_handler = True
helv36 = TkFont.Font(family="Helvetica", size=72, weight="bold")
button_font = TkFont.Font(family="Helvetica", size=36, weight="bold")

add_recipe_window = recipe_functions(root)


def toggle_fullscreen(_event):
    global fullscreen_handler
    fullscreen_handler = not fullscreen_handler
    root.attributes('-fullscreen', fullscreen_handler)


root.bind("<Escape>", toggle_fullscreen)

root.title("Lisa's Recipe Book")
root.geometry("600x600")

root.attributes('-fullscreen', fullscreen_handler)  # fullscreen on touchscreen

root.configure(bg="sky blue")
root.minsize(800, 480)  # min size the window can be dragged to

root.grid_columnconfigure((0), weight=1)
root.grid_rowconfigure((0, 1, 2), weight=1)

# put an image in there
image_size = 1500, 1500

# make a frame for our image and
title = "Lisa Gray's Amazing Cookbook"
title_label = Label(root, text=title, bg="sky blue", fg="black", font=helv36)
title_label.grid(row=0, column=0, sticky="nsew")
canvas_frame = Frame(root, bg='Sky blue')
canvas_frame.grid(row=1, column=0, sticky='nsew')
# title label into the main page
canvas = Canvas(canvas_frame, bg="sky blue")
canvas.pack(fill=BOTH, expand=True)

im = Image.open("/Users/Alexander/Documents/Thonny_Projects/Recipe_book/cooking_image.jpeg")
im.thumbnail(image_size, Image.ANTIALIAS)
img = ImageTk.PhotoImage(im)

canvas.create_image(700, 100, anchor=CENTER, image=img)

## create all buttons for different types of food
menu_button_frame = Frame(root, bg="sky blue")
menu_button_frame.grid(row=2, column=0)
menu_button_height = 3
menu_button_width = 5
menu_padding = 15


#### create the menu ##########
###############################
size = (200, 200)

#image = Image.open("/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")
image = Image.open("/Users/Alexander/Documents/Thonny_projects/Recipe_book/insert_button.png")

new = image.resize((200,150), Image.ANTIALIAS)
add_new_image =  ImageTk.PhotoImage(new)


#add_new_image = PhotoImage(file="/Users/Alexander/Documents/Thonny_Projects/Recipe_book/insert_button.png").resize(200,200)
# Resizing image to fit on button



new_recipe_btn = Button(menu_button_frame, image=add_new_image, text=" Add Recipe ", bg="sky blue",
                        compound=TOP, font=button_font, borderwidth=0, height=menu_button_height,
                        width=menu_button_width,
                        command=add_recipe_window.add_recipe)
new_recipe_btn.grid(row=0, column=0, padx=menu_padding, pady=menu_padding)

breakfast_image = PhotoImage(file="/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")
breakfast_btn = Button(menu_button_frame, image=breakfast_image, text=" Breakfast ", bg="sky blue",
                       compound=TOP, font=button_font, borderwidth=0, height=menu_button_height,
                       width=menu_button_width, command = lambda: add_recipe_window.open_window("Breakfast"))
breakfast_btn.grid(row=0, column=1, padx=menu_padding, pady=menu_padding)

appetizer_image = PhotoImage(file="/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")
appetizer_btn = Button(menu_button_frame, image=appetizer_image, text=" Appetizer ", bg="sky blue",
                       compound=TOP, font=button_font, borderwidth=0, height=menu_button_height,
                       width=menu_button_width, command = lambda: add_recipe_window.open_window("Appetizer"))
appetizer_btn.grid(row=0, column=2, padx=menu_padding, pady=menu_padding)
entree_image = PhotoImage(file="/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")

entree_btn = Button(menu_button_frame, image=entree_image, text=" Entree ", bg="sky blue",
                    compound=TOP, font=button_font, borderwidth=0, height=menu_button_height, width=menu_button_width,
                    command = lambda: add_recipe_window.open_window("Entree"))
entree_btn.grid(row=0, column=3, padx=menu_padding, pady=menu_padding)

dessert_image = PhotoImage(file="/Users/Alexander/Documents/Thonny_Projects/Recipe_book/Entree_image.png")
dessert_btn = Button(menu_button_frame, image=dessert_image, text=" Dessert ", bg="sky blue",
                     compound=TOP, font=button_font, borderwidth=0, height=menu_button_height, width=menu_button_width,
                     command = lambda: add_recipe_window.open_window("Dessert"))
dessert_btn.grid(row=0, column=4, padx=menu_padding, pady=menu_padding)

add_new_recipe = Button(menu_button_frame, text = "Create Recipe", bg = "sky blue", font = button_font,
                        height = 3, command = add_recipe_window.add_recipe_online)
add_new_recipe.grid(row=1, column=0, columnspan = 5, padx=menu_padding, pady=menu_padding, sticky = 'nsew')
##### resize all buttons depending on the window size
menu_button_frame.grid_columnconfigure((0, 1), weight=1)
menu_button_frame.grid_rowconfigure((0), weight=1)

if __name__ == "__main__":
    root.mainloop()

