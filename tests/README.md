# Tests

This folder contains the structure to run more complicated
tests. The goal is to provide sufficient coverage that if
these tests pass, it is safe to deploy to production.

Tests can be run via

```bash
poetry run pytest
```

## Test data

The folder `data` contains json files containing sample activities
collected from traffic. They are used to provide realistic results
when running the tests.
