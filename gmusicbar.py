import getpass
import pygst
pygst.require("0.10")
import gst
from gmusicapi import Webclient

email = raw_input("Email: ")
password = getpass.getpass()

api = Webclient()
api.login(email, password)
# => True

firstsong = api.get_all_songs()[0]['id']
print firstsong

url = api.get_stream_url(firstsong)

player = gst.element_factory_make("playbin2", "player")
player.set_property('uri', url)
player.set_state(gst.STATE_PLAYING)
print url
