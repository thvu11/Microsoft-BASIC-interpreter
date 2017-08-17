__author__ = 'Darren Wong'
'stimulate the screen describing the overall information of the application'

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import escape_markup

from AbstractScreen import AbstractScreen

class AboutUsScreen(AbstractScreen):
	#build the interface for About us Screen
	def __init__(self, **kwargs):
		super(AboutUsScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical')
		label = Label(text='[size=25]Author[/size]\nHuy Vu & Darren Wong\n\n[size=25]Email[/size]\nthvu11'+ escape_markup('@') + 'student.monash.edu.au\ndwwon6' + escape_markup('@') + 'student.monash.edu.au\n\n[size=25]Description[/size]\nScratch Basic is an intepreter of basic programming language\nwith an aim to introduce beginner to programming world', markup=True)
		btn = Button(text='BACK', size_hint = (.2, .1), pos_hint={'right':.6})
		btn.bind(on_press=self.change_screen)
		layout.add_widget(label)
		layout.add_widget(btn)
		layout.add_widget(Label(text="", size_hint_y = .3))
		self.add_widget(layout)

	def change_screen(self, *args):
		#navigation back to welcome screen
		self.manager.current = 'welcome_screen'
