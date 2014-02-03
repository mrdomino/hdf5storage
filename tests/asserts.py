import collections

import numpy as np
import numpy.testing as npt

def assert_equal(a, b):
    # Compares a and b for equality. If they are dictionaries, they must
    # have the same set of keys, after which they values must all be
    # compared. If they are a collection type (list, tuple, set,
    # frozenset, or deque), they must have the same length and their
    # elements must be compared. If they are not numpy types (aren't
    # or don't inherit from np.generic or np.ndarray), then it is a
    # matter of just comparing them. Otherwise, their dtypes and shapes
    # have to be compared. Then, if they are not an object array,
    # numpy.testing.assert_equal will compare them elementwise. For
    # object arrays, each element must be iterated over to be compared.
    assert type(a) == type(b)
    if type(b) == dict:
        assert set(a.keys()) == set(b.keys())
        for k in b:
            assert_equal(a[k], b[k])
    elif type(b) in (list, tuple, set, frozenset, collections.deque):
        assert len(a) == len(b)
        if type(b) in (set, frozenset):
            assert a == b
        else:
            for index in range(0, len(a)):
                assert_equal(a[index], b[index])
    elif not isinstance(b, (np.generic, np.ndarray)):
        assert a == b
    else:
        assert a.dtype == b.dtype
        assert a.shape == b.shape
        if b.dtype.name != 'object':
            npt.assert_equal(a, b)
        else:
            for index, x in np.ndenumerate(a):
                assert_equal(a[index], b[index])


def assert_equal_none_format(a, b):
    # Compares a and b for equality. b is always the original. If they
    # are dictionaries, they must have the same set of keys, after which
    # they values must all be# compared. If they are a collection type
    # (list, tuple, set, frozenset, or deque), then the compairison must
    # be made with b converted to an object array. If the original is
    # not a numpy type (isn't or doesn't inherit from np.generic or
    # np.ndarray), then it is a matter of converting it to the
    # appropriate numpy type. Otherwise, both are supposed to be numpy
    # types. For object arrays, each element must be iterated over to be
    # compared. Then, if it isn't a string type, then they must have the
    # same dtype, shape, and all elements. If it is an empty string,
    # then it would have been stored as just a null byte (recurse to do
    # that comparison). If it is a bytes_ type, the dtype, shape, and
    # elements must all be the same. If it is string_ type, we must
    # convert to uint32 and then everything can be compared.
    if type(b) == dict:
        assert set(a.keys()) == set(b.keys())
        for k in b:
            assert_equal_none_format(a[k], b[k])
    elif type(b) in (list, tuple, set, frozenset, collections.deque):
        assert_equal_none_format(a, np.object_(list(b)))
    elif not isinstance(b, (np.generic, np.ndarray)):
        if b is None:
            # It should be np.float64([])
            assert type(a) == np.ndarray
            assert a.dtype == np.float64([]).dtype
            assert a.shape == (0, )
        elif isinstance(b, (bytes, str, bytearray)):
            assert a == np.bytes_(b)
        else:
            assert_equal_none_format(a, np.array(b)[()])
    else:
        if b.dtype.name != 'object':
            if b.dtype.char in ('U', 'S'):
                if b.shape == tuple() and len(b) == 0:
                    assert_equal(a, \
                        np.zeros(shape=tuple(), dtype=b.dtype.char))
                elif b.dtype.char == 'U':
                    c = np.atleast_1d(b).view(np.uint32)
                    assert a.dtype == c.dtype
                    assert a.shape == c.shape
                    npt.assert_equal(a, c)
                else:
                    assert a.dtype == b.dtype
                    assert a.shape == b.shape
                    npt.assert_equal(a, b)
            else:
                assert a.dtype == b.dtype
                assert a.shape == b.shape
                npt.assert_equal(a, b)
        else:
            assert a.dtype == b.dtype
            assert a.shape == b.shape
            for index, x in np.ndenumerate(a):
                assert_equal_none_format(a[index], b[index])


def assert_equal_matlab_format(a, b):
    # Compares a and b for equality. b is always the original. If they
    # are dictionaries, they must have the same set of keys, after which
    # they values must all be# compared. If they are a collection type
    # (list, tuple, set, frozenset, or deque), then the compairison must
    # be made with b converted to an object array. If the original is
    # not a numpy type (isn't or doesn't inherit from np.generic or
    # np.ndarray), then it is a matter of converting it to the
    # appropriate numpy type. Otherwise, both are supposed to be numpy
    # types. For object arrays, each element must be iterated over to be
    # compared. Then, if it isn't a string type, then they must have the
    # same dtype, shape, and all elements. All strings are converted to
    # numpy.str_ on read. If it is empty, it has shape (1, 0). A
    # numpy.str_ has all of its strings per row compacted together. A
    # numpy.bytes_ string has to have the same thing done, but then it
    # needs to be converted up to UTF-32 and to numpy.str_ through
    # uint32.
    #
    # In all cases, we expect things to be at least two dimensional
    # arrays.
    if type(b) == dict:
        assert set(a.keys()) == set(b.keys())
        for k in b:
            assert_equal_matlab_format(a[k], b[k])
    elif type(b) in (list, tuple, set, frozenset, collections.deque):
        assert_equal_matlab_format(a, np.object_(list(b)))
    elif not isinstance(b, (np.generic, np.ndarray)):
        if b is None:
            # It should be np.zeros(shape=(0, 1), dtype='float64'))
            assert type(a) == np.ndarray
            assert a.dtype == np.dtype('float64')
            assert a.shape == (1, 0)
        elif isinstance(b, (bytes, str, bytearray)):
            if len(b) == 0:
                assert_equal(a, np.zeros(shape=(1, 0), dtype='U'))
            elif isinstance(b, (bytes, bytearray)):
                assert_equal(a, np.atleast_2d(np.str_(b.decode())))
            else:
                assert_equal(a, np.atleast_2d(np.str_(b)))
        else:
            assert_equal(a, np.atleast_2d(np.array(b)))
    else:
        if b.dtype.name != 'object':
            if b.dtype.char in ('U', 'S'):
                if len(b) == 0 and (b.shape == tuple() \
                        or b.shape == (0, )):
                    assert_equal(a, np.zeros(shape=(1, 0),
                                 dtype='U'))
                elif b.dtype.char == 'U':
                    c = np.atleast_1d(b)
                    c = np.atleast_2d(c.view(np.dtype('U' \
                        + str(c.shape[-1]*c.dtype.itemsize//4))))
                    assert a.dtype == c.dtype
                    assert a.shape == c.shape
                    npt.assert_equal(a, c)
                elif b.dtype.char == 'S':
                    c = np.atleast_1d(b)
                    c = c.view(np.dtype('S' \
                        + str(c.shape[-1]*c.dtype.itemsize)))
                    c = np.uint32(c.view(np.dtype('uint8')))
                    c = c.view(np.dtype('U' + str(c.shape[-1])))
                    c = np.atleast_2d(c)
                    assert a.dtype == c.dtype
                    assert a.shape == c.shape
                    npt.assert_equal(a, c)
                    pass
                else:
                    c = np.atleast_2d(b)
                    assert a.dtype == c.dtype
                    assert a.shape == c.shape
                    npt.assert_equal(a, c)
            else:
                c = np.atleast_2d(b)
                # An empty complex number gets turned into a real
                # number when it is stored.
                if np.prod(c.shape) == 0 \
                        and b.dtype.name.startswith('complex'):
                    c = np.real(c)
                assert a.dtype == c.dtype
                assert a.shape == c.shape
                npt.assert_equal(a, c)
        else:
            c = np.atleast_2d(b)
            assert a.dtype == c.dtype
            assert a.shape == c.shape
            for index, x in np.ndenumerate(a):
                assert_equal_matlab_format(a[index], c[index])