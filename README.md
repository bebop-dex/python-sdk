<h3>Running the solver integration tests</h3>

1. Install the dependencies: `make install`

2. Set up your environment.
    1. Create a `.env` file at the root of the project
    2. Supply your private key as `PRIVATE_KEY=...`
    3. (_OPTIONAL_) If you're running the tests on the *TEST* environment, you need to add basic authentication to your env. Add the following to the `.env`:
        - `LOGIN=...`
        - `PASSWORD=...`

3. Run the tests
    - Gasless Mode: `make gasless-solver-test chain-id={CHAIN_ID} solver={SOLVER_EMOJI} env={ENV}`
    - Self-Execution Mode: `make self-exec-solver-test chain-id={CHAIN_ID} solver={SOLVER_EMOJI} env={ENV}`
