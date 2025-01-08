import customtkinter as CTk
import openai, json
import clubs, awards, sports, AP, universities
from tkinter import messagebox
from random import SystemRandom
random = SystemRandom() ## Habit of mine to use SystemRandom when possible. 

## First expand, write in as many features into the code as possible
## Then re-org, making the code-base actually readable and consolidating
## bloated code into more optimal code and adding in quality of life 
## changes.

with open("APIKEY.config", 'r') as api_key_file :
    openai.api_key = api_key_file.read()

with open("systemprompt.txt", 'r') as sp :
    systemPrompt = sp.read()

is_dev_version = True
build_tag = "Alpha-1234"

class app() :
    career_path = ["Undecided", "Tech", "Engineering", "Art", "Music", "Business", "Law", "Medical", "Sports", "Other"]

    AP_T1 = [
        "Calculus AB/BC",
        "Physics 1",
        "Physics 2",
        "Physics C E&M/Mechanics",
        "Biology",
        "Chemistry",
    ]

    AP_T2 = [
        "Pre-calculus",
        "Statistics",
        "Pyschology",
    ]

    ## Most APs belong in here. They are generally not that hard but they can definitely be of use.
    AP_T3 = [
        "English Language",
        "English Literature",
        "US Government & Politics",
        "Environmental Science",
        "Chinese",
        "Spanish Language",
        "Spanish Literature",
        "French",
        "Japanese",
        "Latin",
        "Italian",
        "CSA",
        "World History",
        "European History",
        "Macroeconomics",
        "Microeconomics",
        "US History",
    ]

    AP_T4 = [
        "Art History",
        "Music Theory",
        "Research",
        "Seminar",
        "CSP",
        "Comp. Gov. & Politics"
    ]

    AP_T5 = [
        "Art & Design 2D/3D", ## Actual joke of an AP here...
        "Drawing"

    ]

    ALL_APS = AP_T1 + AP_T2 + AP_T3 + AP_T4 + AP_T5
    ALL_APS.sort()

    regions = ["Local/School", "State", "Regional", "National", "International"]

    taken_APs = []
    taken_clubs = []
    taken_sports = []
    awarded_awards = []
    sat_score = 0 

    ## All screen objects, used for screen changing
    all_screen_obj = [] ## This is preparing me for memory management and screen management-- if an item isn't added to this list, it stays on the screen for ever.

    ## GUI color stuff
    bg_color = "#192E45"
    bg_color_light = "#2A4D73"

    app_red = "#E34039"
    app_red_dark = "#75322f"

    app_green = "#44AD4D"
    app_green_dark = "#28482B"

    app_light_blue = "#294D73"

    app_text_color = "#FFFFFF"

    app_text_box_color = "#0F2845"
    border_color = "#1A1A1A"

    black="#000000"
    white="#FFFFFF"

    ## L = 50
    ## H = 35
    ## T = 25
    ## B = 20
    ## S = 15
    large_font = ("Segoe UI", 50) ## Segoe is a nice font
    header_font = ("Segoe UI", 35)
    medium_font = ("Segoe UI", 30)
    text_font = ("Segoe UI", 25)
    button_font = ("Segoe UI", 20)
    sm_font = ("Segoe UI", 17)
    small_font = ("Segoe UI", 15)

    used_act = False

    def __init__(self, app:CTk.CTk) :
        self.app = app
        self.app.title("CounselAI") 
        CTk.set_appearance_mode("dark")
        self.app.config(background=self.bg_color)
        self.app.geometry("600x600")
        self.app.bind('<Control-q>', quit)
        self.app_width = 600
        self.app_hieght = 800

        app.resizable(False, False)

        self.chatHistory = [
            {"role" : "system", "content" : systemPrompt}    
        ]

        ## Spawns screen constants...
        self.header = CTk.CTkFrame(self.app, width=600, height=75, fg_color=self.bg_color_light, bg_color=self.bg_color, corner_radius=0)
        self.header.place(x=0, y=0)

        app_name = CTk.CTkLabel(self.header, text="CounselAI", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12) ## This places the text 50 px below the top and 51 px above the header border... >:-(
        self.all_screen_obj.append(app_name)

        settings_button = CTk.CTkButton(self.header, text="⚙️", font=self.header_font, fg_color=self.bg_color_light, hover_color=self.bg_color, border_width=0, command = lambda : self.director("SettingButton"), width=60, height=50)
        settings_button.place(x=525, y=12)

        self.ai_chat_button = CTk.CTkButton(self.app, 100, border_width=0, command=self.chat_with_ai, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text="Chat with AI!", font=self.header_font)
        self.ai_chat_button.place(x=200, y=550)

        self.parse_unis()

        self.intro_1st_slide()

        self.app.mainloop()

    def quit(self, blank_var = None) : ## B/c for some dumb reason, tkinter sends an argument straight into this functnion...
        self.app.quit()

    def clearScreen(self,) :
        while self.all_screen_obj :
            self.all_screen_obj[0].destroy()
            del self.all_screen_obj[0]

    def director(self, screen) :
        pass

    ## Questionaire code
    def intro_1st_slide(self,) : 
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Introduction", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        intro_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Welcome to CounselAI!", font=self.header_font)
        intro_text.place(x=0, y = 150)
        self.all_screen_obj.append(intro_text)

        intro_text_2 = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text="A free AI-based college counseling application.", font=self.text_font)
        intro_text_2.place(x=0, y = 225)
        self.all_screen_obj.append(intro_text_2)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_1st_slide_message, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)
    
    def intro_1st_slide_message(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Introduction", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        intro_text_1 = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text="CounselAI helps to recommend you\ncolleges using a \"hollistic\" review process\nlike how colleges evaluate your application.\nCounselAI takes into account your\nGPA, test scores, extracurriculars,\nand other information to recommend to\nyou the best colleges possible.", font=self.medium_font)
        intro_text_1.place(x=0, y = 125)
        self.all_screen_obj.append(intro_text_1)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_1st_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_2nd_slide, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_2nd_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Introduction", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        name_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Enter your name", font=self.header_font)
        name_text.place(x=0, y = 150)
        self.all_screen_obj.append(name_text)

        self.name_tb = CTk.CTkEntry(self.app, placeholder_text="Your name", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.name_tb.place(x=100, y=300)
        self.all_screen_obj.append(self.name_tb)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_1st_slide_message, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_3rd_slide, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_3rd_slide(self,) :
        try :
            self.name = self.name_tb.get()
        except : self.name = "Error"

        self.clearScreen()
        
        app_name = CTk.CTkLabel(self.header, text="CounselAI: Grades", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        gpa_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What is your current GPA?", font=self.header_font)
        gpa_text.place(x=0, y = 150)
        self.all_screen_obj.append(gpa_text)

        self.gpa_tb = CTk.CTkEntry(self.app, placeholder_text="Your GPA", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.gpa_tb.place(x=100, y=300)
        self.all_screen_obj.append(self.gpa_tb)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_2nd_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_4th_slide(self,) :
        try :
            is_valid = False
            self.gpa = float(self.gpa_tb.get())
            assert(self.gpa >= 0 and self.gpa <= 5)
            is_valid = True
        except (ValueError) :
            messagebox.showerror("Invalid GPA", "The GPA entered was invalid!")
        except AssertionError : 
            messagebox.showerror("Invalid GPA", "Valid GPA range, 1-5.")
        
        except Exception :
            is_valid = True
        
        if is_valid :
            self.clearScreen()

            app_name = CTk.CTkLabel(self.header, text="CounselAI: AP Courses", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
            app_name.place(x=20, y=12)
            self.all_screen_obj.append(app_name)

            ap_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken any AP Courses?", font=self.header_font)
            ap_text.place(x=0, y = 150)
            self.all_screen_obj.append(ap_text)

            yes_aps = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_4th_slide_ap_selector, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_aps.place(x=150, y=400)
            self.all_screen_obj.append(yes_aps)

            no_aps = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_5th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_aps.place(x=375, y=400)
            self.all_screen_obj.append(no_aps)

            back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_3rd_slide, width=100, height=50)
            back_button.place(x=150, y=450)
            self.all_screen_obj.append(back_button)

    def intro_4th_slide_ap_selector(self) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: AP Courses", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        ap_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Select your AP: ", font=self.text_font)
        ap_text.place(x=25, y=150)
        self.all_screen_obj.append(ap_text)

        self.ap_db = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-"] + self.ALL_APS, font=self.text_font)
        self.ap_db.place(x=300, y=150)
        self.all_screen_obj.append(self.ap_db)

        ap_grade_text = CTk.CTkLabel(self.app, bg_color=self.app_text_box_color, fg_color=self.bg_color, text="Your grade in the class: ", font=self.text_font)
        ap_grade_text.place(x=25, y=250)
        self.all_screen_obj.append(ap_grade_text)

        self.ap_grade = CTk.CTkOptionMenu(self.app, bg_color=self.app_text_box_color, fg_color=self.bg_color, values=["-", "A", "B", 'C', 'D/F', "Test Only"], font=self.text_font)
        self.ap_grade.place(x=400, y=250)
        self.all_screen_obj.append(self.ap_grade)

        ap_test_grade_text = CTk.CTkLabel(self.app, bg_color=self.app_text_box_color, fg_color=self.bg_color, text="Your score on the AP exam", font=self.text_font)
        ap_test_grade_text.place(x=25, y=350)
        self.all_screen_obj.append(ap_test_grade_text)

        self.ap_score = CTk.CTkOptionMenu(self.app, bg_color=self.app_text_box_color, fg_color=self.bg_color, values=['-', '5','4','3','2','1'], font=self.text_font)
        self.ap_score.place(x=400, y=350)
        self.all_screen_obj.append(self.ap_score)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide_ap_selector_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_4th_slide_ap_selector_validator(self,) :
        try :
            ap_course = self.ap_db.get()
            ap_grade = self.ap_grade.get()
            ap_score = self.ap_score.get()

            if ap_course == "-" or ap_grade == "-" or ap_score == "-" :
                raise ValueError
            
            ap_score = int(ap_score)

            ## Messy code ahead!
            if ap_grade == "A" :
                ap_grade = 5
            elif ap_grade == "B" :
                ap_grade = 4
            elif ap_grade == "C" :
                ap_grade = 3
            else :
                ap_grade = 0.5

            if ap_course in self.AP_T1 :
                self.taken_APs.append(AP.apClass(ap_course, 5, ap_grade, ap_score))
            elif ap_course in self.AP_T2 :
                self.taken_APs.append(AP.apClass(ap_course, 4, ap_grade, ap_score))
            elif ap_course in self.AP_T3 :
                self.taken_APs.append(AP.apClass(ap_course, 3, ap_grade, ap_score))
            elif ap_course in self.AP_T4 :
                self.taken_APs.append(AP.apClass(ap_course, 2, ap_grade, ap_score))
            else :
                self.taken_APs.append(AP.apClass(ap_course, 1, ap_grade, ap_score))

            self.clearScreen()

            app_name = CTk.CTkLabel(self.header, text="CounselAI: AP Courses", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
            app_name.place(x=20, y=12)
            self.all_screen_obj.append(app_name)

            ap_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken any other APs?", font=self.header_font)
            ap_text.place(x=0, y = 150)
            self.all_screen_obj.append(ap_text)

            yes_ap = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_4th_slide_ap_selector, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_ap.place(x=150, y=450)
            self.all_screen_obj.append(yes_ap)

            no_ap = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_5th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_ap.place(x=375, y=450)
            self.all_screen_obj.append(no_ap)
        except ValueError :
            messagebox.showerror("Invalid AP Course", "Please fill out all the information for the AP Course.")

        except Exception as err:
            print(err)

    def intro_5th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        sat_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken the SAT yet?", font=self.header_font)
        sat_text.place(x=0, y = 150)
        self.all_screen_obj.append(sat_text)

        yes_sat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_5th_slide_sat_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_sat.place(x=150, y=400)
        self.all_screen_obj.append(yes_sat)

        no_sat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_5th_slide_psat, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_sat.place(x=375, y=400)
        self.all_screen_obj.append(no_sat)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

    def intro_5th_slide_sat_score(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        sat_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What is your highest SAT score?", font=self.header_font)
        sat_text.place(x=0, y = 150)
        self.all_screen_obj.append(sat_text)

        self.sat_tb = CTk.CTkEntry(self.app, placeholder_text="Your SAT score, 400-1600", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.sat_tb.place(x=100, y=300)
        self.all_screen_obj.append(self.sat_tb)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_5th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_5th_slide_sat_score_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_5th_slide_sat_score_validator(self,) :
        try :
            self.sat_score = int(self.sat_tb.get())
            assert((self.sat_score/10).is_integer())
            assert(self.sat_score >= 400 and self.sat_score <= 1600)
            self.intro_6th_slide()
        except : 
            messagebox.showerror("Invalid SAT Score", "Invalid SAT Score, SAT score range is from 400 to 1600.")
        
    
    def intro_5th_slide_psat(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        psat_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken a PSAT yet?", font=self.header_font)
        psat_text.place(x=0, y = 150)
        self.all_screen_obj.append(psat_text)

        yes_psat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_5th_slide_psat_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_psat.place(x=150, y=400)
        self.all_screen_obj.append(yes_psat)

        no_psat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_6th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_psat.place(x=375, y=400)
        self.all_screen_obj.append(no_psat)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_5th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

    def intro_5th_slide_psat_score(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        psat_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What is your most\nrecent PSAT score?", font=self.text_font)
        psat_text.place(x=0, y = 150)
        self.all_screen_obj.append(psat_text)

        self.psat_tb = CTk.CTkEntry(self.app, placeholder_text="Your PSAT score", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.psat_tb.place(x=100, y=250)
        self.all_screen_obj.append(self.psat_tb)

        ap_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="PSAT Version: ", font=self.text_font)
        ap_text.place(x=150, y=350)
        self.all_screen_obj.append(ap_text)

        self.psat_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-", "8/9", "10/11"], font=self.text_font)
        self.psat_dd.place(x=300, y=350)
        self.all_screen_obj.append(self.psat_dd)

        yes_psat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Back", command=self.intro_5th_slide_psat, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_psat.place(x=150, y=450)
        self.all_screen_obj.append(yes_psat)

        no_psat = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Next", command=self.intro_5th_slide_psat_score_validator, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_psat.place(x=375, y=450)
        self.all_screen_obj.append(no_psat)
    
    def intro_5th_slide_psat_score_validator(self,) :
        try :
            psat_score = int(self.psat_tb.get())
            assert(isinstance(psat_score/10, int) or (psat_score/10).is_integer())
            psat_version = self.psat_dd.get()
            if psat_version == "-" :
                raise AssertionError
            elif psat_version == "8/9" :
                psat_score += 160 ## Aprox for SAT conversion
                assert(psat_score >= 400 and psat_score <= 1440)
            else :
                psat_score += 80 ## Aprox for SAT conversion
                assert(psat_score >= 400 and psat_score <= 1440)
            self.sat_score = psat_score
            self.intro_6th_slide()
        except : 
            messagebox.showerror("Invalid SAT Score", "Invalid SAT Score, SAT score range is from 400 to 1600.")

    def intro_6th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        act_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken the ACT yet?", font=self.header_font)
        act_text.place(x=0, y = 150)
        self.all_screen_obj.append(act_text)

        yes_act = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_6th_slide_act_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_act.place(x=150, y=400)
        self.all_screen_obj.append(yes_act)

        no_act = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_7th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_act.place(x=375, y=400)
        self.all_screen_obj.append(no_act)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_5th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)
    
    def intro_6th_slide_act_score(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Standardized Tests", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        act_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What is your highest ACT score?", font=self.header_font)
        act_text.place(x=0, y = 150)
        self.all_screen_obj.append(act_text)

        self.act_tb = CTk.CTkEntry(self.app, placeholder_text="Your ACT score, 1-36", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.act_tb.place(x=100, y=300)
        self.all_screen_obj.append(self.act_tb)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_6th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_6th_slide_act_score_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)
    
    def intro_6th_slide_act_score_validator(self,) :
        try :
            self.act_score = int(self.act_tb.get())
            assert(self.act_score >= 1 and self.act_score <= 36)

            ## I came up with this algorithm myself, it is relatively accurate for score conversions
            self.act_score = 35*self.act_score + 340

            ## Janky but works
            if self.act_score > self.sat_score :
                self.sat_score = self.act_score 
                self.used_act = True

            self.intro_7th_slide()
        except : 
            messagebox.showerror("Invalid ACT Score", "Invalid ACT Score, ACT score range is from 1 to 36.")
    
    def intro_7th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Clubs", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Were you a part of any clubs?", font=self.header_font)
        clubs_text.place(x=0, y = 150)
        self.all_screen_obj.append(clubs_text)

        yes_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_7th_slide_club_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_clubs.place(x=150, y=400)
        self.all_screen_obj.append(yes_clubs)

        no_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_8th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_clubs.place(x=375, y=400)
        self.all_screen_obj.append(no_clubs)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_6th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

    def intro_7th_slide_club_entry(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Clubs", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        club_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Your Club name: ", font=self.text_font)
        club_text.place(x=50, y=150)
        self.all_screen_obj.append(club_text)

        self.club_tb = CTk.CTkEntry(self.app, placeholder_text="Club name", width=300, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.club_tb.place(x=250, y=150)
        self.all_screen_obj.append(self.club_tb)

        club_text_p = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Club type", font=self.text_font)
        club_text_p.place(x=50, y=250)
        self.all_screen_obj.append(club_text_p)

        self.club_purpose = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-", "Academic", "Recreational", "Volunteering", "Other"], font=self.text_font)
        self.club_purpose.place(x=300, y=250)
        self.all_screen_obj.append(self.club_purpose)

        club_role_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Club Role", font=self.text_font)
        club_role_text.place(x=50, y=350)
        self.all_screen_obj.append(club_role_text)

        self.clube_role = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-", "President", "Vice-president", "Other leadership role", "Member"], font=self.text_font)
        self.clube_role.place(x=300, y=350)
        self.all_screen_obj.append(self.clube_role)    

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_7th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_7th_slide_club_entry_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)

    def intro_7th_slide_club_entry_validator(self,) :
        try :
            club_name = self.club_tb.get()
            club_purpose = self.club_purpose.get()
            club_role = self.clube_role.get()

            assert(club_purpose != "-" and club_role != "-")
            ## Janky but got no time to write clean solution
            if club_purpose == "Academic" :
                club_purpose = 2.5
            elif club_purpose == "Volunteering" : 
                club_purpose = 1.5
            else : ## Recreational counts as other as not realy boost
                club_purpose = 1

            if club_role == "President" :
                club_role = 3
            elif club_role == "Vice-president" :
                club_role = 2.5
            elif club_role == "Other leadership role" :
                club_role = 1.75
            else :
                club_role = 1

            self.taken_clubs.append(clubs.clubs(club_name, club_purpose, club_role))

            self.clearScreen()

            app_name = CTk.CTkLabel(self.header, text="CounselAI: Clubs", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
            app_name.place(x=20, y=12)
            self.all_screen_obj.append(app_name)

            clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Were you a part of any other clubs?", font=self.header_font)
            clubs_text.place(x=0, y = 150)
            self.all_screen_obj.append(clubs_text)

            yes_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_7th_slide_club_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_clubs.place(x=150, y=400)
            self.all_screen_obj.append(yes_clubs)

            no_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_8th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_clubs.place(x=375, y=400)
            self.all_screen_obj.append(no_clubs)

        except :
            messagebox.showerror("Invalid Club Entry", "Invalid Club Entry!")
            self.intro_7th_slide_club_entry()

    def intro_8th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Sports", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        sports_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Did you participate in any sports?", font=self.header_font)
        sports_text.place(x=0, y = 150)
        self.all_screen_obj.append(sports_text)

        yes_sports = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_8th_slide_sports_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_sports.place(x=150, y=400)
        self.all_screen_obj.append(yes_sports)

        ## TEMP LINK TO 10TH SLIDE
        no_sports = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_10th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_sports.place(x=375, y=400)
        self.all_screen_obj.append(no_sports)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_7th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)
    
    def intro_8th_slide_sports_entry(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Sports", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        sports_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="The Sports name: ", font=self.text_font)
        sports_text.place(x=50, y=150)
        self.all_screen_obj.append(sports_text)

        self.sports_tb = CTk.CTkEntry(self.app, placeholder_text="Sports name", width=300, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.sports_tb.place(x=250, y=150)
        self.all_screen_obj.append(self.sports_tb)

        sports_role = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Sports role", font=self.text_font)
        sports_role.place(x=50, y=250)
        self.all_screen_obj.append(sports_role)

        self.sports_role_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values=["-", "Captain/Leader", "Other leadership role", "Player"], font=self.text_font)
        self.sports_role_dd.place(x=300, y=250)
        self.all_screen_obj.append(self.sports_role_dd)

        club_role_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Length of\nthe sport\n(Months)", font=self.text_font)
        club_role_text.place(x=50, y=350)
        self.all_screen_obj.append(club_role_text)

        self.sports_length = CTk.CTkEntry(self.app, placeholder_text="(i, e. 5)", width=300, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.sports_length.place(x=250, y=350)
        self.all_screen_obj.append(self.sports_length)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_8th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_8th_slide_sports_entry_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)
    
    def intro_8th_slide_sports_entry_validator(self,) :
        #try :
            sports_name = self.sports_tb.get()
            sports_role = self.sports_role_dd.get()
            sports_length = int(self.sports_length.get()) ## This gives exception if not int so we can tell user that the data is wrong
            assert(sports_role != "-")

            if sports_role == "Captain/Leader" :
                sports_role = 2
            elif sports_role == "Other leadership role" :
                sports_role = 1.25
            else : 
                sports_role = 1

            self.taken_sports.append(sports.sports(sports_name, sports_role, sports_length))

            self.clearScreen()

            app_name = CTk.CTkLabel(self.header, text="CounselAI: Sports", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
            app_name.place(x=20, y=12)
            self.all_screen_obj.append(app_name)

            clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Did you participate in\nany other sports?", font=self.header_font)
            clubs_text.place(x=0, y = 150)
            self.all_screen_obj.append(clubs_text)

            yes_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_8th_slide_sports_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_clubs.place(x=150, y=400)
            self.all_screen_obj.append(yes_clubs)

            ## TEMP redir to 10th slide instead of 9th
            no_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_10th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_clubs.place(x=375, y=400)
            self.all_screen_obj.append(no_clubs)

            back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_7th_slide, width=100, height=50)
            back_button.place(x=150, y=450)
            self.all_screen_obj.append(back_button)

    def intro_10th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Awards & Challenges", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        awards_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you won any\nawards/challenges?", font=self.header_font)
        awards_text.place(x=0, y = 150)
        self.all_screen_obj.append(awards_text)

        yes_awards = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_10th_slide_award_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_awards.place(x=150, y=400)
        self.all_screen_obj.append(yes_awards)

        no_awards = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_11th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_awards.place(x=375, y=400)
        self.all_screen_obj.append(no_awards)

        ## TEMP LINK TO 8TH SLIDE
        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_8th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

    def intro_10th_slide_award_entry(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Awards & Challenges", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        award_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="The award's name: ", font=self.text_font)
        award_text.place(x=50, y=150)
        self.all_screen_obj.append(award_text)

        self.award_tb = CTk.CTkEntry(self.app, placeholder_text="Award's name", width=300, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.award_tb.place(x=275, y=150)
        self.all_screen_obj.append(self.award_tb)

        award_region = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Award's Region: ", font=self.text_font)
        award_region.place(x=50, y=250)
        self.all_screen_obj.append(award_region)

        self.award_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-"] + self.regions, font=self.text_font)
        self.award_dd.place(x=300, y=250)
        self.all_screen_obj.append(self.award_dd)

        award_level_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Award's Level: ", font=self.text_font)
        award_level_text.place(x=50, y=350)
        self.all_screen_obj.append(award_level_text)

        self.award_level = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-", "Top 3", "Finalist", "Participant"] , font=self.text_font)
        self.award_level.place(x=300, y=350)
        self.all_screen_obj.append(self.award_level)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_10th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_10th_slide_award_entry_validator, width=100, height=50)
        next_button.place(x=350, y=450)
        self.all_screen_obj.append(next_button)
    
    def intro_10th_slide_award_entry_validator(self,) :
        try :
            award_name = self.award_tb.get()
            award_region = self.award_dd.get()
            award_level = self.award_level.get()
            
            assert(award_region != "-" and award_level != "-")

            if award_region == "Local/School" :
                award_region = 0.75
            elif award_region == "State" :
                award_region = 1.5
            elif award_region == "Regional" :
                award_region = 3
            elif award_region == "National" :
                award_region = 5
            else :
                award_region = 6
            
            if award_level == "Top 3" :
                award_level = 3
            elif award_level == "Finalist" :
                award_level = 1.5
            else :
                award_level = 0.5

            self.clearScreen()

            app_name = CTk.CTkLabel(self.header, text="CounselAI: Awards & Challenges", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
            app_name.place(x=20, y=12)
            self.all_screen_obj.append(app_name)

            self.awarded_awards.append(awards.awards(award_name, award_level, award_region))

            clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you won any\nother awards or challenges?", font=self.header_font)
            clubs_text.place(x=0, y = 150)
            self.all_screen_obj.append(clubs_text)

            yes_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_10th_slide_award_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_clubs.place(x=150, y=400)
            self.all_screen_obj.append(yes_clubs)

            ## TEMP redir to 10th slide instead of 9th
            no_clubs = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_11th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_clubs.place(x=375, y=400)
            self.all_screen_obj.append(no_clubs)

        except :
            messagebox.showerror("Invalid Award Entry", "Invalid Award Entry!")
            self.intro_10th_slide_award_entry()

    def intro_11th_slide(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Carreer", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        career_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What career field would\nyou like to pursue?", font=self.header_font)
        career_text.place(x=0, y = 150)
        self.all_screen_obj.append(career_text)

        self.career_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-"] + self.career_path , font=self.header_font, width = 300)
        self.career_dd.place(x=150, y=250)
        self.all_screen_obj.append(self.career_dd)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_10th_slide, width=100, height=50)
        back_button.place(x=150, y=450)
        self.all_screen_obj.append(back_button)

        report = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Generate Report", command=self.generate_report, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        report.place(x=350, y=450)
        self.all_screen_obj.append(report)

    def generate_report(self,) :
        try :
            self.career_path_entered = self.career_dd.get()
            assert (self.career_path_entered != "-")
            if self.sat_score == 0 :
                self.sat_score = "no test"
                self.student_score = self.gpa*12 ## If no SAT, GPA takes more of SAT's weight, but not all as GPA != SAT
            ## Student score eval
            else : self.student_score = self.sat_score/75 + self.gpa*8
            
            ## Very dumb but it works so :shrug:
            for i in self.taken_APs :
                self.student_score += i.apValue

            for i in self.taken_clubs :
                self.student_score += i.clubValue
            
            for i in self.taken_sports :
                self.student_score += i.sportsValue
            
            for i in self.awarded_awards :
                self.student_score += i.awardValue

            if self.career_path_entered == "Undecided" or self.career_path_entered == "Other" :
                self.tag = ""
            else :
                self.tag = self.career_path_entered
            
            self.recommend_unis = []
            self.reach_unis = []
            self.target_unis = []
            self.safety_unis = []

            for i in self.ALL_UNIS : ## Ugly code
                if self.student_score*1.3 > i.universityDifficulty and self.student_score*1.15 <= i.universityDifficulty :
                    self.reach_unis.append(i)
                elif self.student_score*1.15 > i.universityDifficulty and  self.student_score*0.8 <= i.universityDifficulty :
                    self.target_unis.append(i)
                elif self.student_score*0.6 > i.universityDifficulty and self.student_score*0.4 <= i.universityDifficulty :
                    self.safety_unis.append(i)

            temp_recommend = self.reach_unis + self.target_unis + self.safety_unis

            self.recommend_unis = [uni for uni in temp_recommend if self.tag in uni.tags or self.tag == ""]
            
            try :
                if len(self.recommend_unis) < 6 :
                    for i in range(6-len(self.recommend_unis)) :
                        randomVar = random.choice(temp_recommend)
                        self.recommend_unis.append(randomVar)
                        temp_recommend.remove(randomVar)

                for uni in temp_recommend :
                    if len(self.recommend_unis) >= 6 :
                        break
                    if uni not in self.recommend_unis :
                        self.recommend_unis.append(uni)
                    self.recommend_unis = list(set(self.recommend_unis)) ## Remove duplicates, this is jank

            except IndexError : ## This is for when the user has a comically low eval score...
                tempT5_UNIS = self.T5_UNIS.copy()
                for i in range(3) : 
                    randomUni = random.choice(tempT5_UNIS)
                    tempT5_UNIS.remove(randomUni)
                    self.recommend_unis.append(randomUni)

            for i in self.recommend_unis :
                print(i.name)

            uni_cp = self.recommend_unis.copy()
            self.temp_recommend_unis = []

            for i in range(6 if 6 <= len(uni_cp) else len(uni_cp)) :
                randomUni = random.choice(uni_cp)
                uni_cp.remove(randomUni)
                self.temp_recommend_unis.append(randomUni)

            self.report_slide_1()

        except AssertionError:
            messagebox.showerror("Invalid Career Field", "Invalid Career Field!")
            self.intro_11th_slide()
    
    def report_slide_1(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: Report (1/4)", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        recommend_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Recommended Universities: ", font=self.text_font, width=600)
        recommend_text.place(x=0, y=90)
        self.all_screen_obj.append(recommend_text)
        
        self.temp_recommend_unis = self.temp_recommend_unis[:6] ## Truncates the total unis to 6 or less

        y_pos = 140
        for i in range(len(self.temp_recommend_unis)) : 
            uni = self.temp_recommend_unis[i]

            layer = CTk.CTkFrame(self.app, 600, 50, 0, 0, self.bg_color_light, self.bg_color_light)
            layer.place(x=0, y=y_pos + i*60)

            uni_text = CTk.CTkLabel(layer, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text=uni.name, font=self.button_font)
            uni_text.place(x=15, y=12)
            self.all_screen_obj.append(uni_text)

            uni_button = CTk.CTkButton(layer, 75, border_width=0, command=lambda university = uni.name: self.report_slide_2(university), text="More info", font=self.small_font)
            uni_button.place(x=500, y=12)

            self.all_screen_obj.append(layer)

    def report_slide_2(self, university_name) : ## TODO: Cache the response from OpenAI to save some API billing
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: 2/4", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        self.temp_chat = [{"role" : "system", "content" : systemPrompt + ". Please do not use lists and keep the reponse in a paragraph. Refer to the user as 'you'."}] ## Janky but works
        self.temp_chat.append({"role" : "user", "content" : f"Generate a short description of  {university_name}. Include key details such as location, good programs, etc."})

        try :
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=self.temp_chat,
                max_tokens=250,
                n=1,
                stop=None,
                temperature=0.75, ## Using higher temperatures leads to more predictable results, but it does help it remain more consistent
                ## We are also not trying to bypass AI-detectors here. But if we needed we can use https://github.com/IDoUseLinux/aint.
            )

            uni_description = response.choices[0].message.content
            print(uni_description)
        except Exception as e :
            messagebox.showerror("Error!", f"An error occurred: {str(e)}")

        uni_description = self.format_text(uni_description, self.sm_font)
        
        uni_name = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text=university_name + " :", font=self.button_font, width=600)
        uni_name.place(x=0, y=80)
        self.all_screen_obj.append(uni_name)

        uni_description_text = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text=uni_description, font=self.sm_font)
        uni_description_text.place(x=0, y=125)
        self.all_screen_obj.append(uni_description_text)

        back_button = CTk.CTkButton(self.app, text="<", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.report_slide_1, width=50, height=50)
        back_button.place(x=50, y=500)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text=">", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = lambda temp_un = university_name : self.report_slide_3(temp_un), width=50, height=50)
        next_button.place(x=500, y=500)
        self.all_screen_obj.append(next_button)

    def report_slide_3(self, university_name) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: 3/4", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        for i in range(len(self.ALL_UNIS)) :
            if self.ALL_UNIS[i].name == university_name :
                university_obj = self.ALL_UNIS[i]
                break
        
        if self.student_score*1.3 > university_obj.universityDifficulty and university_obj.universityDifficulty <= self.student_score*1.15 :
            uni_type = "reach"
            type_message = f"This means that you have a chance at getting for {self.tag}."
        elif self.student_score*1.15 > university_obj.universityDifficulty and university_obj.universityDifficulty <= self.student_score*0.8 :
            uni_type = "target"
            type_message = f"This means that you have a decent chance at getting accepted."
        else :
            uni_type = "safety"
            type_message = f"This means that you have a high chance at getting accepted."

        uni_explanier = self.format_text(f"{university_name} is a {uni_type} university for you. {type_message} It has a 75th percentile SAT score of {university_obj.sat75}, 50th percentile of {university_obj.sat50}, and 25th percentile of {university_obj.sat25}.", self.sm_font)

        uni_description_text = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text=uni_explanier, font=self.sm_font)
        uni_description_text.place(x=0, y=110)
        self.all_screen_obj.append(uni_description_text)
        

        back_button = CTk.CTkButton(self.app, text="<", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = lambda temp_un = university_name: self.report_slide_2(temp_un), width=50, height=50)
        back_button.place(x=50, y=500)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text=">", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = lambda temp_un = university_name : self.report_slide_4(temp_un), width=50, height=50)
        next_button.place(x=500, y=500)
        self.all_screen_obj.append(next_button)


    def report_slide_4(self, university_name) :
        self.clearScreen()
        
        app_name = CTk.CTkLabel(self.header, text="CounselAI: 4/4", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        self.temp_chat.append({"role" : "user", "content" : f"Give some advice for the user to on to get accepted at {university_name} for {self.career_path_entered}. The user currently has a {"ACT" if self.used_act else "SAT"} score of {self.act_score if self.used_act else self.sat_score} and a highschool GPA of {self.gpa}."})

        try :
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=self.temp_chat,
                max_tokens=250,
                n=1,
                stop=None,
                temperature=0.75,
            )

            uni_advice = response.choices[0].message.content
        except Exception as e :
            messagebox.showerror("Error!", f"An error occurred: {str(e)}")

        uni_advice = self.format_text(uni_advice, self.sm_font)

        uni_advice_head = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text=f"Advice for {university_name} :", font=self.button_font, width=600)
        uni_advice_head.place(x=0, y=80)
        self.all_screen_obj.append(uni_advice_head)

        uni_description_text = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text=uni_advice, font=self.sm_font)
        uni_description_text.place(x=0, y=110)
        self.all_screen_obj.append(uni_description_text)

        back_button = CTk.CTkButton(self.app, text="<", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = lambda temp_un = university_name : self.report_slide_2(temp_un), width=50, height=50)
        back_button.place(x=50, y=500)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text=">", font=self.medium_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.report_slide_1, width=50, height=50)
        next_button.place(x=500, y=500)
        self.all_screen_obj.append(next_button)

    def chat_with_ai(self,) :
        self.clearScreen()

        app_name = CTk.CTkLabel(self.header, text="CounselAI: AI Chat", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12)
        self.all_screen_obj.append(app_name)

        self.ai_chat_button.destroy()

        self.ai_entry = CTk.CTkEntry(self.app, 400, 50, 0, 0, self.app_text_box_color, self.app_text_box_color, placeholder_text="Hello, World!", font=self.medium_font)
        self.ai_entry.place(x=50, y=550)
        self.all_screen_obj.append(self.ai_entry)

        send_button = CTk.CTkButton(self.app, 50, 50, 0, 0, command=self.sendMessage, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text="Send", font=self.header_font)
        send_button.place(x=450, y=550)
        self.all_screen_obj.append(send_button)

        self.current_y_ai = 15

    def parse_unis(self, ) :
        self.T1_UNIS = []
        self.T2_UNIS = []
        self.T3_UNIS = []
        self.T4_UNIS = []
        self.T5_UNIS = []

        with open("tier1.json", 'r') as t1 :
            tier1s = json.load(t1)
            
            for i in tier1s :
                ## Ugly but works
                self.T1_UNIS.append(universities.university(i, tier1s[i]["acc_rate"], 5, tier1s[i]["75_sat"], tier1s[i]["50_sat"], tier1s[i]["25_sat"], tier1s[i]["tags"]))
                #print(self.T1_UNIS[len(self.T1_UNIS)-1].universityDifficulty)

        with open("tier2.json", 'r') as t2 :
            tier2s = json.load(t2)

            for i in tier2s :
                self.T2_UNIS.append(universities.university(i, tier2s[i]["acc_rate"], 4, tier2s[i]["75_sat"], tier2s[i]["50_sat"], tier2s[i]["25_sat"], tier2s[i]["tags"]))

        with open("tier3.json", 'r') as t3 :
            tier3s = json.load(t3)

            for i in tier3s :
                self.T3_UNIS.append(universities.university(i, tier3s[i]["acc_rate"], 3, tier3s[i]["75_sat"], tier3s[i]["50_sat"], tier3s[i]["25_sat"], tier3s[i]["tags"]))
            
        with open("tier4.json", 'r') as t4 :
            tier4s = json.load(t4)

            for i in tier4s :
                self.T4_UNIS.append(universities.university(i, tier4s[i]["acc_rate"], 2, tier4s[i]["75_sat"], tier4s[i]["50_sat"], tier4s[i]["25_sat"], tier4s[i]["tags"]))

        with open("tier5.json", 'r') as t5 :
            tier5s = json.load(t5)

            for i in tier5s :
                self.T5_UNIS.append(universities.university(i, tier5s[i]["acc_rate"], 1, tier5s[i]["75_sat"], tier5s[i]["50_sat"], tier5s[i]["25_sat"], tier5s[i]["tags"]))
                #print(self.T5_UNIS[len(self.T5_UNIS)-1].universityDifficulty)

        ## Also a bit janky but also works
        self.ALL_UNIS = self.T1_UNIS + self.T2_UNIS + self.T3_UNIS + self.T4_UNIS + self.T5_UNIS

    def sendMessage(self) :
        user_input = self.ai_entry.get()
        self.ai_entry.delete(0, CTk.END)
        print(user_input)

        ai_response = self.format_text(self.sendOPENAIMessage(user_input))

        print(ai_response)
        ai_message = CTk.CTkLabel(self.app, 500, 400, bg_color=self.bg_color, fg_color=self.bg_color, text=ai_response, font=self.text_font)
        ai_message.place(x=25, y=100)

    def sendOPENAIMessage(self, user_input) -> str :
        try :
            self.chatHistory.append({"role" : "user", "content" : user_input})

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=self.chatHistory,
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.75
            )

            return response.choices[0].message.content
        except Exception as e : 
            return f"An error occurred: {str(e)}"
    
    def format_text(self, text:str, type) :
        formatted_text = list(text)

        space_count = 0
        last_space = 0
        i = 0  # Use manual index control

        if type == self.sm_font :
            mod1 = 10
            mod2 = 50
            mod3 = 60
        elif type == self.text_font :
            mod1 = 6 
            mod2 = 30
            mod3 = 36

        while i < len(formatted_text):
            last_space += 1
            if formatted_text[i] == " ":
                space_count += 1
                # Check conditions for inserting '\n'
                if (space_count % mod1 == 0 and last_space >= mod2) or last_space >= mod3 :
                    formatted_text[i] = "\n"  # Replace the space with a newline
                    last_space = 0  # Reset distance since last space/newline
            i += 1  # Manually increment index

        return "".join(formatted_text)
        
    
var = app(CTk.CTk())