#!/usr/bin/env bash

taql "update $1::NAMES set NAME=substr(NAME,0,24)"