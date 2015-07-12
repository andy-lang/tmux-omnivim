# tmux-omnivim
Vim and Tmux, together as one.

Imagine the scene: you're using Tmux with several panes in the same window. In one pane is an instance of Vim that you're running, with all of your buffers open. In another pane, you've got directories open in various locations, which you're using to browse around projects and the like. But then you realise you need to open another file that's in one of those directories. So you type `vim file` to open the file, and...oh. Right. It opens another Vim instance in that pane. That's not what you wanted at all! You want a single Vim instance in the window; the pivot upon which your workflow hinges! 

This is where omnivim comes to the rescue. By harnessing the powers of Vim and Tmux combined, you can keep a single Vim instance in the pane in which it was first called, on a per-window basis. Here's how it works...
* If there's no instance of Vim open in any of the panes in the *current* window, typing a `vim file` command opens a new Vim instance in the pane in which the command was typed (i.e. how every terminal command has worked since the dawn of time).
* If there is a Vim instance open in the current window, then typing a `vim file` command opens those file/s in that running instance.
* If there is a Vim instance running in *another* window, then typing a `vim file` command opens a new Vim instance.

Pretty simple, but pretty nifty.

Please note that this is still very much a work in progress. The main outline of functionality is all here, but there's some issues to be ironed out. Let me know if you stumble upon things that need fixing and I'll take a look.

## Requirements
Most of these requirements come by default, but it's still nice to let you know.
* **Tmux** (duh)
  * I've tested 1.9 and 1.9a and they both work fine. Basically so long as you have a version of Tmux that has the send-keys command (which has been around since 2008), then the script *should* work fine. Let me know if they don't, and I'll take a look.
* **Vim** (duh)
  * The only caveat here is that Vim **must** be compiled with the `clientserver` option. There is no way around this, as the script relies heavily on the use of the --servername flag.
  * If you need to check whether your version of Vim has this available, run the following command:

  `vim --version | grep clientserver`
  
  If you see `+clientserver` (the '+' is important), then you're good to go. Otherwise, you'll need to find a way to install Vim with this option - either compile the executable yourself, or find a version that has it compiled.
* **A shell**
  * I've tested this code most heavily on Bash, so it's guaranteed best to work there. However, I've done some testing on Zsh as well and it works just as well.
  * If you have other shell environments that don't work, then let me know and I'll see what I can do. Alternatively, fix it yourself and send me a pull request.
 

## Installation
Installation is pretty straightforward. Clone the repository with

`git clone https://github.com/andy-lang/tmux-omnivim.git`

and copy the script to your chosen directory. Make sure it's executable with `chmod +x`, too.

## Features
* Separate Vim instances between Tmux windows
* Custom Vim commands and command line flags
* Tmux not currently open? Vim opens as normal!
* Call Vim without omnipresence using a simple flag
* ...your ideas here...


## Known Issues
See TODO.md for a list of bugs that need to be fixed, as well as some potential future features.


## FAQ
> But what if I want to use a different version of Vim? eg Neovim, GVim, etc?

Not to worry! I've made an option for this available in the script. Use the command line flag `--vimcmd` to change the Vim command that's executed. For example, if you want to use GVim by default, you'd call the program as follows:

`omnivim.sh --vimcmd gvim`

> What if I have Vim command line flags that I want executed?

I've made this option available, too. Similar to the above, there's a command line flag `--vimflags` to set a list of Vim flags that will be called when you call this script. Let's say you want to use the flags -n (for no swap file) and -R (read only mode). To do this, call omnivim as follows:

`omnivim.sh --vimflags "-n -R"`

Please note that the quotes are *extremely* important. Without them only the first flag will be set.

> What if I want omnivim to run every time I call Vim?

I'm flattered! You can do this with Bash aliases. Let's assume you've got custom Vim commands and flags that you want called every time as well. Add this to your Bash aliases file:

`alias vim="/path/to/omnivim.sh --vimcmd gvim --vimflags \"-n -R\""`

> What if I don't want omnivim to run on a particular call?

Too easy. Just type `--lit` when you call Vim. Any arguments after this flag will be run through a vanilla Vim session. For example, let's say you want to run Vundle's `+PluginInstall` flag, so you don't want it run through a server. To do this, just call:

`vim --lit +PluginInstall`

This is particularly useful if you've got Vim aliased to omnivim, but you want to run some command line flags that don't play well with Vim's clientserver stuff, such as `+PluginInstall`. Alternatively, it's useful if you just want another Vim session open in another pane.


## Miscellaneous
Thanks to [@deshawnbw](http://github.com/deshawnbw) for a 'starting point' for the script. I've relied on his [initial script](https://gist.github.com/deshawnbw/2792055) heavily for this project, so mad props to him for doing a lot of the initial work. Also thanks to [@ReeceH](http://github.com/ReeceH) for letting me blab to him about the issues I was having with the script, and his ideas on why they were happening.

If you like the script, be sure to star it on GitHub. If you really like it, consider following me on GitHub for potential future projects.
