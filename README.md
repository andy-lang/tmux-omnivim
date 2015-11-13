# tmux-omnivim
Vim and Tmux, together as one.

One of my frustrations with Tmux was that if I had a Vim process open in another pane, typing a Vim command would open files in _that_ pane instead of the one that has Vim already running. I looked around and couldn't find anyone who had come up with a solution, so I wrote my own. Here's how it works...

* If there's no instance of Vim open in any of the panes in the *current* Tmux window, typing a `vim file1 file2` command opens a new Vim instance in the pane in which the command was typed.
* If there is a Vim instance open in the current window, then typing a `vim file` command opens those file/s in that running instance.
* If there is a Vim instance running in *another* window, then typing a `vim file` command opens a new Vim instance.

Pretty simple, but pretty nifty.

Please note that this is still very much a work in progress. The main outline of functionality is all here, but there's some issues to be ironed out. Let me know if you stumble upon things that need fixing and I'll take a look.


## Features
* Compatability with Neovim, Vim, and GVim
* Separate Vim instances between Tmux windows
* Custom Vim commands and command line flags
* Tmux not currently open? Vim opens as normal!
* Call Vim without omnipresence using a simple flag
* ...your ideas here...

# Requirements
* **Tmux**
* Either of the following:
  * Vim/GVim compiled with the `clientserver` option
  * Neovim
* Python 2
* A shell environment
  * Bash and Zsh have been tested most extensively


## Installation
Installation is pretty straightforward. Clone the repository with

`git clone https://github.com/andy-lang/tmux-omnivim.git`

and copy the script to your chosen directory.

If you want to use something other than Vim (eg Neovim, GVim), then export the following environment variable:

`export OMNIVIM_EDITOR=_your Vim variant here_`

OMNIVIM_EDITOR can also hold flags, if you want. For example:

`export OMNIVIM_EDITOR=gvim -v`


## FAQ
> What if I want omnivim to run every time I call Vim?

I'm flattered! You can do this with aliases in your shell. Let's assume you've got custom Vim commands and flags that you want called every time as well, like the ones we just talked about. Add this as an alias to your shell:

`alias vim="python /path/to/omnivim.py"`

> What if I don't want omnivim to run on a particular call, but I have it aliased?

Too easy. Just type `--lit` when you call Vim. Any arguments except this flag will be run through a vanilla Vim session.

For example, let's say you want to run Vundle's `+PluginInstall` flag. To do this, just call:

`vim --lit +PluginInstall`

This is particularly useful if you've got Vim aliased to omnivim, but you want to run some command line flags that don't play well with Vim's clientserver stuff, such as `+PluginInstall`. Alternatively, it's useful if you just want another Vim session open in another pane.


## Miscellaneous
Thanks to [@deshawnbw](http://github.com/deshawnbw) for a 'starting point' for the script. The initial shell script relied heavily on his [initial work](https://gist.github.com/deshawnbw/2792055), so thanks heaps!

If you like the script, be sure to star it on GitHub. If you really like it, consider following me on GitHub for potential future projects.
