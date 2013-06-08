#!/usr/bin/python2

import os
import sys
import fcntl
import termios
import getpass
import subprocess
from gmusicapi import Webclient
from os.path import expanduser

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

def play(url):
	fnull = open('/dev/null', 'w')
	proc = subprocess.Popen(['mplayer', "%s" % url], stdin=subprocess.PIPE, stdout=fnull, stderr=fnull)
	return proc

def main():
  home = expanduser('~')
  configfile = open(home + '/.gmusicbarrc')

  for a in configfile:
    line = a.split(' ')
    if (line[0] == 'email'):
      email = line[1]
    else:
      email = raw_input("Email: ")

  password = getpass.getpass()
  
  api = Webclient()
  api.login(email, password)

  playlists = api.get_all_playlist_ids()
  for playlist in playlists['user']:
    print playlist

  while True:
    c = getch() 
    if (c == 'q'):
      api.logout() 
      break

  

if __name__ == '__main__':
	main()
