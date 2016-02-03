### Build

Requirements:
- virtualenv
- pip

The project is a set of modules built with Python 3. Use a virtualenv environment to manage project building and running.

To Start:
1. Create a virtual envirionment using virtualenv and source the environment.

```bash
virtualenv -p Python3 modules
source modules/bin/activate
```

2. Download dependencies
```bash`
pip install -r requirements.txt 
```

### Testing

##### Simulation Tests
Navigate to the 'simulation' folder in the virtual environment and test with
```bash
py.test
```
