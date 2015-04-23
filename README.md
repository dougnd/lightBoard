# lightBoard

The code for [Out of Artifice's](outofartifice.com) lighting control board.

## Usage

### Simulator

The simulator can be run with:

    python run.py sim


### On Board

The real version is meant to be run on a beaglebone black with the following pinouts:
* "P8_15", previous program
* "P8_16", next program
* "P8_17", turn front lights on
* "P8_18", turn all lights off
* "P8_9", button 1
* "P8_10", button 2
* "P8_11", button 3
* "P8_12", button 4
* "P8_14", button 5


Run it with:

    sudo python run.py
