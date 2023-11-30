import pymongo
from customtkinter import *

app = CTk();
app.geometry("1366x768")

app.columnconfigure((0,1,2), weight=1)
app.rowconfigure((0,1,2,3,4), weight=1)

app.title("Keam College Predictor 2024")

# Connect MongoDB.
connect = pymongo.MongoClient("mongodb://localhost:27017")

#Toggle mode
def toggle_mode():
    global mode_value
    if(mode_value == True):
        mode_button.configure(text="Light Mode",text_color="black",fg_color="white")
        app.configure(bg_color="#707370")
        frame1.configure(fg_color="#171710")
        frame2.configure(fg_color="#595E60")
        frame3.configure(fg_color="#B0B7C0")
        main_title.configure(text_color="white")
        your_rank_title.configure(text_color="white")
        result.configure(text_color="white")
        result_head.configure(text_color="white")
        mode_value = False
    else:
        mode_button.configure(text="Dark Mode",text_color="white",fg_color="black")
        app.configure(bg_color="white")
        frame1.configure(fg_color="#36EEE0")
        frame2.configure(fg_color="#4C5270")
        frame3.configure(fg_color="#BCECE0")
        main_title.configure(text_color="black")
        your_rank_title.configure(text_color="black")
        result.configure(text_color="black")
        result_head.configure(text_color="black")
        mode_value = True


# Function list colleges
def reset_list():
    result.configure(text=" ")

def process_list(my_colleges,pr_branch):
    max_length = int(slider_var.get())
    for i in range(min(max_length,len(my_colleges))):
        result_head.configure(text="Top ranked Engineering Colleges for your Rank\n\n")
        data = my_colleges[i]
        print(data['name'] ,"last rank: ",data[pr_branch])
        current_text = result.cget("text")
        new_text = current_text + data['name'] +  ",     CuttOff Rank : "+ str(data[pr_branch]) + "\n\n"
        result.configure(text=new_text)
        

def list_colleges(my_connect):
    my_rank = int(rank_input.get())
    rank_title_update = "Your Rank is " + rank_input.get()
    your_rank_title.configure(text=rank_title_update)
    my_choice = comboBox.get();
    pr_branch = ""
    match my_choice:
        case "Computer Science Engineering":
            pr_branch = "cslastrank"
        case "Electrical & Communication Engineering":
            pr_branch = "eclastrank"
        case "Electrical & Electronics Engineering":
            pr_branch = "eelastrank"
        case "Civil Engineering":
            pr_branch = "celastrank"
        case "Mechanical Engineering":
            pr_branch = "melastrank"
    db = my_connect["colleges"]
    collegelist = db["college"]
    cond_college = {pr_branch: {'$gt' : my_rank }}
    my_colleges = list(collegelist.find(cond_college).sort({pr_branch: 1}))
    process_list(my_colleges,pr_branch)

    #for i in find_record:
        #print(i['name'] ,"last rank: ",i[pr_branch])
       # current_text = result.cget("text")
       # new_text = current_text + i['name'] +"\n"
       # result.configure(text=new_text)
        
def sliding(value):
    slider_text = "Top " + str(int(value)) + " Colleges"
    slider_label.configure(text=slider_text)

# Frames 
frame1 = CTkFrame(master=app,fg_color="#36EEE0",width=1366,height=153,border_width=3,border_color="white")
frame1.grid(row=0,column=0,columnspan=3)
frame2 = CTkFrame(master=app,width=455,height=459,fg_color="#4C5270",border_width=3,border_color="white")
frame2.grid(row=1,column=0,rowspan=4,sticky="nwes")
frame3 = CTkScrollableFrame(master=app,width=910,height=612,fg_color="#BCECE0",border_width=3,border_color="white")
frame3.grid(row=1,column=1,rowspan=4,columnspan=2)



# Main Title
main_title = CTkLabel(master=frame1,text="Keam College Predictor",text_color="black",font=("Comic Sans MS",60))
main_title.place(relx=0.5,rely=0.4,anchor="center")
your_rank_title = CTkLabel(master=frame1,text=" ",text_color="black",font=("Arial",15))
your_rank_title.place(relx=0.5,rely=0.8,anchor="center")
# Rank Input
sub_head_label = CTkLabel(master=frame2,text="KEAM College Predictor",text_color="white",font=("Arial",10))
sub_head_label.pack(padx=10,pady=10)
rank_input = CTkEntry(master=frame2,placeholder_text="Enter your Keam Rank here",width=300,height=30)
#rank_input.place(relx=0.5,rely=0.5,anchor="center")
rank_input.pack(padx=10,pady=10)

# Radio Input
radio_label = CTkLabel(master=frame2,text="Select Your Prefered Branch",text_color="white",font=("Arial",15))
#radio_label.place(relx=0.5,rely=0.3,anchor="center")
radio_label.pack(padx=10,pady=10)
comboBox = CTkComboBox(master=frame2,text_color="white",values=["Computer Science Engineering","Electrical & Electronics Engineering","Electrical & Communication Engineering","Civil Engineering","Mechanical Engineering"])
comboBox.pack(padx=8,pady=8)

# Slider
slider_label = CTkLabel(master=frame2,text=" ",text_color="white",font=("Helvetica", 15))
slider_label.pack()
slider_var = DoubleVar()
slider = CTkSlider(master=frame2,variable=slider_var,from_=1,to=50,command=sliding)
slider.pack()
slider.set(1)

# Submit button.
btn = CTkButton(master=frame2,text="Submit",corner_radius=32,command=lambda: list_colleges(connect),fg_color="#C850C0",hover_color="#4158D0")
btn.pack(padx=10, pady=10)
reset_btn = CTkButton(master=frame2,text="Reset",corner_radius=32,command=reset_list,fg_color="#C850C0",hover_color="#4158D0")
reset_btn.pack(padx=10,pady=10)

# Dark mode/ Light Mode
mode_button = CTkButton(frame2,text="Dark Mode",text_color="white",corner_radius=32,command=toggle_mode,fg_color="black",hover_color="gray")
mode_button.pack();
mode_value = True



# Result 
result_head = CTkLabel(master=frame3,text=" ",text_color="black",font=("Comic Sans MS",25))
result_head.pack()
result = CTkLabel(master=frame3,text="",text_color="black",font=("Arial",20))
result.pack()


app.mainloop()