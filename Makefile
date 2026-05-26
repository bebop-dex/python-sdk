.PHONY: install
install: ## Install the environment and pre-commit hooks
	@echo "✔︎ Syncing environment with uv"
	@uv sync --all-groups
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "✔︎ Checking lockfile consistency: uv lock --check"
	@uv lock --check
	@echo "✔︎ Linting code: pre-commit"
	@uv run pre-commit run -a
	@echo "✔︎ Static type checking: mypy"
	@uv run mypy
	@echo "✔︎ Running deptry"
	@uv run deptry .

.PHONY: gasless-solver-test
gasless-solver-test:
	@echo "🚀 [$(env) env] Running solver integration tests in gasless mode..."
	@uv run pytest --chain-id=$(chain-id) --gasless=true --solver=$(solver) --env=$(env) tests/solver_integration_test.py

.PHONY: self-exec-solver-test
self-exec-solver-test:
	@echo "🚀 [$(env) env] Running solver integration tests in self-execution mode..."
	@uv run pytest --chain-id=$(chain-id) --gasless=false --solver=$(solver) --env=$(env) tests/solver_integration_test.py

.PHONY: gasless-maker-test
gasless-maker-test:
	@echo "🚀 [$(env) env] Running maker integration tests in gasless mode..."
	@uv run pytest --chain-id=$(chain-id) --gasless=true --maker=$(maker) --env=$(env) tests/maker_integration_test.py

.PHONY: self-exec-maker-test
self-exec-maker-test:
	@echo "🚀 [$(env) env] Running maker integration tests in self-execution mode..."
	@uv run pytest --chain-id=$(chain-id) --gasless=false --maker=$(maker) --env=$(env) tests/maker_integration_test.py
