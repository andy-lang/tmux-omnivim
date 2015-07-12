#!/usr/bin/env bash

# if you have a custom alias for vim (eg default flag commands), change this variable as necessary in order to maintain it.
vim_command="gvim"
vim_flags="-v"

# make sure we're in tmux. If we are...
if [ -n "$TMUX" ]; then
	currentpaneid=$(tmux display-message -p "#D")
	currentwindowid=$(tmux display-message -p "#{window_id}")
	vimservercount=$($vim_command $vim_flags --serverlist | wc -l)
	winname=${currentpaneid:1} # pane id but without the @

	vimservername="$currentwindowid" # I know this is the a duplicate variable, but it's nice to have for readability's sake

	# no current vim servers open. Create a new vim server
	if [ "$vimservercount" -eq "0" ]; then
		# if command line parameters passed in, use 'em.
		if [ "$#" -eq "0" ]; then
			tmux send-keys -t "$currentpaneid" "$vim_command $vim_flags --servername $vimservername" C-m
		else
			tmux send-keys -t "$currentpaneid" "$vim_command $vim_flags --servername $vimservername --remote-silent $*" C-m
		fi
	
	# we have at least one vim server open. We want the one that's in the current window (if it exists).
	# to do this we search the list of currently-running vim servers.
	# if there exists a server with this window id, we have a match. Otherwise, open a new instance of Vim in the current pane
	else
		for p in $($vim_command $vim_flags --serverlist); do
			if [ "$p" == "$currentwindowid" ]; then
				$vim_command $vim_flags --servername $vimservername --remote $*
				exit
			fi
		done

		if [ "$#" -eq "0" ]; then
			tmux send-keys -t "$currentpaneid" "$vim_command $vim_flags --servername $vimservername" C-m
		else
			tmux send-keys -t "$currentpaneid" "$vim_command $vim_flags --servername $vimservername --remote-silent $*" C-m
		fi
	fi
# otherwise we're not in tmux. So just launch Vim business as usual
else 
	$vim_command $vim_flags "$*"
fi

