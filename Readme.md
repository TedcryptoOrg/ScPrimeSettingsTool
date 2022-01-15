#Scprime Price Tracker

This tool allows you to grab the price settings for a specific
provider (e.g.: XA-Miner) which you could then use for your own provider

It is ideal to mimic these to offer a better provider to the network

## Install

This script will need a few things from your machine, so you will
need python3 and pip3 installed. 

After you have done that, you can run `make install` to install all the
libs required to run this script.

## Run

After you have successfully installed the libs you can run the script by

```shell
python3 main.py -url GRAFANA_URL
```

It should then return the settings information

You also have the following options:

 - `--url`: The url of the grafana instance you want to connect to
 - `--config`: The yaml file for the configuration (this could in future be something hosted in the cloud)
 - `--commands`: Return the settings commands you need to run on your provider
 - `--screenshot`: Saves a screenshot on the root folder of the page you are listening too -- useful for debug
 - `--update-settings`: List of settings you want to update, e.g.: `--update-settings="collateral,minstorageprice"`.
It also works with element names from the configuration, e.g.: "minstorageprice" or "storage_price" are the same
