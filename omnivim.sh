#!/bin/bash

# read in parameters. Code is messy already...
varArr=()
for var in "$@"; do
	varArr+=("$var")
done

vimcmd='vim'
vimflags=''
otherflags=()

# parse long arguments
for (( i = 0; i < "${#varArr[@]}"; i++ )); do
	arg=${varArr[$i]}
	case "$arg" in
		"--vimcmd")
			# set vim command to the argument after this
			let i+=1
			vimcmd="${varArr[i]}"
			;;
		"--vimflags")
			# set vim flags to the argument after this
			let i+=1
			vimflags="${varArr[i]}"
			;;
		"--lit")
			# everything after this will be sent to Vim literally, ie without creating an omnivim instance.
			let i+=1
			for (( j = i; j < ${#varArr[@]}; j++ )); do
				otherflags+=(${varArr[$i]})
			done
			$vimcmd $vimflags "${otherflags[@]}"
			exit
			;;
		*)
			otherflags+=($arg)
	esac
done



# make sure we're in tmux. If we are...
if [ -n "$TMUX" ]; then
	currentpaneid=$(tmux display-message -p "#D")
	currentwindowid=$(tmux display-message -p "#{window_id}")
	vimservercount=$($vimcmd $vimflags --serverlist | wc -l)
	winname=${currentpaneid:1} # pane id but without the @

	vimservername="$currentwindowid" # I know this is the a duplicate variable, but it's nice to have for readability's sake

	# no current vim servers open. Create a new vim server
	if [ "$vimservercount" -eq "0" ]; then
		# if command line parameters passed in, use 'em.
		if [ "${#otherflags}" -eq "0" ]; then
			tmux send-keys -t "$currentpaneid" "$vimcmd $vimflags --servername $vimservername" C-m
		else
			tmux send-keys -t "$currentpaneid" "$vimcmd $vimflags --servername $vimservername --remote-silent ${otherflags[@]}" C-m
		fi
	
	# we have at least one vim server open. We want the one that's in the current window (if it exists).
	# to do this we search the list of currently-running vim servers.
	# if there exists a server with this window id, we have a match. Otherwise, open a new instance of Vim in the current pane
	else
		for p in $($vimcmd $vimflags --serverlist); do
			if [ "$p" == "$currentwindowid" ]; then
				$vimcmd $vimflags --servername $vimservername --remote ${otherflags[@]}
				exit
			fi
		done

		if [ "${#otherflags}" -eq "0" ]; then
			tmux send-keys -t "$currentpaneid" "$vimcmd $vimflags --servername $vimservername" C-m
		else
			tmux send-keys -t "$currentpaneid" "$vimcmd $vimflags --servername $vimservername --remote-silent ${otherflags[@]}" C-m
		fi
	fi
# otherwise we're not in tmux. So just launch Vim business as usual
else 
	$vimcmd $vimflags "${otherflags[@]}"
fi

