__author__ = 'Huy Vu'
'stimulate the process of interact with input in Let function of Scratch Basic'

import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from AbstractScreen import AbstractScreen
from functools import partial


class LetScreen(AbstractScreen):
	#build the interface of Let screen
	def __init__(self, **kwargs):
		super(LetScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 5)
		#input and its label
		lbl_1 = Label(text = "LET", size_hint = (.2, .5))
		self.input_1 = TextInput(hint_text = 'New variable', size_hint= (.8, .5), multiline = False)
		lbl_2 = Label(text = "=", size_hint = (.2,.5))
		self.input_2  = TextInput(hint_text = "Assigned variable or value", size_hint= (.8, .5), multiline = False)
		self.input_3  = TextInput(hint_text = "Assigned variable or value", size_hint= (.8, .5), multiline = False)
		#navigation button
		back_btn = Button(text = "BACK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.back_to_function_screen, self))

		ok_btn = Button(text = "OK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		ok_btn.bind(on_press = self.confirm_screen)
	
		expression = BoxLayout(orientation = 'horizontal', size_hint_y = .5)
		self.lbl_add = Button(text = "+", bold=True, font_size=50, size_hint_x = .5, background_color=(128,0,0,1))
		self.lbl_add.bind(on_press = partial(self.chosen_label,1))
		expression.add_widget(self.lbl_add)

		self.lbl_sub = Button(text= "-", bold=True, font_size=50, size_hint_x = .5, pos_hint={'right':.9})
		self.lbl_sub.bind(on_press=partial(self.chosen_label, 0))
		expression.add_widget(self.lbl_sub)

		self.lbl_mul = Button(text= "x", bold=True, font_size=50, size_hint_x = .5, pos_hint={'right':.9})
		self.lbl_mul.bind(on_press=partial(self.chosen_label, 2))
		expression.add_widget(self.lbl_mul)

		self.lbl_div = Button(text= "/", bold=True, font_size=50, size_hint_x = .5, pos_hint={'right':.9})
		self.lbl_div.bind(on_press=partial(self.chosen_label, 3))
		expression.add_widget(self.lbl_div)
		
		guidance = Button(text='?', background_color = (128, 0, 128, 1), size_hint = (.1, .3), pos_hint={'right':1})
		guidance.bind(on_press = partial(self.guide, 'let'))

		self.popup = Popup(title="Error", content=Label(text="Please enter a valid input!"), size_hint= (.4, .4))
		self.popup.dismiss()

		condition = BoxLayout(orientation = 'horizontal')
		condition.add_widget(lbl_1)
		condition.add_widget(self.input_1)
		result = BoxLayout(orientation = 'horizontal')
		result.add_widget(lbl_2)
		result.add_widget(self.input_2)
		
		result1 = BoxLayout(orietation='horizontal')
		result1.add_widget(Label(text = "", size_hint = (.2,.5)))
		result1.add_widget(self.input_3)

		layout.add_widget(guidance)
		layout.add_widget(condition)
		layout.add_widget(result)
		layout.add_widget(Label(text="CHOOSE OPERATOR", size_hint_y = .3))
		layout.add_widget(expression)
		layout.add_widget(result1)
		layout.add_widget(back_btn)
		layout.add_widget(ok_btn)
		
	
		self.add_widget(layout)	
	
	def chosen_label(self, option, *args):
		if option == 1:
			self.lbl_add.background_color = (128, 0, 0, 1)
			self.lbl_sub.background_color = (1, 1, 1, 1)
			self.lbl_div.background_color = (1, 1, 1, 1)
			self.lbl_mul.background_color = (1, 1, 1, 1)
		elif option == 0:
			self.lbl_sub.background_color = (128, 0, 0, 1)
			self.lbl_add.background_color = (1, 1, 1, 1)
			self.lbl_mul.background_color = (1, 1, 1, 1)
			self.lbl_div.background_color = (1, 1, 1, 1)
		elif option == 2:
			self.lbl_mul.background_color = (128, 0, 0, 1)
			self.lbl_add.background_color = (1, 1, 1, 1)
			self.lbl_sub.background_color = (1, 1, 1, 1)
			self.lbl_div.background_color = (1, 1, 1, 1)
		else:
			self.lbl_div.background_color = (128, 0, 0, 1)
			self.lbl_add.background_color = (1, 1, 1, 1)
			self.lbl_mul.background_color = (1, 1, 1, 1)
			self.lbl_sub.background_color = (1, 1, 1, 1)

	def confirm_screen(self, *args):
		#check if any text input is valid and edit the content of chosen line
		if len(self.input_1.text.split()) == 1 and len(self.input_2.text.split()) == 1 and len(self.input_3.text.split()) == 1:
			#global chosen_line, line_dictionary, label_dictionary
			if self.lbl_add.background_color == [128, 0, 0, 1]:
				exp = " + "
			elif self.lbl_sub.background_color == [128, 0, 0, 1]:
				exp = " - "
			elif self.lbl_mul.background_color == [128, 0, 0, 1]:
				exp = " * "
			else:
				exp = " / "
			
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "LET " + self.input_1.text + " = " + self.input_2.text + exp + self.input_3.text
			#highlight the line that has input
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (255, 255, 0, 1)
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 25
			#reset all the fields
			self.input_1.select_all()
			self.input_2.select_all()
			self.input_3.select_all()
			self.manager.current = 'work_screen'
		else:
			self.popup.open()

	def parse_value(self):
		#parse current data for Edit function
		edited_data = AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()
		#print edited_data
		self.input_1.text = edited_data[1]
		self.input_2.text = edited_data[3]
		self.input_3.text = edited_data[5]
		expression = edited_data[2]
		if expression == '+':
			self.chosen_label(1)
		elif expression == '-':
			self.chosen_label(0)
		elif expression == '*':
			self.chosen_label(2)
		elif expression == '/':
			self.chosen_label(3)

