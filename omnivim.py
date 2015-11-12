import os, sys
import subprocess

# check that the editor is set to vim or something similar
# TODO: get this working with Neovim, Gvim, etc.
# EDITOR = os.environ.get('EDITOR', 'vim') if os.environ.get('EDITOR') else 'vim'
EDITOR = "gvim"
EDITOR_FLAGS = "-v"
DEBUG = False

# check that tmux is currently running. This will be None if no tmux environment variable has been set
IN_TMUX = os.environ.get('TMUX')

# TODO: read this from command line arguments
files = ["omnivim.py", "omnivim.sh"]


if IN_TMUX is not None:
	# get the current tmux window in which this command was run
	tmux_current_window = subprocess.check_output(["tmux", "display-message", "-p", "#{window_id}"]).rstrip()
	if DEBUG:
		print "current window: |" + tmux_current_window + "|"

	vim_server_list = str.split(subprocess.check_output([EDITOR, '--serverlist']).rstrip())
	if DEBUG:
		print "vim servers:", vim_server_list

	for name in vim_server_list:
		if DEBUG:
			print "name: " + name
		if name == tmux_current_window:
			subprocess.call([EDITOR, EDITOR_FLAGS, "--servername", name, "--remote"] + files)
			sys.exit(0)

	# if we hit this point, we didn't find a server.
	# So just create a new Vim server with the required arguments
	subprocess.call([EDITOR, EDITOR_FLAGS, "--servername", tmux_current_window, "--remote-silent"] + files)

else:
	# otherwise we're not in tmux.
	# So just launch vim, business as usual, with no added server shenanigans
	subprocess.call([EDITOR, EDITOR_FLAGS] + files)
