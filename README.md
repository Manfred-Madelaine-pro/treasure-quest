# :world_map: Treasure Quest :mountain:

## :electric_plug: Dependencies
1. :desktop_computer: Set your Virtual Environment :

	``` bash
	# Download venv librairy
	apt-get install python3-venv -y
	# Create your venv
	py -m venv my_venv
	# Activate your venv
	. venv/bin/activate
	```
	
	_For more information, go to [Python Virtual Environment Official Documentation](https://docs.python.org/3/library/venv.html)._


1. :package: Install the project dependencies

	``` bash
	pip install parameterized
 	pip install nose2
	```

## :zap: Quick start

1. To start the project, simply run bellow commands:

	``` bash
	python back.py
	```

2. To run the tests, simply run bellow commands:

	``` bash
	python -m unittest discover
 	# or
 	nose2
	```