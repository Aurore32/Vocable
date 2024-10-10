import tkinter
import tkinter.messagebox
import customtkinter
import catsim.irt
import numpy as np
from datetime import datetime
from quiz_brain import QuizBrain
from fpdf import FPDF
import fpdf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker 
import os
import userpaths

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(1.3)

class QuizInterface(customtkinter.CTk):
    def __init__(self, quiz_brain: QuizBrain) -> None:
        super().__init__()
        self.quiz = quiz_brain
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.information_entered = False
        self.score = 0
        self.name = ""
        self.grade = ""
        self.pdf = FPDF()
        self.pdf.add_font("Simhei", style="", fname = "SIMHEI.TTF")
        self.final_score = 0
        self.color_palette = {
            True: 'lime',
            False: 'red'
        }

        # configure window
        self.title("Vocable 1.0")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.iconbitmap("vocable_icon.ico")

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vocable 1.0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                    command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["130%", "140%", "150%", "160%", "170%", "180%", "190%", "200%"],
                                                            command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.textbox = customtkinter.CTkTextbox(self, width=80, font=customtkinter.CTkFont(size=16, weight='normal'), wrap='word')
        self.textbox.grid(row=0, column=1, columnspan = 3, padx=(20, 60), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "\nWelcome to Vocable, a self-adapting vocabulary test for identifying your vocabulary level!\n \n The test will be approximately 50 questions long. \n \n Each question will ask you for the correct definition of a word from four answer choices. \n \n The test is self-adaptive, giving you harder questions if you answer correctly. \n \n Please enter your full name (first and last) and grade below; once entered, click \"Begin\" to start. \n \n Good luck, and have fun!")
        self.textbox.configure(state='disabled')
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter your name...", textvariable=self.name)
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", command=self.check_info, border_width=2, text_color=("gray10", "#DCE4EE"), text='Begin!', width=100, height=40)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.grade_menu = customtkinter.CTkOptionMenu(self, values=["Choose...", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], command=self.set_grade)   
        self.grade_menu.grid(row=3, column=2, padx=(20,20), pady=(10, 20))
        self.grade_menu_label = customtkinter.CTkLabel(self, text="Grade level:", anchor="w")
        self.grade_menu_label.grid(row=3, column=2, padx=20, pady=(0, 80))
        self.mainloop()
        
    def radio_buttons(self):
        options = self.quiz.current_question.choices

        self.radiobutton_frame = customtkinter.CTkFrame(self, fg_color='sky blue')
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Answer choices: ")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.user_answer, value=options[0], text=options[0])
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.user_answer, value=options[1], text=options[1])
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.user_answer, value=options[2], text=options[2])
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.user_answer, value=options[3], text=options[3])
        self.radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="n")

    
    def display_question(self):
        q_text = self.quiz.next_question()
        self.textbox.insert("0.0", q_text)
        self.textbox.configure(state='disabled')
        
        
    def next_button(self):
        """To show feedback for each answer and keep checking for more questions"""

        if self.quiz.has_more_questions() == False:
            # Moves to next to display next question and its options
            self.quiz.check_answer(self.user_answer.get())
            self.radiobutton_frame.destroy()
            self.textbox.destroy()
            self.progressbar.destroy()
            self.entry.destroy()

            self.textbox = customtkinter.CTkTextbox(self, width=100, font=customtkinter.CTkFont(size=16, weight='bold'), wrap='word')
            self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

            self.progressbar = customtkinter.CTkProgressBar(master=self, progress_color='deep sky blue', height=20, border_color='azure', border_width=5)
            self.progressbar.grid(row=2, column=1, columnspan=3, padx=(20, 20), pady=(5, 5), sticky="sew")
            self.progressbar.set(1 - (catsim.irt.see(theta=self.quiz.ability, items=self.quiz.difficulty_matrix[self.quiz.administered_items]) - 0.3)/1.7)

            self.entry = customtkinter.CTkEntry(self, placeholder_text="{} -- Grade {} -- Question {}".format(self.name, self.grade, self.quiz.question_no+1))
            self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
            self.entry.configure(state='disabled')

            self.display_question()
            self.radio_buttons()
        
        else:

            self.documents = userpaths.get_my_documents()
            print(self.documents)
            self.path='{}\\Vocable Reports'.format(self.documents)
            print(self.path)
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            self.language = tkinter.messagebox.askyesno(title='Quiz completion', message="Quiz completed - thank you for using Vocable! A report will be generated in a few seconds.\n\nDo you want the report to be generated in English? Press \'Yes\' for English, \'No\' for Chinese...")

            self.quiz.check_answer(self.user_answer.get())
            self.quiz.question_list.append(self.quiz.question_no)
            self.quiz.question_list.pop(0)
            self.grade_scores = self.difficulty_to_grade(np.array(self.quiz.ability_scores))
            print(self.grade_scores)
            print(self.quiz.question_list)
            self.final_score = float(self.difficulty_to_grade(self.quiz.ability))
            if self.final_score < 1.5:
                self.final_score = 1.5
            else:
                self.final_score = round(self.final_score, ndigits=1)
            self.grade_level, self.month_level = divmod(self.final_score, 1)
            self.grade_level = int(self.grade_level)
            self.difficulty_vector = np.round(self.difficulty_to_grade(np.array(self.quiz.difficulty_matrix[self.quiz.administered_items][:,1]))).tolist()
            print(self.difficulty_vector)
            self.dict = {'Questions Completed': self.quiz.administered_items,
                         'Answer Values': self.quiz.response_vector,
                         'Grade Level': self.difficulty_vector}
            self.df = pd.DataFrame(data=self.dict)
            self.df_counts = self.df.groupby(['Grade Level', 'Answer Values']).size().reset_index().pivot(columns='Answer Values', index='Grade Level', values=0)
            print(self.df_counts)

            # Bar plot
            matplotlib.rc('font', family='Arial')
            ax = self.df_counts.plot.bar(stacked=True, color=self.color_palette, edgecolor='black', linewidth=2)
            ax.set_xlabel('Grade Level of Word', font='Arial', fontsize=20)
            ax.set_ylabel('No.\nof\nQuestions', font='Arial', fontsize=20, rotation=0)
            plt.xticks(font='Arial', fontsize=16, rotation=0)
            plt.yticks(font='Arial', fontsize=16, rotation=0)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.yticks(ticks=plt.yticks()[0], labels=plt.yticks()[0].astype(int))
            plt.xticks(ticks=plt.xticks()[0], labels=plt.xticks()[0].astype(int))
            ax.legend(loc='upper left', labels=['Incorrect', 'Correct'], fontsize=20)
            for bars in ax.containers:
                ax.bar_label(bars)
            fig = ax.get_figure()
            fig.set_size_inches(16,9)
            fig.savefig('{}\\words_correct_per_grade_{}.png'.format(self.path, self.name), bbox_inches='tight', dpi=100)
            plt.clf()


            # Score gradient
            self.colormap_grade_scale = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","yellow", "green"])
            plt.imshow([[0.,1.], [0.,1.]], 
            cmap = self.colormap_grade_scale, 
            interpolation = 'bicubic',
            extent=[1,13,-0.375,0.375])
            plt.plot(self.final_score, -0.5, color='black', marker='^')
            plt.plot(self.final_score, 0.5, color='black', marker='v')
            plt.plot([self.final_score, self.final_score], [0.5,-0.5], color='black', marker='_')
            plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], font='Arial')
            plt.yticks([])
            
            plt.savefig('{}\\scaled_score_{}.png'.format(self.path, self.name), bbox_inches='tight', dpi=1200)
            plt.clf()

            # Vocabulary attainment plot
                
            self.vocabplot_x = np.array(sorted([0,1,2,3,4,5,6,7,8,9,10,11,12,13,round(self.final_score, 1)])).astype(float)
            self.pos_of_final = self.vocabplot_x.tolist().index(round(self.final_score,1))
            self.pos_of_grade = self.vocabplot_x.tolist().index(float(self.grade))
            self.vocabplot_y = (self.grade_to_vocab(self.vocabplot_x)/100).round() * 100
            self.vocab_size = round(self.grade_to_vocab(float(self.final_score)) / 100) * 100
            self.exp_vocab_size = round(self.grade_to_vocab(float(self.grade)) / 100) * 100
            self.vocab_palette = sns.hls_palette(n_colors=14, l=.9)
            self.vocab_palette.insert(self.pos_of_final, (1,0,0))
            self.vocab_palette.pop(self.pos_of_grade)
            self.vocab_palette.insert(self.pos_of_grade, (0,1,0))
            self.edgecolors = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']
            self.edgecolors.insert(self.pos_of_final, 'darkred')
            self.edgecolors.pop(self.pos_of_grade)
            self.edgecolors.insert(self.pos_of_grade, 'darkred')
            axes = sns.barplot(x=self.vocabplot_x, y=self.vocabplot_y, palette=self.vocab_palette, edgecolor=self.edgecolors, linewidth=1.5)
            axes.set_xlabel('Grade Level', fontsize=20, rotation=0)
            axes.set_ylabel('Vocabulary Size', fontsize=20, rotation=0)
            plt.yticks(size=16)
            plt.xticks(size=16)
            axes.get_xticklabels()[self.pos_of_final].set_weight('bold')
            axes.get_xticklabels()[self.pos_of_final].set_fontsize(18)
            axes.get_xticklabels()[self.pos_of_final].set_bbox(dict(facecolor="whitesmoke"))
            axes.get_xticklabels()[self.pos_of_grade].set_weight('bold')
            axes.get_xticklabels()[self.pos_of_grade].set_fontsize(18)
            axes.get_xticklabels()[self.pos_of_grade].set_bbox(dict(facecolor="whitesmoke"))
            
            self.labels=['Current level\nEstimated vocabulary: {}'.format(self.vocab_size, self.grade), 'Expected level at grade {}\nExpected vocabulary: {}'.format(self.grade, round(self.grade_to_vocab(float(self.grade)) / 100) * 100)]
            self.artists=[plt.Rectangle((0,0),1,1, color='red'), plt.Rectangle((0,2),1,1, color='lime')]
            axes.legend(handles=self.artists, labels=self.labels, loc='upper left', fontsize=17)
            for bars in axes.containers:
                axes.bar_label(bars, fontsize=16)
            fig = axes.get_figure()
            fig.set_size_inches(16,9)
            fig.savefig('{}\\vocabulary_size_{}.png'.format(self.path, self.name), bbox_inches='tight', dpi=100)
            plt.clf()

            # Catsim test progress plot
            self.grade_scores.tolist()
            axes = plt.plot(self.quiz.question_list, self.difficulty_vector, color='orangered', linewidth=1, marker='^', label='Question Grade Level')
            plt.plot(self.quiz.question_list, self.grade_scores, color='magenta', linewidth=1, marker='o', label='Your Estimated Grade Level')
            plt.axhline(y=self.final_score, color='deepskyblue', label='Your Final Score')
            plt.legend(fontsize=17)
            plt.xlabel('Question Number', fontsize=20, rotation=0)
            plt.ylabel('Grade\nLevel', fontsize=20, rotation=0)
            plt.yticks(size=16)
            plt.xticks(size=16)
            loc, labels = plt.xticks()
            plt.xticks(np.arange(1, max(loc), step=3))
            plt.savefig('{}\\quiz_progress_{}'.format(self.path, self.name), bbox_inches='tight', dpi=100)
            
            if self.language == True:
                self.ReportGen(self.pdf)
            if self.language == False:
                self.ReportGen_zh(self.pdf)
            self.destroy()
            
    
    def display_options(self):
        """To display four options"""

        val = 0

        # deselecting the options
        self.user_answer.set(None)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def set_grade(self, grade: str):
        self.grade = grade
    
    def grade_to_difficulty(self, grade: float):
        return -(np.log((17.964042153403764 - 4.916490600870272 - grade)/(grade + 4.916490600870272)) / 2.6314356784524997) - 0.6960783308308821
    
    def difficulty_to_grade(self, difficulty: float):    
        return (17.964042153403764) / (1 + np.exp(-2.6314356784524997*(difficulty+0.6960783308308821))) - 4.916490600870272

    def grade_to_vocab(self, grade: float):
        return 31000 * np.exp(-3.5 * np.exp(-0.128 * (grade + 2)))
    
    def check_info(self):
        self.name = self.entry.get()
        if self.name != "" and self.grade != "" and self.grade != "Choose...":
                
            self.grade_menu_label.destroy()
            self.textbox.destroy()
            self.main_button_1.destroy()
            self.entry.destroy()
            self.grade_menu.destroy()

            self.title("Vocable v1.0")
            self.geometry(f"{1100}x{580}")
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vocable 1.0\n\n{}\nGrade {}".format(self.name, self.grade), font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
            self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode_event)
            self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
            self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
            self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["130%", "140%", "150%", "160%", "170%", "180%", "190%", "200%"],
                                                                command=self.change_scaling_event)
            self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
            
        # create textbox
            self.textbox = customtkinter.CTkTextbox(self, width=100, font=customtkinter.CTkFont(size=16, weight='bold'), wrap='word')
            self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        
            self.user_answer = tkinter.StringVar()

            self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.next_button, text='Next', width=15, height=40)
            self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

            self.entry = customtkinter.CTkEntry(self, placeholder_text="{} -- Grade {} -- Question {}".format(self.name, self.grade, self.quiz.question_no+1))
            self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
            self.entry.configure(state='disabled')

            self.progressbar = customtkinter.CTkProgressBar(master=self, progress_color='deep sky blue', height=20, border_color='azure', border_width=5)
            self.progressbar.grid(row=2, column=1, columnspan=3, padx=(20, 20), pady=(5, 5), sticky="sew")
            self.progressbar.set(0)
            self.quiz.ability = self.grade_to_difficulty(float(self.grade))
            print(self.quiz.ability)

            self.display_question()
            self.radio_buttons()
            self.mainloop()

        elif len(self.name) > 15:
            self.information_entered = False
            self.invalidname_label = customtkinter.CTkLabel(self, text="Name too long!", anchor="w", text_color='red')
            self.invalidname_label.grid(row=2, column=3, padx=20, pady=(0, 0))
            self.after(2000, self.invalidname_label.destroy)
    
        else:
            self.information_entered = False
            self.invalidname_label = customtkinter.CTkLabel(self, text="Name or grade invalid!", anchor="w", text_color='red')
            self.invalidname_label.grid(row=2, column=3, padx=20, pady=(0, 0))
            self.after(2000, self.invalidname_label.destroy)

    def ReportGen(self, pdf: FPDF):
        for f in os.listdir(self.path):
            if not f.endswith(".pdf"):
                continue
            os.remove(os.path.join(self.path, f))
        pdf = FPDF(orientation='p', unit='mm', format='A4')
        pdf.set_page_background('report_template_1.jpg')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(35)
        pdf.cell(60, 0, 'Vocabulary Report for {}'.format(self.name), ln=1)
        pdf.cell(165)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 0, 'Vocable v1.0', ln=1)
        pdf.ln()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(35)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, 'Grade: {}'.format(self.grade), ln=1)
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, 'Date: {}'.format(self.date))
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        if self.final_score == 1:
            pdf.cell(0, 0, 'Scaled Score: 1 (or lower)')
        else:
            pdf.cell(0, 0, 'Scaled Score: {}'.format(self.final_score))
        pdf.image('{}\\scaled_score_{}.png'.format(self.path, self.name), x=45, y=50, w=160, h=26)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        pdf.cell(35)
        pdf.multi_cell(0, 5, '{}\'s vocabulary currently corresponds to that of a Grade {} level after {} months of study.'.format(self.name, self.grade_level, round(self.month_level * 12)))
        pdf.ln()
        pdf.ln()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(35)
        pdf.cell(50, 0, 'Vocabulary Size Estimates')
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.image('{}\\vocabulary_size_{}.png'.format(self.path, self.name), x=45, y=110, w=160, h=90)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 5, '{}\'s estimated vocabulary size is {} (shown in red); as a Grade {} student, they are currently expected to master {} words (shown in green).'.format(self.name, self.vocab_size, self.grade, self.exp_vocab_size))
        pdf.ln()
        if self.vocab_size <= self.exp_vocab_size:
            pdf.cell(35)
            pdf.set_font('Arial', 'IB', 12)
            pdf.multi_cell(0, 5, '{}\' estimated vocabulary size is roughly {}% less than expected for their grade.'.format(self.name, 100 - round(self.vocab_size * 100 / self.exp_vocab_size)))
            pdf.ln()
            pdf.cell(35)
            pdf.multi_cell(0, 5, 'To catch up to their current grade level, {} will have to learn another {} words this year, or {} per month.'.format(self.name, self.exp_vocab_size-self.vocab_size, round((self.exp_vocab_size-self.vocab_size) / 12)))
        else:
            pdf.cell(35)
            pdf.set_font('Arial', 'IB', 12)
            pdf.multi_cell(0, 5, '{}\'s estimated vocabulary size is roughly {}% more than expected for their grade. Congratulations!'.format(self.name, round(self.vocab_size * 100 / self.exp_vocab_size) - 100))

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(35)
        pdf.cell(60, 0, 'Vocabulary Report for {}'.format(self.name), ln=1)
        pdf.cell(165)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 0, 'Vocable v1.0', ln=1)
        pdf.ln()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(35)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, 'Grade: {}'.format(self.grade), ln=1)
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, 'Date: {}'.format(self.date))
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)

        pdf.cell(0,0,'Vocabulary Mastery per Grade')
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.image('{}\\words_correct_per_grade_{}.png'.format(self.path, self.name), x=45, y=50, w=160, h=90)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Arial', 'I', 14)
        pdf.multi_cell(0, 5, 'The above graph demonstrates {}\'s mastery level of words for every grade level. Red indicates incorrect answers, while green indicates correct.'.format(self.name))
        pdf.ln()
        pdf.ln()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(35)
        pdf.cell(50, 0, 'Ability Level Progress')
        pdf.image('{}\\quiz_progress_{}.png'.format(self.path, self.name), x=47, y=180, w=150, h=85)
        pdf.output('{}\\report_{}.pdf'.format(self.path,self.name), 'F')

        # Deletion of files, cleanup, and opening the report
        os.startfile('{}\\report_{}.pdf'.format(self.path,self.name))
        for f in os.listdir(self.path):
            if not f.endswith(".png"):
                continue
            os.remove(os.path.join(self.path, f))

    def ReportGen_zh(self, pdf: FPDF):
        for f in os.listdir(self.path):
            if not f.endswith(".pdf"):
                continue
            os.remove(os.path.join(self.path, f))
        pdf = FPDF(orientation='p', unit='mm', format='A4')
        pdf.add_font("Simhei", style="", fname = "MSYH.TTC")
        pdf.add_font("Simhei", style="B", fname = "MSYHBD.TTC")
        pdf.set_page_background('report_template_1.jpg')
        pdf.add_page()
        pdf.set_font('Simhei', 'B', 16)
        pdf.cell(35)
        pdf.cell(60, 0, '{}的词汇报告'.format(self.name), ln=1)
        pdf.cell(165)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 0, 'Vocable v1.0', ln=1)
        pdf.ln()
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(35)
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(0, 0, '年级: {}'.format(self.grade), ln=1)
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(0, 0, '日期: {}'.format(self.date))
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        if self.final_score == 1:
            pdf.cell(0, 0, '评测分数: 1（及以下）')
        else:
            pdf.cell(0, 0, '评测分数: {}'.format(self.final_score))
        pdf.image('{}\\scaled_score_{}.png'.format(self.path, self.name), x=45, y=50, w=160, h=26)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.set_font('Simhei', '', 12)
        pdf.cell(35)
        pdf.multi_cell(0, 5, '{}的词汇量同等于一位处于学年中第{}个月的{}年级学生。'.format(self.name, round(self.month_level * 12), self.grade_level))
        pdf.ln()
        pdf.ln()
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(35)
        pdf.cell(50, 0, '词汇估量')
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.image('{}\\vocabulary_size_{}.png'.format(self.path, self.name), x=45, y=110, w=160, h=90)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Simhei', '', 12)
        pdf.multi_cell(0, 5, '经过测评，{}的预估词汇量为{}个词（详情如红条所示）; 作为一位{}年级的学生，{}满足该年级词汇水平基准前需总计掌握{}个英语单词。'.format(self.name, self.vocab_size, self.grade, self.name, self.exp_vocab_size))
        pdf.ln()
        if self.vocab_size <= self.exp_vocab_size:
            pdf.cell(35)
            pdf.set_font('Simhei', '', 12)
            pdf.multi_cell(0, 5, '{}的预算词汇量距离年级基准词汇量相差{}%。'.format(self.name, 100 - round(self.vocab_size * 100 / self.exp_vocab_size)))
            pdf.ln()
            pdf.cell(35)
            pdf.multi_cell(0, 5, '若想达到基准水平，{}需在本学年掌握{}个英文词汇，相当于于每个月学习{}个新词。'.format(self.name, self.exp_vocab_size-self.vocab_size, round((self.exp_vocab_size-self.vocab_size) / 12)))
        else:
            pdf.cell(35)
            pdf.set_font('Simhei', '', 12)
            pdf.multi_cell(0, 5, '{}的预算词汇量超越了年级基准词汇量约{}%。恭喜{}目前为止在英文词汇中取得的卓越进展！'.format(self.name, round(self.vocab_size * 100 / self.exp_vocab_size) - 100, self.name))

        pdf.add_page()
        pdf.set_font('Simhei', 'B', 16)
        pdf.cell(35)
        pdf.cell(60, 0, '{}的词汇报告'.format(self.name), ln=1)
        pdf.cell(165)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 0, 'Vocable v1.0', ln=1)
        pdf.ln()
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(35)
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(0, 0, '年级: {}'.format(self.grade), ln=1)
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(0, 0, '日期: {}'.format(self.date))
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)

        pdf.cell(0,0,'年级分类词汇进度展示')
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.image('{}\\words_correct_per_grade_{}.png'.format(self.path, self.name), x=45, y=50, w=160, h=90)
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.ln()
        pdf.cell(35)
        pdf.set_font('Simhei', '', 12)
        pdf.multi_cell(0, 5, '上述柱状图展示了{}在每一个年级的词汇中分别取得的测试成绩；红色与绿色区域分别代表了错误与正确题目的总数。'.format(self.name))
        pdf.ln()
        pdf.ln()
        pdf.set_font('Simhei', 'B', 14)
        pdf.cell(35)
        pdf.cell(50, 0, '测评等级分演变图')
        pdf.image('{}\\quiz_progress_{}.png'.format(self.path, self.name), x=47, y=180, w=150, h=85)
        pdf.output('{}\\report_{}.pdf'.format(self.path, self.name), 'F')

        # Deletion of files, cleanup, and opening the report
        os.startfile('{}\\report_{}.pdf'.format(self.path, self.name))
        for f in os.listdir(self.path):
            if not f.endswith(".png"):
                continue
            os.remove(os.path.join(self.path, f))

