#!/bin/zsh
tmux new-session -d 'uvicorn --port 9696 --reload --workers 4 main:app'
sleep 1
tmux split-window -h 'python turn.py'
#tmux swap-pane -U
#tmux swap-pane -D
tmux attach-session -d