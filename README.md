# Python Compiler

Python compiler with Spanish sintax to help Mexican kids in their introduction to Computer Science.

## Prerequisites
You need to have Docker installed on your local machine.

## Installing
Download the entire folder to your computer and then open your terminal and navigate to its location.

Then run

```
docker-compose up
```
This will run `python app.py` and start the server in `localhost:5000`.

For shutting down use
```
docker-compose down
```

## Bash
In order to enter to bash run
```
docker-compose run api bash
```

## Compiler

Modify `input.txt` file as this will be the input of the compiler.

Run:

```
python compiler/parser.py
```

## Tests

Add a `test*.txt` file inside `tests` folders for a new test.

Then run:

```
python compiler/parser.py -t
```

in order to execute all of the tests files and log the errors if found.
