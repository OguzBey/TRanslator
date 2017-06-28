#! -*- coding: utf-8 -*-

import pyperclip
from googletrans import Translator
import sys
import sqlite3
from colorama import Fore,Style
from os import system
from time import sleep

reload(sys)
sys.setdefaultencoding("UTF-8")

__version__ = "1.1.1"
__author__ = "OguzBey"
__contact__ = "cfmelun@gmail.com" 

class Translater(object):

	def __init__(self):
		self.colors = {'red':Fore.RED,'green':Fore.GREEN,'cyan':Fore.CYAN,'yellow':Fore.LIGHTYELLOW_EX,'magenta':Fore.MAGENTA,'bold':Style.BRIGHT,'reset':Style.RESET_ALL}
		self.translator = Translator()
		self.select_languages = "tr"
		self.database = "dictionary.db"
		self.connection = sqlite3.connect(self.database)
		self.cursor = self.connection.cursor()
		self.columns = {'isim':'i_anlam','fiil':'f_anlam','zarf':'z_anlam','edat':'e_anlam','baglac':'b_anlam','sifat':'s_anlam','zamir':'zz_anlam'}
		self.names2 = {'isim':'isim','zarf':'zarf','bağlaç':'baglac','sıfat':'sifat','zamir':'zamir','fiil':'fiil','edat':'edat'}
	def clean_db(self):
		self.cursor.execute("drop table kelimeler")
		for key, value in self.columns.iteritems():
			try:
				self.cursor.execute("drop table %s" %key)
			except:
				pass
		self.cursor.execute('''CREATE TABLE kelimeler(id INTEGER PRIMARY KEY autoincrement,
			kelime text not null)''')
		for table,column in self.columns.iteritems():

			self.cursor.execute('''CREATE TABLE %s(id INTEGER NOT NULL,
				%s text not null,
				FOREIGN KEY(id) REFERENCES kelimeler(id))''' %(table,column))
		system('clear')
		print "Veritabanı temizlendi..."
		pass

	def flush(self):
		pyperclip.copy("")
		pass

	def notify(self, title, message):
		cmd = 'notify-send --app-name=TRanslater --urgency=low  "%s" "%s"'%(title, message)
		#--expire-time=10000
		system(cmd)

	def copy(self):
		self.c_word = pyperclip.paste()
		self.c_word = self.c_word.rstrip(" ")
		self.c_word = self.c_word.lstrip(" ")
		self.c_word = self.c_word.lower()
		if len(self.c_word) > 1 and len(self.c_word) < 20:
			if self.c_word.count(" ") < 2:
				return True
			else:
				return False
		else:
			return False
		pass

	def listener(self):
		self.flush()
		while True:
			sleep(0.2)
			if self.copy():
				self.run(self.c_word)
				self.flush()
			else:
				pass
		pass

	def offline_mod(self,word):
		for table, column in self.columns.iteritems():
			self.name = table
			self.column = column
			cek = self.cursor.execute("select %s from %s where id in(select id from kelimeler where kelime =?)" %(self.column,self.name),(word,))
			self.anlam = cek.fetchone()
			if self.anlam:
				if self.name in self.columns:
					self.notify(self.c_word + " -- " + self.name, self.anlam[0])
					print self.colors['yellow']+self.name+": "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
			else:
				pass
	
	def value_control(self,word):
		cek = self.cursor.execute("select count(*) from kelimeler where kelime=?",(word,))
		self.sayi = int(cek.fetchone()[0])
		if self.sayi == 0:
			# print "Bu kelime yok !"
			return self.sayi
		elif self.sayi == 1:
			# print "Bu kelime var !"
			return self.sayi
		else:
			print "Bu kelimeden çok fazla var"
			print self.sayi
			sys.exit()
	def join_mean(self,list):

		self.printable = ""
		for means in list:
			self.printable += means+", "
		return self.printable.rstrip(", ")

	def cevir(self,word):
		self.translated = self.translator._translate(word,self.select_languages)
		if self.translated[1]:
			self.cursor.execute("insert into kelimeler(kelime) values(?)",(word,))
			cek = self.cursor.execute("select id from kelimeler where kelime=?",(word,))
			self.id = str(cek.fetchone()[0])
			self.sayi = len(self.translated[1])
			for i in range(0,self.sayi):
				print "--"*20
				print self.colors['yellow']+self.translated[1][i][0]+": \n"+self.colors['reset']
				strr = str(self.translated[1][i][0])
				if strr in self.names2:
					table = self.names2[strr]
					column = self.columns[table]
					self.printable = self.join_mean(self.translated[1][i][1])
					self.notify(self.c_word + " -- " + self.translated[1][i][0], self.printable)
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into %s(id,%s) values(?,?)"%(table,column),(self.id,self.printable))

				else:
					print self.translated[1][i][0]
					sys.exit()

			self.connection.commit()
			print "\n\n"
			print self.colors['red']+self.colors['bold']+"[!]"+self.colors['reset']+self.colors['green']+self.colors['bold']+" Veritabanına eklendi.."+self.colors['reset']
		else:
			print "Çeviri yok"

	def run(self,word):
		system('clear')
		print ">> "+self.colors['cyan']+self.colors['bold']+word.upper()+self.colors['reset']+"\n"
		if self.value_control(word) == 0:
			self.cevir(word)
		else:
			# print "Offline mod başlıyor"
			self.offline_mod(word)
			print ""
try:		
	if len(sys.argv) == 2:
		if sys.argv[1] == "--clean":
			Translater().clean_db()
		else:
			pass
	else:
		Translater().listener()
except KeyboardInterrupt:
	pass
