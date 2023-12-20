PYTHON=python
# had to change this to work in my environment (was python3)

stages:
	echo verify clean run

verify:
	for f in *.py; do echo $$f; done

run:
	$(PYTHON)  wsuvpyunitrunner.py -f

clean:
	rm -rf *~
