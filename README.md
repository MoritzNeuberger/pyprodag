# pyprodag
A simple process data aggregator tool to monitor processes on your computer. Created as an exercise to get back into Python.

# Usage
The tool runs as a daemon process in the background of the system and monitores the processes according to a `settings.json` file.
To specify which `settings.json` file is used, use
```
python run_data_aggregator_daemon.py -s "settings_1.json" 
```

An example for how one can structure a `settings.json` is given in `example_settings.json`.

Under the `cwd` given in the settings, the tool will create new sub-folders in which the aggregated data is stored.
