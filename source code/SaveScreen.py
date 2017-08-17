__author__ = 'Huy Vu'
'support users to save the program'

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
import os
from insertion_sort import insertion_sort

class SaveScreen(AbstractScreen):
	'''build the interface for the screen'''
	def __init__(self, **kwargs):
		super(SaveScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation='vertical')

		lbl_0 = Label(text = "Saved name", size_hint = (.2, .5))
		self.input_0 = TextInput(size_hint= (.8, .5), multiline = False)

		lbl_1 = Label(text = "Author name", size_hint = (.2, .5))
		self.input_1 = TextInput(text = "", size_hint= (.8, .5), multiline = False)

		lbl_2 = Label(text = "Brief description", size_hint = (.2, .5))
		self.input_2 = TextInput(text = "", size_hint= (.8, .5), multiline = False)

		lbl_3 = Label(text = "Email", size_hint = (.2, .5))
		self.input_3 = TextInput(text = "", size_hint= (.8, .5), multiline = False)

		back_btn = Button(text = "BACK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		back_btn.bind(on_press = partial(self.save_confirm, 0))

		save_btn = Button(text = "OK", size_hint = (.2, .5), background_color=(0, 0, 255, .3))
		save_btn.bind(on_press = partial(self.save_confirm, 1))

		layout_title = BoxLayout(orientation='horizontal')
		layout_title.add_widget(lbl_0)
		layout_title.add_widget(self.input_0)

		layout_author = BoxLayout(orientation='horizontal')
		layout_author.add_widget(lbl_1)
		layout_author.add_widget(self.input_1)

		layout_des = BoxLayout(orientation='horizontal')
		layout_des.add_widget(lbl_2)
		layout_des.add_widget(self.input_2)

		layout_em = BoxLayout(orientation='horizontal')
		layout_em.add_widget(lbl_3)
		layout_em.add_widget(self.input_3)
		
		layout.add_widget(layout_title)
		layout.add_widget(layout_author)
		layout.add_widget(layout_des)
		layout.add_widget(layout_em)
		layout.add_widget(save_btn)
		layout.add_widget(back_btn)

		self.add_widget(layout)

	def save_confirm(self, option, *args):
		'''navigation between screen
		   save the current work in specific directory
		'''
		if option == 0:
			self.manager.current = 'work_screen'
		else:
			#check if user doesn't specify the saved name for the work
			if len(self.input_0.text.split()) == 0:
				popup = Popup(title="Error", content=Label(text="Please enter a valid input!"), size_hint= (.4, .4))
				popup.open()
			else:
				#specify the directory to save the work
				path = str(os.getcwd()) + '/saved_scratch_data/'
				file = open(path + self.input_0.text + ".txt", 'w')
				tmp_list = []
				#add all the non-empty  item from dictionary to a temporary list
				for value in AbstractScreen.line_dictionary.keys():
					if AbstractScreen.line_dictionary[value].text != "":
						tmp_list.append(int(value))
				#sort temporary list by line number
				insertion_sort(tmp_list)
				for key in tmp_list:
					file.write(str(key) + " " + AbstractScreen.line_dictionary[str(key)].text + '\n')
				file.close()
				#save the meta data in a second text file with same name as the name that customer choses cascading with _detail
				file = open(path + self.input_0.text + "_detail.txt", 'w')
				file.write("Author name: " + self.input_1.text + '\n')
				file.write("Description: " + self.input_2.text + '\n')
				file.write("Email: " + self.input_3.text + '\n')
				file.close()
				self.manager.current = 'welcome_screen'
