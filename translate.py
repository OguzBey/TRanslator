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

__version__ = "1.0.0"
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
		self.columns = ['i_anlam','f_anlam','z_anlam','e_anlam','b_anlam','s_anlam','zz_anlam']
		self.names = ['isim','fiil','zarf','edat','baglac','sifat','zamir']
	def clean_db(self):
		self.cursor.execute("drop table kelimeler")
		for i in self.names:
			try:
				self.cursor.execute("drop table %s" %i)
			except:
				pass
		self.cursor.execute('''CREATE TABLE kelimeler(id INTEGER PRIMARY KEY autoincrement,
			kelime text not null)''')
		self.cursor.execute('''CREATE TABLE isim(id INTEGER NOT NULL,
			i_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE sifat(id INTEGER NOT NULL,
			s_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE zarf(id INTEGER NOT NULL,
			z_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE edat(id INTEGER NOT NULL,
			e_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE fiil(id INTEGER NOT NULL,
			f_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE baglac(id INTEGER NOT NULL,
			b_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		self.cursor.execute('''CREATE TABLE zamir(id INTEGER NOT NULL,
			zz_anlam text not null,
			FOREIGN KEY(id) REFERENCES kelimeler(id))''')
		system('clear')
		print "Veritabanı temizlendi..."
		pass

	def flush(self):
		pyperclip.copy("")
		pass
	def copy(self):
		self.c_word = pyperclip.paste()
		self.c_word = self.c_word.rstrip(" ")
		self.c_word = self.c_word.lstrip(" ")
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
		for i in range(0,6):
			self.name = self.names[i]
			self.column = self.columns[i]
			cek = self.cursor.execute("select %s from %s where id in(select id from kelimeler where kelime =?)" %(self.column,self.name),(word,))
			self.anlam = cek.fetchone()
			if self.anlam:
				if self.name == "isim":
					print self.colors['yellow']+"İsim: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				elif self.name == "fiil":
					print self.colors['yellow']+"Fiil: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				elif self.name == "zarf":
					print self.colors['yellow']+"Zarf: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				elif self.name == "edat":
					print self.colors['yellow']+"Edat: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				elif self.name == "baglac":
					print self.colors['yellow']+"Bağlaç: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				elif self.name == "sifat":
					print self.colors['yellow']+"Sıfat: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
				else:
					print self.colors['yellow']+"Zamir: "+self.colors['reset']+self.colors['magenta']+self.colors['bold']+self.anlam[0]+self.colors['reset']
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
				if self.translated[1][i][0] == "isim":
					#isim
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into isim(id,i_anlam) values(?,?)",(self.id,self.printable))

				elif self.translated[1][i][0] == "fiil":
					#fiil 
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into fiil(id,f_anlam) values(?,?)",(self.id,self.printable))
					
				elif self.translated[1][i][0] == "bağlaç":
					#baglac
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into baglac(id,b_anlam) values(?,?)",(self.id,self.printable))
					
				elif self.translated[1][i][0] == "edat":
					#edat 
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into edat(id,e_anlam) values(?,?)",(self.id,self.printable))

				elif self.translated[1][i][0] == "sıfat":
					#sifat
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into sifat(id,s_anlam) values(?,?)",(self.id,self.printable))

				elif self.translated[1][i][0] == "zarf":
					#zarf
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into zarf(id,z_anlam) values(?,?)",(self.id,self.printable))
				elif self.translated[1][i][0] == "zamir":
					self.printable = self.join_mean(self.translated[1][i][1])
					print self.colors['red']+self.colors['bold']+self.printable+self.colors['reset']
					self.cursor.execute("insert into zamir(id,zz_anlam) values(?,?)",(self.id,self.printable))

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
		
if len(sys.argv) == 3:
	if sys.argv[2] == "--clean":
		Translater().clean_db()
	else:
		pass
else:
	Translater().listener()