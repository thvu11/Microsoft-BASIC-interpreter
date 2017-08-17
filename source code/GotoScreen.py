__author__ = 'Darren Wong'
'stimulate the process of interact with input in Goto function of Scratch Basic'

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

class GotoScreen(AbstractScreen):
	#build the interface of Goto screen
	def __init__(self, **kwargs):
		super(GotoScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 5)
		lbl = Label(text = "GOTO", size_hint = (.2, .3), valign = 'top', halign = 'center')
		lbl.bind(size=lbl.setter('text_size'))
		self.input = TextInput(hint_text = "Next line program goes to", size_hint = (.8, .3))
		back_btn = Button(text = "BACK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.back_to_function_screen, self))

		ok_btn = Button(text = "OK", size_hint = (.2, .2), background_color=(0, 0, 255, .3))
		ok_btn.bind(on_press = self.confirm_screen)

		guidance = Button(text='?',background_color = (128, 0, 128, 1), size_hint = (.1, .1), pos_hint={'right':1})

		guidance.bind(on_press = partial(self.guide, 'goto'))

		touch_mode_btn = Button(text = "touch mode", size_hint=(.2, .2), background_color=(0, 0, 255, .3))
		touch_mode_btn.bind(on_press = self.touch_mode_activate)
		self.popup1 = Popup(title="Notice", content=Label(text="Press the line to specify the destination"), size_hint= (.4, .4))
		self.popup1.dismiss()
		self.popup2 = Popup(title="Error", content=Label(text="Please enter a valid input!"), size_hint= (.4, .4))
		self.popup2.dismiss()
		layout_1 = BoxLayout(orientation='horizontal')
		layout_1.add_widget(lbl)
		layout_1.add_widget(self.input)

		layout.add_widget(guidance)
		layout.add_widget(touch_mode_btn)
		layout.add_widget(layout_1)
		layout.add_widget(back_btn)
		layout.add_widget(ok_btn)

		self.add_widget(layout)

	def touch_mode_activate(self, *args):
		#lead user back to work space section and specify next instruction to finish the touch experience 
		self.popup1.open()
		self.manager.current = 'work_screen'
		AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "CURRENT WORKING LINE"
		AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (255, 255, 0, 1)
		AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 25
		AbstractScreen.touch_mode = True


	def confirm_screen(self, *args):
		#check if text input is not empty and modify the text of specific line
		if len(self.input.text.split()) == 1:
			#change text and color of associated line number
			AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text = "GOTO " + self.input.text
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].color = (255, 255, 0, 1)
			AbstractScreen.label_dictionary[AbstractScreen.chosen_line].font_size = 25
			self.input.select_all()
			self.manager.current = 'work_screen'
		else:
			self.popup2.open()

	def parse_value(self):
		#use for retrieve current data for edit function
		edited_data = AbstractScreen.line_dictionary[AbstractScreen.chosen_line].text.split()
		#print edited_data[1]
		self.input.text = edited_data[1]


		
