import sys
from app_controller import app

try:
	port = sys.argv[1]
	port = int(port)
	if __name__ == "__main__":
		print "server at port ",port
		app.run(host = 'localhost',port = port)
except:
	if __name__ == "__main__":
		print ("server at port 8000")
		app.run(host = 'localhost',port = 8000)
