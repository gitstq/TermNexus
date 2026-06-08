# Makefile for TermNexus

.PHONY: help install test clean build lint format check

PYTHON := python3
PIP := pip3

help:
	@echo "TermNexus - Available Commands:"
	@echo "  make install    - Install package in development mode"
	@echo "  make test       - Run all tests"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build distribution packages"
	@echo "  make lint       - Run code linting"
	@echo "  make format     - Format code"
	@echo "  make check      - Run all checks (lint + test)"

install:
	$(PIP) install -e .

test:
	$(PYTHON) -m unittest discover tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	$(PYTHON) -m build

lint:
	$(PYTHON) -m flake8 termnexus/ tests/ --max-line-length=120 --ignore=E501,W503

format:
	$(PYTHON) -m black termnexus/ tests/ --line-length=120

check: lint test
	@echo "All checks passed!"
