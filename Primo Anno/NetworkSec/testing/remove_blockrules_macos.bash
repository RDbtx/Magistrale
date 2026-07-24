#!/bin/zsh

sudo pfctl -t blackwall_blocked -T flush
sudo pfctl -f /etc/pf.conf


echo "\n\nRULES:"
sudo pfctl -sr