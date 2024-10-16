.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "✔︎ Creating virtual environment using poetry"
	@poetry install
	@poetry run pre-commit install
	@poetry lock --no-update
	@poetry shell
	@export PYTHONPATH=$(shell pwd)

.PHONY: check
check: ## Run code quality tools.
	@echo "✔︎ Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "✔︎ Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "✔︎ Static type checking: Running mypy"
	@poetry run mypy
	@echo "✔︎ Running deptry"
	@poetry run deptry .

.PHONY: gasless-solver-test
gasless-solver-test:
	@echo "🚀 [$(env) env] Running solver integration tests in gasless mode..." 
	@poetry run pytest --chain-id=$(chain-id) --gasless=true --solver=$(solver) --env=$(env) tests/solver_integration_test.py

.PHONY: self-exec-solver-test
self-exec-solver-test:
	@echo "🚀 [$(env) env] Running solver integration tests in self-execution mode..."
	@poetry run pytest --chain-id=$(chain-id) --gasless=false --solver=$(solver) --env=$(env) tests/solver_integration_test.py

.PHONY: gasless-maker-test
gasless-maker-test:
	@echo "🚀 [$(env) env] Running maker integration tests in gasless mode..." 
	@poetry run pytest --chain-id=$(chain-id) --gasless=true --maker=$(maker) --env=$(env) tests/maker_integration_test.py

.PHONY: self-exec-maker-test
self-exec-maker-test:
	@echo "🚀 [$(env) env] Running maker integration tests in self-execution mode..."
	@poetry run pytest --chain-id=$(chain-id) --gasless=false --maker=$(maker) --env=$(env) tests/maker_integration_test.py
