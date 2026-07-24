#!/bin/zsh

sudo pfctl -f - << 'EOF'
table <blackwall_blocked> persist
block drop in quick from <blackwall_blocked> to any
EOF
sudo pfctl -e

echo "\n\nRULES:"
sudo pfctl -sr