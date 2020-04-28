import importlib


def load_tests(name):
    # Load module which contains test data
    tests_module = importlib.import_module(name)
    # Tests are to be found in the variable `tests` of the module
    for test in tests_module.tests.iteritems():
        yield test

def test_feature(chess_data):
    assert chess_data < 5