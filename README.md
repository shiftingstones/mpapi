# Star Wars Mission Planning API
An API to determine what starships in the Star Wars universe support your mission parameters.  The MPAPI project is a FastAPI service exposing one authenticated endpoint at `/api/v1/starship-readiness`.  The endpoint retrieves all starships that can accommodate the specified passenger capacity, hyperdrive requirements, and any additional cargo weight.

## Setup and Test

- Clone the repo and drop into the new directory.

  ```
  git clone https://github.com/shiftingstones/mpapi.git mpapi-repo && cd mpapi-repo
  ```

- Run the unit tests in a docker container.  All four tests should pass.

  ```
  docker compose run --rm test
  ```

- Start the app in a docker container.  Log messages will be displayed to the console.
  ```
  docker compose up app
  ```

- Open a new terminal and test with curl.  The API authentication key is `hansolofalcon`.
  ```
  curl -D - -X 'GET' \
    'http://localhost:8000/api/v1/starship-readiness?num-passengers=100&hyperdrive-required=true&cargo-weight=0' \
    -H 'accept: application/json' \
    -H 'x-api-key: hansolofalcon'
  ```
