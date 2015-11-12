import os, sys
import subprocess
import re

try:
	from neovim import socket_session, Nvim, attach
	import argparse
except ImportError:
	# no neovim installed on host machine.
	pass

def call_neovim(editor, editor_flags, files):
	"""Call neovim with a desired number of flags and files.

	This is done in a separate function as neovim has a VERY different way of doing things.

	If a running Vim server is found in the current Tmux window, then the files are opened there. Otherwise, a new Vim server instance is created in the pane where the call to this program was made.

	Args:
		editor (str): The editor command that should be called.
		editor_flags (str): A list of strings containing extra flags that should be called alongside the editor of choice.
		files (str): A list of strings containing the files that should be opened.
	"""
	print "TODO: call neovim"
	
	"""
	parser = argparse.ArgumentParser(description="Neovim client")
	# TODO: arguments with particular tmux windows
	parser.add_argument('--addr', default='tmp/nvim.sock', help="Neovim listen address")
	parser.add_argument('file', help="file")
	parser.add_argument('line', type=int, help="line")
	args = parser.parse_args()
	
	session = socket_session(args.addr)
	nvim = Nvim.from_session(session)

	nvim.command("e {}".format(args.file))
	nvim.current.window.cursor = (args.line, 0)
	"""

	# TODO: find if there's any currently running neovim instances
	# TODO: find current running nvim instance, and send commands to that instead
	# TODO: if no neovim instances, make a new juan
	nvim = attach('socket', path='/tmp/nvim')
	nvim.command('cd ' + os.path.abspath(os.curdir))
	print os.path.abspath(os.curdir)

	# TODO: is there a better way of doing this?
	for file in files:
		nvim.command('e ' + file)


def call_vim(editor, editor_flags, files):
	"""Call vim (or a variant thereof) with a desired number of flags and files.

	If a running Vim server is found in the current Tmux window, then the files are opened there. Otherwise, a new Vim server instance is created in the pane where the call to this program was made.

	Args:
		editor (str): The editor command that should be called.
		editor_flags (str): A list of strings containing extra flags that should be called alongside the editor of choice.
		files (str): A list of strings containing the files that should be opened.
	"""

	# get the current tmux window in which this command was run
	tmux_current_window = subprocess.check_output(["tmux", "display-message", "-p", "#{window_id}"]).rstrip()

	vim_server_list = str.split(subprocess.check_output([editor] + editor_flags + ['--serverlist']).rstrip())

	for name in vim_server_list:
		if name == tmux_current_window:
			subprocess.call([editor] + editor_flags + ["--servername", name, "--remote"] + files)
			sys.exit(0)

	# if we hit this point, we didn't find a server.
	# So just create a new Vim server with the required arguments
	subprocess.call([editor] + editor_flags + ["--servername", tmux_current_window, "--remote-silent"] + files)

def main():
	# work out the editor.

	# if the OMNIVIM_EDITOR environment variable is set, use it.
	# otherwise, if the EDITOR variable is set, use that instead.
	# otherwise, use vim.
	EDITOR = 'vim'
	if os.environ.get('OMNIVIM_EDITOR') is not None:
		EDITOR = os.environ.get('OMNIVIM_EDITOR')
	elif os.environ.get('EDITOR') is not None:
		EDITOR = os.environ.get('EDITOR')
	
	# similar for editor flags. If OMNIVIM_EDITOR_FLAGS is set, use that.
	# otherwise, use nothing.
	EDITOR_FLAGS = []
	if os.environ.get('OMNIVIM_EDITOR_FLAGS') is not None:
		EDITOR_FLAGS = str.split(os.environ.get('OMNIVIM_EDITOR_FLAGS').rstrip(), ' ')
		

	# read files from command line arguments
	# we remove the first, since this will always be omnivim.py
	files = sys.argv
	files.pop(0)
	
	# checking the TMUX environment variable will confirm whether or not tmux is currently running.
	in_tmux = os.environ.get('TMUX')

	if in_tmux is not None:
		# if tmux is running, then we have different things to do if using neovim or g/vim
		# use regex to work it out
		is_neovim = re.search('n(eo)?vim', EDITOR)
		is_vim = re.search('g?vim', EDITOR)

		if is_neovim is not None:
			call_neovim(EDITOR, EDITOR_FLAGS, files)
		elif is_vim is not None:
			call_vim(EDITOR, EDITOR_FLAGS, files)
	else:
		# otherwise, just call the editor and flags with the requisite files, no strings (or servers) attached.
		subprocess.call([editor] + editor_flags + files)

main()
