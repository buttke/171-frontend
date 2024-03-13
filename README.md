# HOW TO RUN

## SETUP

(Assuming you already pulled the repo and have a shell in it)

(`git clone git@github.com:buttke/171-frontend.git` etc.)

### Venv

Venv is Python's virtual environment. Python now mandates that packages either
be installed globally by a package manager (not pip) or installed to a virtual
environment with pip or some pip replacement. Venv is best suited for this use
case, so to set up a virtual environment, you can use the following command.


```
python3 -m venv .venv
```

You can then activate the environment by running

```
source .venv/bin/activate
```

This is a bit different on Windows.

More info [here](https://docs.python.org/3/library/venv.html)

### Install requirements

Once the venv is active, run

```
pip install -r requirements.txt
```

## RUN

Then you may simply run the server:

```
python server.py
```

Which will now be accessible from a web browser at [http://127.0.0.1:5001](http://127.0.0.1:5001)
