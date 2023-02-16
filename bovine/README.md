# bovine

bovine is meant to contain the core ActivityPub Server implementation.
It is based on [quart](https://pypi.org/project/quart/) and meant
to be performant through the use of asynchronous processing.

The basic layout is:

- `bovine.server` contains quart blueprints that define endpoints
- `bovine.processors` contains what I call processors, which are meant
 to perform operations on items arriving in the inbox or outbox. This
 allows one to programmatically define a processing chain for elements
 arriving in the inbox. See `bovine_blog.processors` for a sample
 implementation.
- `bovine.types` defines some objects that help with managing data

## tests

Tests using a mock server provided in `bovine.utils.test.in_memory_test_app`
are located in the `test` folder. These are meant to ensure that the
basic functionality of an ActivityPub Server is implemented correctly.
