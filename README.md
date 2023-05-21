# what-the-fec


1. Ensure the following are installed and configured
    a. python3.9 (with pyenv)
    b. poetry
    c. docker compose
    d. Make (author used GNU Make)


2. Setup poetry virtual environment

    From project root run:

    ```
    poetry env use python3.9

    poetry install
    ```


3. Copy `.env-example` to a file named `.env` and populate `.env` with values


4. Run application in developer mode

    From project root run:

    ```
    make dev
    ```
