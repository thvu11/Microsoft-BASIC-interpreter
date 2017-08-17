__author__ = 'Huy Vu'
'display the menu of functions for user to choose'

import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from IfScreen import IfScreen
from RemScreen import RemScreen
from GotoScreen import GotoScreen
from PrintScreen import PrintScreen
from LetScreen import LetScreen
from AbstractScreen import AbstractScreen

from functools import partial
from string import lower

class FunctionScreen(AbstractScreen):
	#build the interface for Function screen
	def __init__(self, **kwargs):
		super(FunctionScreen, self).__init__(**kwargs)
		menu = BoxLayout(orientation='vertical', padding = 10, spacing=10)
		#title of the screen
		lbl = Label(text = "[size= 20][color=#00ffff]CHOOSE FUNCTION[/color][/size]", halign = 'left', valign= 'top', size_hint = (1, .5), markup = True)
		lbl.bind(size=lbl.setter('text_size'))
		
		#function can be used for this interpreter
		if_btn = Button(text = "IF", size_hint = (.5, .5))
		rem_btn = Button(text = "COMMENT", size_hint = (.5, .5))
		goto_btn = Button(text= "GOTO", size_hint = (.5, .5))
		print_btn = Button(text = "PRINT", size_hint = (.5, .5))
		let_btn = Button(text="LET", size_hint = (.5, .5))
		edit_btn = Button(text="EDIT", size_hint=(.5, .5))
		clear_btn = Button(text= "CLEAR THE LINE", size_hint=(.5, .5), background_color = (255, 0, 0, 1))
		#navigation back to previous screen
		back_btn = Button(text="BACK", size_hint = (.2, .2), background_color = (0, 0, 255, 1))
		back_btn.bind(on_press = partial(self.change_screen, 'back'))
		if_btn.bind(on_press = partial(self.change_screen, 'if'))
		rem_btn.bind(on_press = partial(self.change_screen, 'rem'))
		goto_btn.bind(on_press = partial(self.change_screen, 'goto'))
		print_btn.bind(on_press = partial(self.change_screen, 'print'))
		let_btn.bind(on_press = partial(self.change_screen, 'let'))
		clear_btn.bind(on_press = partial(self.change_screen, 'clear'))
		edit_btn.bind(on_press = self.edit_navigation)
		self.popup = Popup(title = 'Error', content=Label(text='No content to perform edit'), size_hint = (.4, .4))
		self.popup.dismiss()

		menu.add_widget(lbl)
		menu.add_widget(edit_btn)
		menu.add_widget(if_btn)
		menu.add_widget(rem_btn)
		menu.add_widget(goto_btn)
		menu.add_widget(print_btn)
		menu.add_widget(let_btn)
		menu.add_widget(clear_btn)
		menu.add_widget(back_btn)

		self.add_widget(menu)

	def change_screen(self,option, *args):
		change_menu = {'back': 'work_screen', 'if': 'if_screen', 'rem': 'rem_screen',
				'goto': 'goto_screen', 'print': 'print_screen', 'let': 'let_screen'}
		#choose the screen to go based on option variable
		if option == 'clear':
			#global chosen_line, line_dictionary, label_dictionary
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = ""
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (1, 1, 1, 1)
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 15
			self.manager.current = 'work_screen'
			# reset the input file
			file = open('INPUT.txt', 'w')
			file.close()
		#clean the text of a specific button
		else:
			self.manager.current = change_menu[option]

	def edit_navigation(self, *args):
		#navigate for Edit function
		#go to screen based on the keywork of that line
		if AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text == "":
			self.popup.open()
		else:
			class_menu = {'if_screen': IfScreen, 'rem': RemScreen, 'goto_screen': GotoScreen, 'print_screen': PrintScreen, 'let_screen': LetScreen}
			destination = lower(AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()[0])
			destination += '_screen'
			#navigation and parse current value to all input fields of that screen
			self.manager.current = destination
			class_menu[destination](name = destination).parse_value()
