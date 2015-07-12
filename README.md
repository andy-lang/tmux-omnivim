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
  * If you need to check whether your version of Vim has this available, run the following command: `vim --version | grep clientserver`. If you see '`+clientserver`' (the '+' is important), then you're good to go. Otherwise, you'll need to find a way to install Vim with this option - either compile the executable yourself, or find a version that has it compiled.
* A shell
  * I've tested this code most heavily on Bash, so it's guaranteed best to work there. However, I've done some testing on Zsh as well and it works just as well.
  * If you have other scripting environments that don't work, then let me know and I'll see what I can do. Alternatively, fix it yourself and send me a pull request.
 

## Installation
Installation is pretty straightforward. Clone the repository with
`git clone https://github.com/andy-lang/tmux-omnivim.git`
and copy the script to your chosen directory. Make sure it's executable with `chmod +x`, too.

If you want the script to be executed every time you call Vim (thus ensuring complete consistency of Vim instances in Tmux), then just alias Vim to the directory of the script. In Bash, this would be ```alias vim=/path/to/omnivim.sh```.

## Features
* Separate Vim instances between Tmux windows
* Custom Vim commands and command line flags
* Tmux not currently open? Vim opens as normal!
* ...your ideas here...

## Known Issues
* Some command line arguments don't work wonderfully well. For example, passing the `-e` parameter just means that Vim opens a new file called '-e'. I'm working on a fix to this.
* Plugins break if they have command line options. For example, Vundle's `+PluginInstall` parameter won't work. I'm also working on a 'catch-all' fix to this.

## FAQ
> But what if I want to use a different version of Vim? eg Neovim, GVim, etc?

Not to worry! I've made an option for this available in the script. Just change the `vim_command` variable to be your customised command. For example, if you want Neovim, then just change the line to be ```vim_command='nvim'```. Other commands would work similarly.

> What if I have custom command line flags that I want executed every time I call Vim?

I've made this option available, too. Similar to the above, change the `vim_flags` variable to contain the arguments that you want. I haven't tested this extensively, though, so let me know if there are any issues and I'll get them sorted.

## Miscellaneous Thanks and Stuff
Thanks to @deshawnbw for a 'starting point' for the script. I've relied on his [initial script](https://gist.github.com/deshawnbw/2792055) heavily for this project, so mad props to him for doing a lot of the initial work. Also thanks to @ReeceH for letting me blab to him about the issues I was having with the script, and his ideas on why they were happening.

If you like the script, be sure to star it on GitHub. If you really like it, consider following me on GitHub for potential future projects.
