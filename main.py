import customtkinter as CTk, requests, os
import openai
import score, clubs, awards, sports, AP
from tkinter import messagebox

with open("APIKEY.config") as api_key_file :
    openai.api_key = api_key_file.read()

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
        "Seminar"
        "CSP",
    ]

    AP_T5 = [
        "Art & Design",
    ]

    ALL_APS = AP_T1 + AP_T2 + AP_T3 + AP_T4 + AP_T5
    ALL_APS.sort()

    taken_APs = []
    sat_score = 1050 ## Assume Nat. Avg.

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
        self.app.title("ConsulAI") 
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

        app_name = CTk.CTkLabel(header, text="ConsulAI", fg_color=self.bg_color_light, bg_color=self.bg_color_light, font=self.header_font)
        app_name.place(x=20, y=12) ## This places the text 50 px below the top and 51 px above the header border... >:-(

        settings_button = CTk.CTkButton(header, text="⚙️", font=self.header_font, fg_color=self.bg_color_light, hover_color=self.bg_color, border_width=0, command = lambda : self.director("SettingButton"), width=60, height=50)
        settings_button.place(x=525, y=12)

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
        intro_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Welcome to ConsulAI!", font=self.header_font)
        intro_text.place(x=0, y = 150)
        self.all_screen_obj.append(intro_text)

        intro_text_2 = CTk.CTkLabel(self.app, 600, 75, bg_color=self.bg_color, fg_color=self.bg_color, text="A free AI-based college consuling application!", font=self.text_font)
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
        back_button.place(x=150, y=400)
        self.all_screen_obj.append(back_button)

        next_button = CTk.CTkButton(self.app, text="Next", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command=self.intro_4th_slide, width=100, height=50)
        next_button.place(x=350, y=400)
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
            yes_aps.place(x=150, y=375)
            self.all_screen_obj.append(yes_aps)

            no_aps = CTk.CTkButton(self.app, 75, 30, font=self.text_font, text="No", command=self.intro_5th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_aps.place(x=375, y=375)
            self.all_screen_obj.append(no_aps)

            back_button = CTk.CTkButton(self.app, text="Back", font=self.text_font, fg_color=self.bg_color_light, bg_color=self.bg_color, hover_color=self.bg_color, border_width=0, command = self.intro_3rd_slide, width=100, height=50)
            back_button.place(x=250, y=450)
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

            yes_ap = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_4th_slide_ap_selector, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            yes_ap.place(x=150, y=450)
            self.all_screen_obj.append(yes_ap)

            no_ap = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_5th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
            no_ap.place(x=375, y=450)
            self.all_screen_obj.append(no_ap)

        except Exception as err:
            print(err)

    def intro_5th_slide(self,) :
        self.clearScreen()
        sat_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you taken the SAT yet?", font=self.header_font)
        sat_text.place(x=0, y = 150)
        self.all_screen_obj.append(sat_text)

        yes_sat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_5th_slide_sat_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_sat.place(x=150, y=400)
        self.all_screen_obj.append(yes_sat)

        no_sat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_5th_slide_psat, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
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

        yes_psat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_5th_slide_psat_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_psat.place(x=150, y=450)
        self.all_screen_obj.append(yes_psat)

        no_psat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_6th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_psat.place(x=375, y=450)
        self.all_screen_obj.append(no_psat)

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

        yes_psat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Back", command=self.intro_5th_slide_psat, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_psat.place(x=150, y=450)
        self.all_screen_obj.append(yes_psat)

        no_psat = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Next", command=self.intro_5th_slide_psat_score_validator, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
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

        yes_act = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_6th_slide_act_score, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_act.place(x=150, y=450)
        self.all_screen_obj.append(yes_act)

        no_act = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_7th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_act.place(x=375, y=450)
        self.all_screen_obj.append(no_act)
    
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
        clubs_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Were you apart of any clubs?", font=self.header_font)
        clubs_text.place(x=0, y = 150)
        self.all_screen_obj.append(clubs_text)

        yes_clubs = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_7th_slide_club_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_clubs.place(x=150, y=450)
        self.all_screen_obj.append(yes_clubs)

        no_clubs = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_8th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_clubs.place(x=375, y=450)
        self.all_screen_obj.append(no_clubs)

    def intro_7th_slide_club_entry(self,) :
        self.clearScreen()

    def intro_7th_slide_club_entry_validator(self,) :
        self.clearScreen()

    def intro_8th_slide(self,) :
        self.clearScreen()
        sports_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Did you participate in any sports?", font=self.header_font)
        sports_text.place(x=0, y = 150)
        self.all_screen_obj.append(sports_text)

        yes_sports = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_8th_slide_sports_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_sports.place(x=150, y=450)
        self.all_screen_obj.append(yes_sports)

        no_sports = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_9th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_sports.place(x=375, y=450)
        self.all_screen_obj.append(no_sports)
    
    def intro_8th_slide_sports_entry(self,) :
        self.clearScreen()
    
    def intro_8th_slide_sports_entry_validator(self,) :
        self.clearScreen()
    
    def intro_9th_slide(self,) :
        self.clearScreen()

        challenge_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Have you participated in\nany challenges?", font=self.header_font)
        challenge_text.place(x=0, y = 150)
        self.all_screen_obj.append(challenge_text)

        yes_challenges = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_9th_slide_challenges_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_challenges.place(x=150, y=450)
        self.all_screen_obj.append(yes_challenges)

        no_challenges = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.intro_10th_slide, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_challenges.place(x=375, y=450)
        self.all_screen_obj.append(no_challenges)

    def intro_9th_slide_challenges_entry(self,) :
        self.clearScreen()
    
    def intro_9th_slide_challenges_entry_validator(self,) :
        self.clearScreen()

    def intro_10th_slide(self,) :
        self.clearScreen()

        awards_text = CTk.CTkLabel(self.app, 600, 80, bg_color=self.bg_color, fg_color=self.bg_color, text="Did you recieve any awards?", font=self.header_font)
        awards_text.place(x=0, y = 150)
        self.all_screen_obj.append(awards_text)

        yes_awards = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="Yes", command=self.intro_10th_slide_award_entry, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        yes_awards.place(x=150, y=450)
        self.all_screen_obj.append(yes_awards)

        no_awards = CTk.CTkButton(self.app, 75, 30, font=self.button_font, text="No", command=self.generate_report, border_width=0, border_color=self.bg_color, bg_color=self.bg_color, fg_color=self.bg_color_light)
        no_awards.place(x=375, y=450)
        self.all_screen_obj.append(no_awards)

    def intro_10th_slide_award_entry(self,) :
        self.clearScreen()
    
    def intro_10th_slide_award_entry_validator(self,) :
        self.clearScreen()

    def intro_11_slide(self,) :
        self.clearScreen()

    def generate_report(self,) :
        self.clearScreen()

    

var = app(CTk.CTk())
