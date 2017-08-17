__author__ = 'Darren Wong'
'stimulate the process of interact with input in Print function of Scratch Basic'

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


class PrintScreen(AbstractScreen):
	#build the interface for Print screen
	def __init__(self, **kwargs):
		super(PrintScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 5)
		lbl = Label(text = "PRINT", size_hint = (.2, .3), valign = 'top', halign = 'center')
		lbl.bind(size=lbl.setter('text_size'))
		self.input = TextInput(hint_text = "Object needs to print", size_hint = (.8, .3))
		back_btn = Button(text = "BACK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.back_to_function_screen, self))

		ok_btn = Button(text = "OK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		ok_btn.bind(on_press = self.confirm_screen)

		guidance = Button(text='?',  background_color = (128, 0, 128, 1), size_hint = (.1, .1), pos_hint={'right':1})
		guidance.bind(on_press = partial(self.guide, 'print'))

		self.popup = Popup(title="Error", content=Label(text="Please enter a valid input!"), size_hint= (.4, .4))
		self.popup.dismiss()

		layout_1 = BoxLayout(orientation='horizontal')
		layout_1.add_widget(lbl)
		layout_1.add_widget(self.input)

		layout.add_widget(guidance)
		layout.add_widget(layout_1)
		layout.add_widget(back_btn)
		layout.add_widget(ok_btn)

		self.add_widget(layout)

	def confirm_screen(self, *args):
		#check if text input is valid and edit the content of specific line
		if len(self.input.text.split()) == 1:
			#change the content and highlight associated line number
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "PRINT " + self.input.text
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (255, 255, 0, 1)
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 25
			self.input.select_all()
			self.manager.current = 'work_screen'
		else:
			self.popup.open()

	def parse_value(self):
		#parse current value for Edit function
		edited_data = AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()
		#print edited_data[1]
		self.input.text = edited_data[1]



