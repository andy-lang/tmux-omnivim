import os, os.path, sys
import subprocess
import re

try:
    from neovim import socket_session, Nvim, attach
    import argparse
except ImportError:
    # no neovim installed on host machine.
    pass

def tmux_send_keys(command):
    """ Call a command as a call to `tmux send-keys`.

    Args:
        command (str): The command that should be called, as a single string.
    """
    subprocess.call(['tmux', 'send-keys', '-l', ' '.join(command), '\r'])

def call_neovim(editor, editor_flags, files, nvim_socket_path='/tmp'):
    """Call Neovim with a desired number of flags and files.

    This is done in a separate function as neovim has a VERY different way of doing things.

    If a running Neovim server associated with the current Tmux window is found, then the files are opened there.
    Otherwise, a new Neovim instance is created in the pane where the call to this program was made, with the name in a format that this script knows to recognise.

    Args:
        editor (str): The editor command that should be called.
        editor_flags (str): A list of strings containing extra flags that should be called alongside the editor of choice.
        files (str): A list of strings containing the files that should be opened.
        nvim_socket_path (str): The path where socket files should be stored.
"""

    # all running Neovim instances associated with this script follow the format "/tmp/nvim-@n.omni", where n is the number of the associated tmux window.
    tmux_current_window = subprocess.check_output(["tmux", "display-message", "-p", "#{window_id}"]).rstrip()
    socket_path = os.path.join(nvim_socket_path, ''.join(['.nvim-', tmux_current_window.strip().decode('utf-8'), '.omni']))

    if os.path.exists(socket_path):
        # socket already associated with this window.
        # so just attach to it and send the commands
        nvim = attach('socket', path=socket_path)
        for file in files:
            nvim.command('e ' + os.path.join(os.path.abspath(os.curdir), file))
    else:
        # no associated socket. So we create a new Neovim instance following the format specified above.
        command = ['NVIM_LISTEN_ADDRESS=' + socket_path, editor] + editor_flags + files

        # the call needs to be run through tmux_send_keys so that tmux recognises that Vim is currently running. This allows vim-tmux-navigator to not break.
        tmux_send_keys(command)


def call_vim(editor, editor_flags, files):
    """Call vim (or a variant thereof) with a desired number of flags and files.

    If a running Vim server associated with the current Tmux window is found, then the files are opened there.
    Otherwise, a new Vim instance is created in the pane where the call to this program was made, with the name in a format that this script knows to recognise.

    Args:
        editor (str): The editor command that should be called.
        editor_flags (str): A list of strings containing extra flags that should be called alongside the editor of choice.
        files (str): A list of strings containing the files that should be opened.
"""

    # get the current tmux window in which this command was run
    tmux_current_window = subprocess.check_output(["tmux", "display-message", "-p", "#{window_id}"]).rstrip()
    # and get a list of servers, as a string split by spaces
    vim_server_list = str.split(subprocess.check_output([editor] + editor_flags + ['--serverlist']).rstrip())

    try:
        # if we find a running server, send the commands there
        i = vim_server_list.index(name)
        subprocess.call([editor] + editor_flags + ["--servername", name, "--remote"] + files)
    except:
        # list.index throws an exception if there's nothing found (seriously why is that a thing)
        # so if we hit this point, we didn't find a server. So just create a new Vim server with the necessary arguments
        command = [editor] + editor_flags + ['--servername', tmux_current_window, '--remote-silent'] + files

        # the call needs to be run through tmux_send_keys so that tmux recognises that Vim is currently running. This allows vim-tmux-navigator to not break.
        tmux_send_keys(command)


def main():
    # if the OMNIVIM_EDITOR environment variable is set, use it.
    # otherwise, use vim.
    EDITOR = 'vim'
    EDITOR_FLAGS = []
    if os.environ.get('OMNIVIM_EDITOR') is not None and len(os.environ.get('OMNIVIM_EDITOR')) > 0:
        EDITOR_FLAGS = str.split(os.environ.get('OMNIVIM_EDITOR'), ' ')
        EDITOR = EDITOR_FLAGS.pop(0)

    if os.environ.get('NVIM_SOCKET_PATH') is not None and len(os.environ.get('NVIM_SOCKET_PATH')) > 0:
        NVIM_SOCKET_PATH = os.environ.get('NVIM_SOCKET_PATH')
    else:
        NVIM_SOCKET_PATH = '/tmp/'

    # read files from command line arguments
    # we remove the first, since this will always be omnivim.py
    files = sys.argv
    files.pop(0)

    # checking the TMUX environment variable will confirm whether or not tmux is currently running.
    in_tmux = os.environ.get('TMUX')
    lit_flag = files.count("--lit")

    if in_tmux is not None and lit_flag == 0:
        # if tmux is running, then we have different things to do if using neovim or another form of vim
        # use regex to work it out
        is_neovim = re.search('n(eo)?vim', EDITOR)

        if is_neovim is not None:
            call_neovim(EDITOR, EDITOR_FLAGS, files, NVIM_SOCKET_PATH)
        else:
            call_vim(EDITOR, EDITOR_FLAGS, files)
    else:
    # otherwise, just call the editor and flags with the requisite files, no strings (or servers) attached.
        while files.count("--lit") > 0:
            # if lit_flag was passed in, we need to remove it from the list of files before calling
            # TODO: this is pretty damn hacky.
            files.pop(files.index("--lit"))
        subprocess.call([EDITOR] + EDITOR_FLAGS + files)

main()
