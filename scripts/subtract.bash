#!/usr/bin/env bash

taql "update $1 set CORRECTED_DATA = CORRECTED_DATA - MODEL_DATA_HIGHRES"