#!/bin/bash +x

# src -> build -> pdf
mkdir -p /src
mkdir -p /build
mkdir -p /pdf

cp -r /src/* /build/
cd build || exit
arara main.tex || (cat /build/main.log ; exit 2)
cp /build/main.pdf /pdf/ || (cat /build/main.log ; exit 2)
