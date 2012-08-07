test:
	DJANGO_SETTINGS_MODULE=tests.project.settings nosetests

documentation:
	cd docs; make html

release:
	python setup.py sdist register upload
