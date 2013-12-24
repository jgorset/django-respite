test:
	django-admin.py test --settings=tests.project.settings

documentation:
	cd docs; make html

release:
	python setup.py sdist register upload
