import pymongo
import datetime
import sys
from pymongo import MongoClient
from elasticsearch import Elasticsearch

class Logrepo:
	#public var
	typerepo = ""
	filename = ""
	typedb = ""

	#init arga
   	def __init__(self, arga):
   		if(self.isAttrComplete(arga)):
   			self.assignAttr(arga)
   		else:
   			sys.exit("missing argument")
   			
   	
   	def isAttrComplete(self, arga):
   		if(len(arga)<=3):
   			return 0
   		else:
   			return 1

   	def assignAttr(self, arga):
   		self.typerepo = arga[1]
		self.filename = arga[2]
		self.typedb = arga[3]

   	def process(self):
   		if(self.typerepo == "svn"):
   			print "processing export from svn log"
   			logdata = self.getLogFromSvn()
   		elif(self.typerepo == "git"):
   			print "processing export from git log"
   			logdata = self.getLogFromGit()
   		else:
   			print "false type repo"

   	def getLogFromSvn(self):
   		#assign object log
   		log = Logdata()

   		#parsing file
   		f = open(arg[2],'r')
		for line in f.read().split('------------------------------------------------------------------------'):
			perline = line.split('\n')			
			if(len(perline) > 2):
				p = perline[1].split(" | ")
				q = p[2].split(" ")
				refa = p[0]
				
				log.types = "svn"
				log.revision = refa[1:]
				log.author = p[1]
				log.date = q[0]+"T"+q[1]
				log.time = q[1]
				message = "asdasd"
				a = 0
				for lm in perline:
					if(a>2):
						message = message+lm+" "
					a = a+1
				log.message = message
				log.saveData(self.typedb)
				#log.printData()

		f.close()

	def getLogFromGit(self):
   		#assign object log
   		log = Logdata()

   		#parsing file
   		f = open(arg[2],'r')
		for line in f.read().split('\ncommit '):
			perline = line.split('\n')
			if(len(perline) > 2):

				log.types = "git"
				if(perline[0].split(" ")[0]=='commit'):
		   			log.revision = perline[0].split(" ")[1]
		   		else:
		   			log.revision = perline[0]

		   		log.author = perline[1][8:]
		   		date = perline[2][8:]
		   		log.time = date.split(' ')[3]

		   		message = ""
		   		a = 0
				for lm in perline:
					if(a>3):
						message = message+lm+" "
					a = a+1
				log.message = message

		   		datenew = datetime.datetime.strptime(date,'%a %b %d %H:%M:%S %Y +0700')
				log.date = datenew

				log.saveData(self.typedb)
				#log.printData()

		f.close()

class Logdata:
	#mongo db set up 
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client['log-repo']
	collection = db['log-svn']

	#elasticsearch set up
	es = Elasticsearch()

	#public var
	types = ""
	revision = ""
	author = ""
	date = ""
	time = ""
	message = ""
	date_post = datetime.datetime.utcnow()

	def setAllAttr(self, typ, rev, aut, dat, tim, mess):
		self.types = typ
		self.revision = rev
		self.author = aut
		self.date = dat
		self.time = tim
		self.message = mess

	def saveData(self, dbtype):
		data = {
				"type" : self.types,
				"revision": self.revision,
				"author": self.author,
				"date": self.date,
				"time": self.time,
				"message": self.message,
				"date_post": self.date_post}

		self.saveToDb(data, dbtype, self.types)

	def printData(self):
		print self.types,
		print self.revision,
		print self.author,
		print self.date,
		print self.time,
		print self.message,
		print self.date_post

	def saveToDb(self, data, dbtype, typerepo):
		# change this to change collection
		if(dbtype == "mongo"):
			if(typerepo == "git"):
				posts = self.db.git
			elif(typerepo == "svn"):
				posts = self.db.svn
			else:
				posts = self.db.logrepository

			post_id = posts.insert(data)

		# change this to change index and type
		elif(dbtype == "elastic" or dbtype == "elasticsearch"):
			res = self.es.index(index="log-repo", doc_type=typerepo, body=data)
		else:
			print "failed to save chek elastic or mongo"


#application
arg = sys.argv
l = Logrepo(arg)
l.process()

