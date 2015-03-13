html:
	cd docs; make html

push-docs:
	ghp-import -n -p docs/_build/html
