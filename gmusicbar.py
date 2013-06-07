import getpass
import subprocess
from gmusicapi import Webclient

def play(url):
	fnull = open('/dev/null', 'w')
	proc = subprocess.Popen(['mplayer', "%s" % url], stdin=subprocess.PIPE, stdout=fnull, stderr=fnull)
	return proc

def main():
	email = raw_input("Email: ")
	password = getpass.getpass()

	api = Webclient()
	api.login(email, password)

	firstsong = api.get_all_songs()[0]['id']
	print firstsong

	url = api.get_stream_url(firstsong)
	print url

	cursong = play(url)

if __name__ == '__main__':
	main()