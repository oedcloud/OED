#!/bin/bash
tsocks git config --global user.name "oedcloud"
tsocks git config --global user.email "friendshipcloud@gmail.com"
tsocks git remote rm origin
tsocks git remote add origin git@github.com:oedcloud/OED.git
tsocks git add .
tsocks git commit -asm "Update"
tsocks git push origin
