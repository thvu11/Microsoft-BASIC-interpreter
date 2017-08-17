__author__ = 'Darren Wong'
'the first screen that user will see when initiating the application'

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
from functools import partial

class WelcomeScreen(AbstractScreen):
	#build the interface for Welcome Screen
	def __init__(self, **kwargs):
		super(WelcomeScreen, self).__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical')
		label = Label(text='[size=70]SCRATCH BASIC[/size]', markup= True, size_hint_y = .5)
		btn = Button(text='>>>', size_hint = (.2, .1), pos_hint={'right':.6})
		btn.bind(on_press = partial(self.change_screen, 1))
		load_btn = Button(text='[size=20]Load[/size]', markup=True, size_hint = (.2, .1), pos_hint={'right':.6})
		load_btn.bind(on_press = partial(self.change_screen, 3))
		abt_btn = Button(text='[size=20]About us[/size]', markup=True, size_hint = (.2, .1), pos_hint={'right':.6})
		abt_btn.bind(on_press=partial(self.change_screen, 2))
		layout.add_widget(label)
		layout.add_widget(btn)
		layout.add_widget(load_btn)
		layout.add_widget(abt_btn)
		layout.add_widget(Label(text="", size_hint_y = .3))
		self.add_widget(layout)

	def change_screen(self, choice, *args):
		#navigation to specific screen based on user choice
		if choice == 1:
			self.manager.current = 'work_screen'
		elif choice == 2:
			self.manager.current = 'about_screen'
		else:
			self.manager.current = 'load_screen'

