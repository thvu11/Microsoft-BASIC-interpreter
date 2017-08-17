__author__ = 'Huy Vu'
'Parent class for every screen object in the application, share the data structure across all children class'

import kivy
kivy.require('1.7.2')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class AbstractScreen(Screen):
	#class method for sharing purpose across all child class
	line_dictionary = {}
	label_dictionary = {}
	#use for touch mode experience in Goto function
	touch_mode = False
	chosen_line = '0'

	def __init__(self, **kwargs):
		#sharing popup for guidance of all other screen
		super(AbstractScreen, self).__init__(**kwargs)
		self.pop = Popup(title='Guidance', content=Label(text=""), size_hint=(.6, .6))
		self.pop.dismiss()
		
		

	def guide(self, keyword, *args):
		#edit the content of the popup based on given keyword
		dictionary = {'let': "Format: LET <variable> = <expression>\n<expression> = <value><operator><value>\n<value> can be a variable name or a numerical constant\n<operator> can be choose below\nUsage: assign a value to a variable", 
	'print': "Format: PRINT <value>\n<value> can be a variable name or a numerical value\nUsage: print the value to the text console", 
	'if':"Format: IF <expression> GOTO <value>\n<expression> = <value><operator><value>\n<value> can be a variable name or a numerical constant\n<operator> can be choose below\nUsage: make choice between the IF and GOTO statement", 
	'rem': "Format: REM <comment string>\nUsage: comment on yout code", 
	'goto': "Format: GOTO <value>\n<value> can be a variable name or a numerical value\nUsage: goto the chosen line"}
		self.pop.content.text = dictionary[keyword]
		self.pop.open()

	def back_to_function_screen(self, obj, *args):
		#navigation back to previous screen for most of the functions
		obj.manager.current = 'function_screen'
