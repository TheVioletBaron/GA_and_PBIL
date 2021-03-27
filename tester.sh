#!/bin/sh


for file in /source/maxsat-problems/*
do
    if [[ -f $file ]]; then
        python3 GA.py
    fi
done