__author__ = 'Darren Wong'
'stimulate the process of interact with input in Rem function of Scratch Basic'

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

class RemScreen(AbstractScreen):
	def __init__(self, **kwargs):
		super(RemScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 5)
		lbl = Label(text = "REM", size_hint = (.2, .5), valign = 'top', halign = 'center')
		lbl.bind(size=lbl.setter('text_size'))
		self.input = TextInput(hint_text = "Your comment", size_hint = (.8, .5), multiline = True)
		back_btn = Button(text = "BACK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.back_to_function_screen, self))

		ok_btn = Button(text = "OK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		ok_btn.bind(on_press = self.confirm_screen)
		
		guidance = Button(text='?',  background_color = (128, 0, 128, 1), size_hint = (.1, .1), pos_hint={'right':1})

		guidance.bind(on_press = partial(self.guide, 'rem'))

		self.popup = Popup(title="Error", content=Label(text="Please fill in all the fields!"), size_hint= (.4, .4))
		self.popup.dismiss()

		layout_1 = BoxLayout(orientation='horizontal')
		layout_1.add_widget(lbl)
		layout_1.add_widget(self.input)
		layout.add_widget(guidance)
		layout.add_widget(layout_1)
		layout.add_widget(back_btn)
		layout.add_widget(ok_btn)

		self.add_widget(layout)

	def previous_screen(self, *args):
		self.manager.current = 'function_screen'

	def confirm_screen(self, *args):
		if self.input.text.strip() != "":
			#global chosen_line, line_dictionary, label_dictionary
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "REM " + self.input.text
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (255, 255, 0, 1)
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 25
			self.input.select_all()
			self.manager.current = 'work_screen'
		else:
			self.popup.open()

	def parse_value(self):
		edited_data = AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()
		#print edited_data[1]
		self.input.text = edited_data[1]
