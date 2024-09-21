import customtkinter as CTk, requests, os
import openai, json, requests, random, webbrowser
import score, clubs, awards, sports, AP, universities
from tkinter import messagebox

## First expand, write in as many features into the code as possible
## Then re-org, making the code-base actually redable and consolidating
## bloated code into more optimal code and adding in quality of life 
## changes.

with open("APIKEY.config", 'r') as api_key_file :
    openai.api_key = api_key_file.read()

with open("systemprompt.txt", 'r') as sp :
    systemPrompt = sp.read()

is_dev_version = True
build_tag = "Alpha-1234"

class app() :
    CAREER_PATHS = ["Undecided", "STEM", "Art", "Music", "Business", "Law", "Medical", "Sports", "Other"]

    AP_T1 = [
        "Calculus",
        "Physics",
        "Biology",
        "Chemistry",
    ]

    AP_T2 = [
        "Pre-calculus",
        "Statistics",
        "Pyschology",
        "US History",
    ]

    AP_T3 = [
        "English Language",
        "English Literature",
        "Government & Politics",
        "Environmental Science",
        "Chinese",
        "Spanish",
        "French",
        "Japanese",
        "Latin",
        "Italian",
        "CSA",
        "World History",
        "European History",
        "Macroeconomics",
        "Microeconomics",
    ]

    AP_T4 = [
        "Art History",
        "Music Theory",
        "Research",
        "Seminar",
        "CSP"
    ]

    AP_T5 = [
        "Art & Design",
    ]

    ALL_APS = AP_T1 + AP_T2 + AP_T3 + AP_T4 + AP_T5
    ALL_APS.sort()

    regions = ["Local/School", "State", "Regional", "National", "International"]

    taken_APs = []
    taken_clubs = []
    taken_sports = []
    awarded_awards = []
    sat_score = 1050 ## Assume Nat. Avg. if no test

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
    text_font = ("Segoe UI", 25)
    button_font = ("Segoe UI", 20)
    small_font = ("Segoe UI", 15)

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
        
        ## Spawns screen constants...
        header = CTk.CTkFrame(self.app, width=600, height=75, fg_color=self.bg_color_light, bg_color=self.bg_color, corner_radius=0)
        header.place(x=0, y=0)

        app_name = CTk.CTkLabel(header, text="CounselAI", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12) ## This places the text 50 px below the top and 51 px above the header border... >:-(

        settings_button = CTk.CTkButton(header, text="⚙️", font=self.header_font, fg_color=self.bg_color_light, hover_color=self.bg_color, border_width=0, command = lambda : self.director("SettingButton"), width=60, height=50)
        settings_button.place(x=525, y=12)

        self.chatHistory = [
            {"role" : "system", "content" : systemPrompt}    
        ]

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
        intro_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Welcome to CounselAI!", font=self.header_font)
        intro_text.place(x=0, y = 150)
        self.all_screen_obj.append(intro_text)

        intro_text_2 = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text="A free AI-based college counseling application!", font=self.text_font)
        intro_text_2.place(x=0, y = 225)
        self.all_screen_obj.append(intro_text_2)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_2nd_slide, width=100, height=50)
        next_button.place(x=150, y=400)
        self.all_screen_obj.append(next_button)

    def intro_2nd_slide(self,) :
        self.clearScreen()

        name_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Enter your name", font=self.header_font)
        name_text.place(x=0, y = 150)
        self.all_screen_obj.append(name_text)

        self.name_tb = CTk.CTkEntry(self.app, placeholder_text="Your name", width=400, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
        self.name_tb.place(x=100, y=300)
        self.all_screen_obj.append(self.name_tb)

        back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_1st_slide, width=100, height=50)
        back_button.place(x=150, y=400)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_3rd_slide, width=100, height=50)
        next_button.place(x=350, y=400)
        self.all_screen_obj.append(next_button)

    def intro_3rd_slide(self,) :
        try :
            self.name = self.name_tb.get()
        except : self.name = "Error"

        self.clearScreen()
        
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
            self.gpa = self.gpa_tb.get()
            self.gpa = float(self.gpa)
            assert(self.gpa >= 0 and self.gpa <= 5)
            is_valid = True
        except (ValueError, AssertionError) :
            messagebox.showerror("Invalid GPA", "The GPA entered was invalid!")
            self.intro_3rd_slide()
        except Exception : 
            is_valid = True
        
        if is_valid :
            self.clearScreen()

            ap_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken any APs?", font=self.header_font)
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
        back_button.place(x=150, y=400)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide_ap_selector_validator, width=100, height=50)
        next_button.place(x=350, y=400)
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
            elif ap_grade == "D/F" :
                ap_grade = 2
            else :
                ap_grade = 3

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

            ap_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken any other APs?", font=self.header_font)
            ap_text.place(x=0, y = 150)
            self.all_screen_obj.append(ap_text)

            yes_ap = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_4th_slide_ap_selector, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_ap.place(x=150, y=450)
            self.all_screen_obj.append(yes_ap)

            no_ap = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_5th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_ap.place(x=375, y=450)
            self.all_screen_obj.append(no_ap)

        except Exception as err:
            print(err)

    def intro_5th_slide(self,) :
        self.clearScreen()
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
            assert(isinstance(self.sat_score/10, int) or (self.sat_score/10).is_integer())
            assert(self.sat_score >= 400 and self.sat_score <= 1600)
            self.intro_6th_slide()
        except : 
            messagebox.showerror("Invalid SAT Score", "Invalid SAT Score, SAT score range is from 400 to 1600.")
        
    
    def intro_5th_slide_psat(self,) :
        self.clearScreen()
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
            act_score = int(self.act_tb.get())
            assert(act_score >= 1 and act_score <= 36)

            ## I came up with this algorithm myself, it is relatively accurate for score conversions
            act_score = 35*act_score + 340

            ## Janky but works
            self.sat_score = act_score if act_score > self.sat_score else self.sat_score

            self.intro_7th_slide()
        except : 
            messagebox.showerror("Invalid ACT Score", "Invalid ACT Score, ACT score range is from 1 to 36.")
    
    def intro_7th_slide(self,) :
        self.clearScreen()
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
                club_purpose = 3
            elif club_purpose == "Volunteering" : 
                club_purpose = 2
            else :
                club_purpose = 1

            if club_role == "President" :
                club_role = 3
            elif club_role == "Vice-president" :
                club_role = 2.5
            elif club_role == "Other leadership role" :
                club_role = 2
            else :
                club_role = 1

            self.taken_clubs.append(clubs.clubs(club_name, club_purpose, club_role))

            self.clearScreen()

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

        club_role_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Length of participation (Months)", font=self.text_font)
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
        try :
            sports_name = self.sports_tb.get()
            sports_role = self.sports_role_dd.get()
            sports_length = int(self.sports_length.get()) ## This gives exception if not int so we can tell user that the data is wrong
            assert(sports_role != "-")

            if sports_role == "Captain/Leader" :
                sports_role = 2.5
            elif sports_role == "Other leadership role" :
                sports_role = 1.5
            else : 
                sports_role = 1

            self.taken_sports.append(sports.sports(sports_name, sports_role, sports_length))

            self.clearScreen()

            clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Did you part take in\nany other sports?", font=self.header_font)
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

        except : 
            messagebox.showerror("Invalid Sports Entry", "Invalid Sports Entry!")
            self.intro_8th_slide_sports_entry()

    ## Too complicated to implement for hackathon, will implement for CAC instead
    # def intro_9th_slide(self,) :
    #     self.clearScreen()

    #     challenge_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you participated in\nany challenges?", font=self.header_font)
    #     challenge_text.place(x=0, y = 150)
    #     self.all_screen_obj.append(challenge_text)

    #     yes_challenges = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="Yes", command=self.intro_9th_slide_challenges_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
    #     yes_challenges.place(x=150, y=400)
    #     self.all_screen_obj.append(yes_challenges)

    #     no_challenges = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_10th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
    #     no_challenges.place(x=375, y=400)
    #     self.all_screen_obj.append(no_challenges)

    #     back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_8th_slide, width=100, height=50)
    #     back_button.place(x=150, y=450)
    #     self.all_screen_obj.append(back_button)

    # def intro_9th_slide_challenges_entry(self,) :
    #     self.clearScreen()

    #     challenge_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="The challenge's name: ", font=self.text_font)
    #     challenge_text.place(x=50, y=150)
    #     self.all_screen_obj.append(challenge_text)

    #     self.challenge_tb = CTk.CTkEntry(self.app, placeholder_text="Challenge name", width=300, height=60, font=self.text_font, text_color=self.app_text_color, bg_color=self.bg_color, fg_color=self.app_text_box_color, border_width=0)
    #     self.challenge_tb.place(x=250, y=150)
    #     self.all_screen_obj.append(self.challenge_tb)

    #     challenge_level = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Challenge Level", font=self.text_font)
    #     challenge_level.place(x=50, y=250)
    #     self.all_screen_obj.append(challenge_level)

    #     self.challenge_level_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values=self.regions, font=self.text_font)
    #     self.challenge_level_dd.place(x=300, y=250)
    #     self.all_screen_obj.append(self.challenge_level_dd)

    #     back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_9th_slide, width=100, height=50)
    #     back_button.place(x=150, y=450)
    #     self.all_screen_obj.append(back_button)

    #     next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_9th_slide_challenges_entry_validator, width=100, height=50)
    #     next_button.place(x=350, y=450)
    #     self.all_screen_obj.append(next_button)

    
    # def intro_9th_slide_challenges_entry_validator(self,) :
    #     self.clearScreen()

    def intro_10th_slide(self,) :
        self.clearScreen()

        awards_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you recieved any awards?", font=self.header_font)
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
                award_region = 1
            elif award_region == "State" :
                award_region = 2
            elif award_region == "Regional" :
                award_region = 3
            elif award_region == "National" :
                award_region = 5
            else :
                award_region = 7
            
            if award_level == "Top 3" :
                award_level = 5
            elif award_level == "Finalist" :
                award_level = 3
            else :
                award_level = 1

            self.clearScreen()

            self.awarded_awards.append(awards.awards(award_name, award_level, award_region))

            clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you recieved any\nother awards?", font=self.header_font)
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

        career_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="What career field would\nyou like to pursue", font=self.header_font)
        career_text.place(x=0, y = 150)
        self.all_screen_obj.append(career_text)

        self.career_dd = CTk.CTkOptionMenu(self.app, bg_color=self.bg_color, fg_color=self.bg_color, values= ["-"] + self.CAREER_PATHS , font=self.header_font, width = 300)
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
            career_path = self.career_dd.get()
            assert (career_path != "-")

            self.student_score = self.sat_score/50 + self.gpa*5
            
            ## Very dumb but it works so :shrug:
            tempTotal = 0
            for i in self.taken_APs :
                tempTotal += i.apValue
            
            for i in self.taken_clubs :
                tempTotal += i.clubValue
            
            for i in self.taken_sports :
                tempTotal += i.sportsValue
            
            for i in self.awarded_awards :
                tempTotal += i.awardValue

            self.student_score += tempTotal
            
            print(self.student_score)
                        
            self.clearScreen()
            if career_path == "STEM" :
                tag = "Tech"
            elif career_path == "Undecided" or career_path == "Other" :
                tag = None
            else :
                tag = career_path
            
            recommend_unis = []
            if self.student_score >= 75 :
                for i in self.T1_UNIS :
                    if tag in i.tags :
                        recommend_unis.append(i)
                if tag == "" :
                    for i in range(3) :
                        recommend_unis.append(random.choice(self.T1_UNIS))

            if self.student_score >= 50 and self.student_score <= 90 :
                for i in self.T2_UNIS :
                    if tag in i.tags :
                        recommend_unis.append(i)
                if tag == "" :
                    for i in range(3) :
                        recommend_unis.append(random.choice(self.T2_UNIS))

            if self.student_score >= 40 and self.student_score <= 80 :
                for i in self.T3_UNIS :
                    if tag in i.tags :
                        recommend_unis.append(i)
                if tag == "" :
                    for i in range(3) :
                        recommend_unis.append(random.choice(self.T3_UNIS))

            if self.student_score >= 30 and self.student_score <= 55 :
                for i in self.T4_UNIS :
                    if tag in i.tags :
                        recommend_unis.append(i)
                if tag == "" :
                    for i in range(3) :
                        recommend_unis.append(random.choice(self.T4_UNIS))
                        
            if self.student_score <= 45 :
                for i in self.T5_UNIS :
                    if tag in i.tags :
                        recommend_unis.append(i)
                if tag == "" :
                    for i in range(3) :
                        recommend_unis.append(random.choice(self.T5_UNIS))
            
            
            for i in recommend_unis :
                print(i.name)

            recommend_text = CTk.CTkLabel(self.app, bg_color=self.bg_color, fg_color=self.bg_color, text="Recommended Universities: ", font=self.text_font, width=600)
            recommend_text.place(x=0, y=90)
            self.all_screen_obj.append(recommend_text)

            y_pos = 80
            for i in range(5 if 5 <= len(recommend_unis) else len(recommend_unis)) : 
                uni = random.choice(recommend_unis)
                recommend_unis.remove(uni)

                layer = CTk.CTkFrame(self.app, 600, 65, 0, 0, self.bg_color_light, self.bg_color_light)
                layer.place(x=0, y=y_pos*i+140)

                uni_text = CTk.CTkLabel(layer, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text=uni.name, font=self.button_font)
                uni_text.place(x=15, y=20)
                self.all_screen_obj.append(uni_text)

                uni_button = CTk.CTkButton(layer, 75, border_width=0, command=lambda : webbrowser.open(f"https://google.com/search?q={uni.name}"), text="More info", font=self.small_font)
                uni_button.place(x=485, y=20)


                self.all_screen_obj.append(layer)

            ai_chat_button = CTk.CTkButton(self.app, 100, border_width=0, command=self.chat_with_ai, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text="Chat with AI!", font=self.header_font)
            ai_chat_button.place(x=250, y=550)
            self.all_screen_obj.append(ai_chat_button)

        except :
            messagebox.showerror("Invalid Career Path", "Invalid Career Path!")
            self.intro_11th_slide()
    
    def chat_with_ai(self,) :
        self.clearScreen()
        
        self.ai_box = CTk.CTkScrollableFrame(self.app, 400, 300, 0, 0, self.app_text_box_color, self.app_text_box_color)
        self.ai_box.place(x=100, y=150)
        ## Deleting ai_box requires for basically everything else to be deleted

        self.ai_entry = CTk.CTkEntry(self.app, 340, 50, 0, 0, self.app_text_box_color, self.app_text_box_color, placeholder_text="Hello, World!", font=self.header_font)
        self.ai_entry.place(x=100, y=550)
        self.all_screen_obj.append(self.ai_entry)

        send_button = CTk.CTkButton(self.app, 50, 50, 0, 0, command=self.sendMessage, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text="Send", font=self.header_font)
        send_button.place(x=350, y=550)
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

        ## Also a bit janky but also works
        self.ALL_UNIS = self.T1_UNIS + self.T2_UNIS + self.T3_UNIS + self.T4_UNIS + self.T5_UNIS


    def sendMessage(self) :
        user_input = self.ai_entry.get()
        self.ai_entry.delete(0, CTk.END)
        print(user_input)

        user_message = CTk.CTkLabel(self.ai_box, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text=user_input, font=self.text_font)
        user_message.place(x=15, y=self.current_y_ai)
        self.all_screen_obj.append(user_message)
        self.current_y_ai += int(len(user_input)/2) + 10

        ai_response = self.sendOPENAIMessage(user_input)
        print(ai_response)
        ai_message = CTk.CTkLabel(self.ai_box, bg_color=self.bg_color_light, fg_color=self.bg_color_light, text=ai_response, font=self.text_font)
        ai_message.place(x=15, y=self.current_y_ai)
        self.current_y_ai += int(len(ai_response)/2) + 10



    def sendOPENAIMessage(self, user_input) -> str :
        try :
            self.chatHistory.append({"role" : "user", "content" : user_input})

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.chatHistory,
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e :
            return f"An error occurred: {str(e)}"


var = app(CTk.CTk())