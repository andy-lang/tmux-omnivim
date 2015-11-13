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
	"""Call Neovim with a desired number of flags and files.

	This is done in a separate function as neovim has a VERY different way of doing things.

	If a running Vim server is found in the current Tmux window, then the files are opened there. Otherwise, a new Vim server instance is created in the pane where the call to this program was made.

	Args:
		editor (str): The editor command that should be called.
		editor_flags (str): A list of strings containing extra flags that should be called alongside the editor of choice.
		files (str): A list of strings containing the files that should be opened.
	"""

	# all running Neovim instances associated with this script follow the format "/tmp/nvim-@n", where n is the number of the associated tmux window.
	socketpath='/tmp/nvim-' + subprocess.check_output(["tmux", "display-message", "-p", "#{window_id}"]).rstrip() + '.omni'

	# if there is already a Neovim session associated with this window, send the commands to it.
	if os.path.exists(socketpath):
		# socket already associated with this window.
		# so just attach to it and send the commands
		nvim = attach('socket', path=socketpath)
		for file in files:
			nvim.command('e ' + os.path.join(os.path.abspath(os.curdir), file))
	else:
		command = ' '.join(["NVIM_LISTEN_ADDRESS=" + socketpath, editor] + editor_flags + files)

		# TODO see if this can be done with the subprocess module instead.
		# os.system is moving towards deprecation, but a few tests with subprocess.call() weren't successful.
		# I think it's because of that "NVIM_LISTEN_ADDRESS" at the beginning...subprocess doesn't like that.
		os.system(command)


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
	lit_flag = files.count("--lit")

	if in_tmux is not None and lit_flag == 0:
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
		while files.count("--lit") > 0:
			# if lit_flag was passed in, we need to remove it from the list of files before calling
			# TODO: this is pretty damn hacky.
			files.pop(files.index("--lit"))
			
		subprocess.call([EDITOR] + EDITOR_FLAGS + files)

main()
