# Variables
PYTHON = python
FLASK = flask
PORT = 5001
HOST = 0.0.0.0

# Run the Flask application
run:
	$(PYTHON) -m flask run --host=$(HOST) --port=$(PORT)

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Install requirements
install:
	pip install -r requirements.txt

# Run database checks
check-db:
	curl http://localhost:$(PORT)/api/db-check

# Help command to show available commands
help:
	@echo "Available commands:"
	@echo "  make run         - Run the Flask application"
	@echo "  make clean       - Clean up cache files"
	@echo "  make install     - Install requirements"
	@echo "  make check-db    - Check database status"

.PHONY: run clean install check-db help