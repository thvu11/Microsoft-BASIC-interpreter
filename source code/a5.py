__author__ = 'Darren Wong'
'main method for the Scratch basic application, run this script to execute the program'

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from WorkSpaceScreen import WorkSpaceScreen
from AboutUsScreen import AboutUsScreen
from IfScreen import IfScreen
from RemScreen import RemScreen
from GotoScreen import GotoScreen
from PrintScreen import PrintScreen
from LetScreen import LetScreen
from LoadScreen import LoadScreen
from WelcomeScreen import WelcomeScreen
from SaveScreen import SaveScreen
from FunctionScreen import FunctionScreen
import os

class App(App):
	def build(self):
		if not os.path.exists(os.getcwd() + '/saved_scratch_data'):
			os.makedirs(os.getcwd() + '/saved_scratch_data')
		screen_manager = ScreenManager()
		#create seperated screens for each function and the interface displaying all the work
		work_screen = WorkSpaceScreen(name='work_screen')
		about_screen = AboutUsScreen(name='about_screen')
		
		function_screen = FunctionScreen(name='function_screen')
		if_screen = IfScreen(name='if_screen')
		rem_screen = RemScreen(name='rem_screen')
		goto_screen = GotoScreen(name='goto_screen')
		print_screen = PrintScreen(name='print_screen')
		let_screen = LetScreen(name='let_screen')
		load_screen = LoadScreen(name='load_screen')
		
		welcome_screen = WelcomeScreen(name='welcome_screen')
		save_screen = SaveScreen(name='save_screen')
		
		
		screen_manager.add_widget(welcome_screen)
		
		screen_manager.add_widget(load_screen)
		screen_manager.add_widget(save_screen)
		
		screen_manager.add_widget(about_screen)
		
		screen_manager.add_widget(work_screen)
		screen_manager.add_widget(function_screen)
		screen_manager.add_widget(if_screen)
		screen_manager.add_widget(rem_screen)
		screen_manager.add_widget(goto_screen)
		screen_manager.add_widget(print_screen)
		screen_manager.add_widget(let_screen)
		
		return screen_manager
	

if __name__ == '__main__':
	App().run()
