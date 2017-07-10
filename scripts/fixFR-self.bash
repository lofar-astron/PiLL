#!/usr/bin/env bash

taql "update $1::NAMES set NAME=replace(NAME,\':@MODEL_DATA\',\'\')"