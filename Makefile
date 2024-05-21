security:
	bandit ./bot/*.py

style:
	pylint -j 4 ./bot/*.py