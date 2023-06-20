install:
	python -m pip install -r requirements.txt

run: 
	if [ "$1" = "--demo"]; then \
		python -m src.game.main --demo; \
	else \
		python -m src.game.main; \
	fi