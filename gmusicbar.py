#!/usr/bin/python2

import os
import sys
import fcntl
import termios
import getpass
import subprocess
from gmusicapi import Webclient
from os.path import expanduser

# get rid of this... somehow
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

def login(api):
  configfile = open(expanduser('~/.gmusicbarrc'))
  if configfile:
    for a in configfile:
      line = a.split(' ')
      if (line[0] == 'email'):
        email = line[1]

  if not email:
    email = raw_input("Email: ")

  password = getpass.getpass()
  api.login(email, password)

def index_playlists(playlists):
  indexed = []
  for playlist in playlists:
    indexed.append(playlist)
  return indexed

def choose_playlist(api, indexed, playlists):
  print "Choose a playlist:"
  i = 0;
  for playlist in indexed:
    print str(i) + ": " + playlist
    i += 1;
  while 1:
    c = getch()
    d = int(c)
    if d >= 0 and d < i:
      break
  return playlists[indexed[d]]

def play(url):
	fnull = open('/dev/null', 'w')
	proc = subprocess.Popen(['mplayer', "%s" % url], stdin=subprocess.PIPE, stdout=fnull, stderr=fnull)
	return proc

def main():
  api = Webclient()
  login(api)
  playlists = api.get_all_playlist_ids().pop('user')
  indexed_playlist_names = index_playlists(playlists)
  curlist = choose_playlist(api, indexed_playlist_names, playlists)[0]
  songs = api.get_playlist_songs(curlist)
  print songs

  curpos = 0;
  cursongid = songs[curpos]['id']
  cursongurl = api.get_stream_url(cursongid)
  print cursongurl
  #cursong = play(cursongurl)

  while 1:
    if cursong.poll() is not None:
      curpos += 1
      cursongid = songs[curpos]['id']
      cursong = play(get_stream_url(cursongid))
    c = getch() 
    if (c == 'q'):
      api.logout() 
      break

if __name__ == '__main__':
	main()
