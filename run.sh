#!/bin/zsh
tmux new-session -d 'ssh -vvv -N -L 27017:localhost:27017 time'
tmux split-window -h 'ssh -vvv -N -L 5672:localhost:5672 time'
sleep 3
tmux swap-pane -U
tmux split-window -v 'uvicorn --port 9696 --reload --workers 4 main:app'
tmux swap-pane -D
tmux split-window -v 'python turn.py'
tmux attach-session -d