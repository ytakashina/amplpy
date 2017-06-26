from .utils import Utils, Tuple


class Iterator:
    def __init__(self, obj, function):
        self.obj = obj
        self.it = obj.begin()
        self.end = obj.end()
        self.function = function

    def __iter__(self):
        return self

    def __getitem__(self, key):
        assert isinstance(key, basestring)
        return self.function(self.obj.getIndex(key))

    def next(self):
        if self.it.equals(self.end):
            raise StopIteration
        toReturn = self.function(self.it)
        self.it.postIncrement()
        return toReturn


class EntityIterator(Iterator):
    def __init__(self, obj, entityClass):
        def pair(it):
            entity = entityClass(it.__ref__())
            return (entity.name(), entity)
        Iterator.__init__(self, obj, pair)

    def size(self):
        return int(self.obj.size())

    def __len__(self):
        return self.size()


class InstanceIterator(Iterator):
    def __init__(self, obj, instanceClass):
        Iterator.__init__(
            self, obj,
            lambda it: (
                Tuple.fromTupleRef(it.first()).toPyObj(),
                instanceClass(it.second())
            ),
        )

    def size(self):
        return int(self.obj.numInstances())

    def __len__(self):
        return self.size()


class MemberRangeIterator(Iterator):
    """Iterator for set members."""
    def __init__(self, obj, sizeFunction):
        Iterator.__init__(
            self, obj,
            lambda it: Tuple.fromTupleRef(it.__ref__()).toPyObj()
        )
        # FIXME: MemberRange does not implemet size()
        self.sizeFunction = sizeFunction

    def size(self):
        return int(self.sizeFunction())

    def __len__(self):
        return self.size()


def EnvIterator(obj):
    """Iterator for environment classes."""
    return Iterator(
        obj,
        lambda it: (it.first(), it.second())
    )


def ColIterator(obj):
    return Iterator(
        obj,
        lambda it: Utils.castVariantRef(it.__ref__())
    )


def RowIterator(obj):
    return Iterator(
        obj,
        lambda it: Utils.castVariantRef(it.__ref__())
    )
