#!/bin/bash

# --->>> Define color variables. TODO: Move to common script for all tests
# Normal colors
declare -r C_RED='\e[0;31m'
declare -r C_GREEN='\e[0;32m'
declare -r C_YELLOW='\e[0;33m'
declare -r C_BLUE='\e[0;34m'

# Bold colors
declare -r C_RED_B='\e[1;31m'
declare -r C_GREEN_B='\e[1;32m'
declare -r C_YELLOW_B='\e[1;33m'
declare -r C_BLUE_B='\e[1;34m'

# Underline colors
declare -r C_RED_U='\e[4;31m'
declare -r C_GREEN_U='\e[4;32m'
declare -r C_YELLOW_U='\e[4;33m'
declare -r C_BLUE_U='\e[4;34m'

declare -r C_NONE='\e[0m' # No Color / Reset
