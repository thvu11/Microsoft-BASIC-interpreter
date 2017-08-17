__author__ = 'Huy Vu'
'stimulate the process of interact with input in If-Goto function of Scratch Basic'

import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from AbstractScreen import AbstractScreen
from functools import partial

class IfScreen(AbstractScreen):
	def __init__(self, **kwargs):
		super(IfScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 5)
		#label and text input for each field
		lbl_1 = Label(text = "IF", size_hint = (.2, .5))
		self.input_1 = TextInput(hint_text = 'Condition', size_hint= (.8, .5), multiline = False)
		self.input_3 = TextInput(hint_text = 'Condition', size_hint= (.8, .5), multiline = False)
		lbl_2 = Label(text = "GOTO", size_hint = (.2,.5))
		self.input_2 = TextInput(hint_text = "Line number", size_hint= (.8, .5), multiline = False)
		#navigation button
		back_btn = Button(text = "BACK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.back_to_function_screen, self))

		ok_btn = Button(text = "OK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		ok_btn.bind(on_press = self.confirm_screen)
		#choosing expression with checkbox
		expression = BoxLayout(orientation = 'horizontal', size_hint_y = .5)
		self.lbl_larger = Button(text = ">", bold=True, font_size=50,size_hint_x = .3, background_color = (128,0,0,1))
		self.lbl_larger.bind(on_press= partial(self.on_active, 1))
		expression.add_widget(self.lbl_larger)

		self.lbl_smaller = Button(text = "<", bold=True, font_size=50,size_hint_x = .3, pos_hint={'right':.9})
		self.lbl_smaller.bind(on_press= partial(self.on_active, 3))
		expression.add_widget(self.lbl_smaller)

		self.lbl_equal = Button(text = "==", bold=True, font_size=50,size_hint_x = .3, pos_hint={'right':.9})
		self.lbl_equal.bind(on_press= partial(self.on_active, 2))
		expression.add_widget(self.lbl_equal)

		guidance = Button(text='?',  background_color = (128, 0, 128, 1), size_hint = (.1, .3), pos_hint={'right':1})

		guidance.bind(on_press = partial(self.guide, 'if'))

		self.popup = Popup(title="Error", content=Label(text="Please enter a valid input!"), size_hint= (.4, .4))
		self.popup.dismiss()

		condition = BoxLayout(orientation = 'horizontal')
		condition.add_widget(lbl_1)
		condition.add_widget(self.input_1)

		condition1 = BoxLayout(orientation = 'horizontal')
		condition1.add_widget(Label(text = "", size_hint = (.2, .5)))
		condition1.add_widget(self.input_3)

		result = BoxLayout(orientation = 'horizontal')
		result.add_widget(lbl_2)
		result.add_widget(self.input_2)
		layout.add_widget(guidance)
		layout.add_widget(condition)
		layout.add_widget(Label(text = "CHOOSE OPERATOR"))
		layout.add_widget(expression)
		layout.add_widget(condition1)
		layout.add_widget(result)
		layout.add_widget(back_btn)
		layout.add_widget(ok_btn)
		
	
		self.add_widget(layout)	

	def on_active(self, option, *args):
		#ensure only one checkbox can be chosen
		if option == 1:
			self.lbl_larger.background_color = (128,0,0,1)
			self.lbl_equal.background_color = (1,1,1,1)
			self.lbl_smaller.background_color = (1,1,1,1)
		elif option == 2:
			self.lbl_equal.background_color = (128,0,0,1)
			self.lbl_larger.background_color = (1,1,1,1)
			self.lbl_smaller.background_color = (1,1,1,1)
		else:
			self.lbl_smaller.background_color = (128,0,0,1)
			self.lbl_larger.background_color = (1,1,1,1)
			self.lbl_equal.background_color = (1,1,1,1)

	def confirm_screen(self, *args):
		#check if any input field contains space or tab only
		if len(self.input_1.text.split()) == 1 and len(self.input_2.text.split()) == 1 and len(self.input_3.text.split()) == 1:
			#global chosen_line, line_dictionary, label_dictionary
			if self.lbl_larger.background_color == [128,0,0,1]:
				exp = " > "
			elif self.lbl_equal.background_color == [128,0,0,1]:
				exp = " == "
			else:
				exp = " < "
			AbstractScreen.line_dictionary[str(AbstractScreen.chosen_line)].text = "IF " + self.input_1.text + exp + self.input_3.text + " GOTO " + self.input_2.text 
			#highlighted the line that have input
			AbstractScreen.label_dictionary[str(AbstractScreen.chosen_line)].color = (255, 255, 0, 1)
			AbstractScreen.label_dictionary[str(AbstractScreen.chosen_line)].font_size = 25
			#reset all the fields
			self.input_1.select_all()
			self.input_2.select_all()
			self.input_3.select_all()
			self.manager.current = 'work_screen'
		else:
			self.popup.open()

	def parse_value(self):
		edited_data = AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()
		#print edited_data
		self.input_1.text = edited_data[1]
		self.input_2.text = edited_data[3]
		self.input_3.text = edited_data[5]
		expression = edited_data[2]
		if expression == '>':
			self.on_active(1)
		elif expression == '<':
			self.on_active(3)
		elif expression == '==':
			self.on_active(2)
