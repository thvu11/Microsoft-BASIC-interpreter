__author__ = 'Huy Vu'
'build the work space and text console for the program, support save, load, run code in the workspace'

import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.utils import escape_markup

from functools import partial
import os
from insertion_sort import insertion_sort
import dumbbasic_mod

from AbstractScreen import AbstractScreen

class WorkSpaceScreen(AbstractScreen):
	def __init__(self, **kwargs):
		super(WorkSpaceScreen, self).__init__(**kwargs)
		#global line_dictionary
		#global label_dictionary
		#scroll bar and block of lines
		if not os.path.exists(os.getcwd() + '/saved'):
			os.makedirs(os.getcwd() + '/saved')
		layout_line = GridLayout(cols=2, size_hint_y=None, padding = 20)
		layout_line.bind(minimum_height=layout_line.setter('height'))
		for i in range(1,301):
			#store all lines in a dictionary
    			self.btn = Button(id=str(i),text="", size_hint_y=None, height=40)
			AbstractScreen.line_dictionary[self.btn.id] = self.btn
			callback = partial(self.change_screen, self.btn.id)
			self.btn.bind(on_press = callback)
			line_number = Label(text=str(i), size_hint=(.1,1))
			AbstractScreen.label_dictionary[str(i)] = line_number
			layout_line.add_widget(line_number)
    			layout_line.add_widget(self.btn)
		scroll = ScrollView(size_hint=(1, 1.5))
		scroll.add_widget(layout_line)
		#entired work space
		work_space = BoxLayout(orientation='vertical')
		work_space.add_widget(scroll)
		#run button
		button_menu = BoxLayout(orientation='horizontal', size_hint_y = .2)
		run_btn = Button(text="RUN", background_color = (0, 0, 255, 1))
		run_btn.bind(on_press = self.execute_code)

		save_btn = Button(text="SAVE", background_color = (0, 0, 255, 1))
		save_btn.bind(on_press = partial(self.save_code, 0))
		
		load_btn = Button(text="LOAD", background_color = (0, 0, 255, 1))
		load_btn.bind(on_press = partial(self.save_code, 1))

		back_btn = Button(text="BACK", background_color = (0, 0, 255, 1))
		back_btn.bind(on_press = partial(self.save_code, 2))
		
		button_menu.add_widget(run_btn)
		button_menu.add_widget(save_btn)
		button_menu.add_widget(load_btn)
		button_menu.add_widget(back_btn)

		work_space.add_widget(button_menu)
		
		
		#output console
		out_layout = BoxLayout(orientation='vertical', padding = 10)
		self.text_console = Label(title='text console', text="", valign = 'top', halign = 'left', size_hint_y = None, padding=(10, 10))
		
		self.text_console.height =5000
		#print(out_layout.size)
		with self.text_console.canvas:
			Color(255, 255, 255, .5)
			Rectangle(pos = self.text_console.pos, size=(1000,200))
		self.text_console.bind(size=self.text_console.setter('text_size'))
		scroll_text_console = ScrollView(size_hint=(1,.8))
		scroll_text_console.add_widget(self.text_console)
		out_layout.add_widget(scroll_text_console)
		work_space.add_widget(out_layout)
		#work_space.add_widget(scroll_text_console)
		
		self.add_widget(work_space)

	def change_screen(self, i, *args):
		#global chosen_line, touch_mode, line_dictionary, label_dictionary
		if not AbstractScreen.touch_mode:
			self.manager.current = 'function_screen'
			AbstractScreen.chosen_line = i
		else:
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "GOTO " + str(i)
			AbstractScreen.touch_mode = False
		
		#print i
		#print chosen_line

	def execute_code(self, *args):
		#global line_dictionary
		tmp_list = []
		self.text_console.text = "\n\n"
		#find all the lines that have user's input
		for value in AbstractScreen.line_dictionary.keys():
			if AbstractScreen.line_dictionary[value].text != "":
				tmp_list.append(int(value))
		#sort the line
		insertion_sort(tmp_list)
		#write all the input into a text INPUT file
		file = open("INPUT.txt",'w')
		for item in tmp_list:
			file.write(str(item) + ' ' + AbstractScreen.line_dictionary[str(item)].text + '\n')
		file.close()
		#update the text console
		#run through the intepreter
		file = open("INPUT.txt", 'r')
		check = file.read().strip('\n').split()
		file.close()
		#only run if the INPUT.txt is not empty
		if check:
			dumbbasic_mod.main()
			file = open("output.txt", 'r')
			for line in file:
				self.text_console.text += '         ' + line
		
			file.close()
		else:
			self.text_console.text += '         No input'

	def save_code(self, option, *args):
		if option == 0:
			self.manager.current = 'save_screen'
		elif option == 1:
			self.manager.current = 'load_screen'
		else:
			self.manager.current = 'welcome_screen'


