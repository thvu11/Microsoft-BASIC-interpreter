__author__ = 'Huy Vu'
'display all the files that are saved, support user to load specific file to continue working'

import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from AbstractScreen import AbstractScreen
from functools import partial
import os

class LoadScreen(AbstractScreen):
	#build the interface for Load Screen
	def __init__(self, **kwargs):
		#add scroll view for the meta data, testing more situations about save and load
		super(LoadScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation='vertical', padding = 10)
		
		label = Label(text='Available file\n', halign = 'left', valign= 'top', size_hint_y = None, markup=True)
		label.font_size = '20sp'
		label.height = 3000
		label.bind(size=label.setter('text_size'))
		self.refresh(label)

		load_btn = Button(text = "LOAD", size_hint = (.2, .4), background_color=(0, 0, 255, .3))
		load_btn.bind(on_press = partial(self.load_confirm, 0))

		back_btn = Button(text = "BACK", size_hint = (.2, .4), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.load_confirm, 1))
		
		refresh_btn = Button(text = "REFRESH", size_hint = (.2, .4), background_color=(0, 0, 255, .3))
		refresh_btn.bind(on_press=partial(self.refresh, label))

		self.popup = Popup(title="Error", content=Label(text=""), size_hint= (.4, .4))
		self.popup.dismiss()
		layout_input = BoxLayout(orientation='horizontal')
		lbl_input = Label(text = "[size=20]Chosen file[/size]", markup=True, size_hint = (.2, .3))
		self.input_1 = TextInput(text = "", size_hint= (.8, .4), multiline = False)
		layout_input.add_widget(lbl_input)
		layout_input.add_widget(self.input_1)

		scroll = ScrollView(size_hint=(1, 2))
		scroll.add_widget(label)

		layout.add_widget(scroll)
		layout.add_widget(layout_input)
		layout.add_widget(load_btn)
		layout.add_widget(refresh_btn)
		layout.add_widget(back_btn)
		self.add_widget(layout)

	def refresh(self, label, *args):
		#update the interface in case user just saves a new file
		label.text = ""
		current_dir = str(os.getcwd()) + '/saved_scratch_data'
		for item in os.listdir(current_dir):
			i = os.path.splitext(item)[0]
			if not str(i).endswith("_detail"):
				#display the name of the saved file
				label.text += 'File name:' + '[color=#00ffff]' + item + '[/color]'+ '\n'
				#read its associated meta data file and display the content
				file = open(current_dir + '/' + str(i) + '_detail.txt', 'r')
				for line in file:
					label.text += line + '\n'
				file.close()
				
				label.text += '\n\n'

	def load_confirm(self, option, *args):
		#screen navigation and load the content of chosen file into work space
		if option == 1:
			self.manager.current = 'welcome_screen'
		else:
			
			#reset the line dictionary and label dictionary 
			for item in AbstractScreen.line_dictionary.values():
				item.text = ''
			for item in AbstractScreen.label_dictionary.values():
				item.color = (1, 1, 1, 1)
				item.font_size = 15
			load_file = str(os.getcwd()) + '/saved_scratch_data/' + self.input_1.text
			#open chosen file or display popup noticing invalid file name
			try:
				file = open(load_file, 'r')
			except IOError:
				self.popup.content.text = 'File does not exist'
				self.popup.open()
				return
			#insert new content based on line number in loading file
			#highlight associated line number
			for line in file:
				AbstractScreen.line_dictionary[line[0]].text = line[2:].strip('\n')
				AbstractScreen.label_dictionary[line[0]].color = (255, 255, 0, 1)
				AbstractScreen.label_dictionary[line[0]].font_size = 25
			
			file.close()
			self.manager.current = 'work_screen'
