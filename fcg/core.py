import inspect


class Construction(object):
    pass


class Structure(object):
    def __init__(self, base=None):
        if base is None:
            base = self
        self._base = base
    def __getattr__(self, key):
        v = Structure(base=self._base)
        self.__dict__[key] = v
        return v
    def extract(self):
        settings = []
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                if isinstance(v, Structure) and v._base==self._base:
                    for kk, vv in v.extract():
                        settings.append(('.'.join([k, kk]), vv))
                else:
                    settings.append((k, v))
        return settings


class DummyStructure(object):
    def __init__(self, name, base=None):
        self._path = name
        if base is None:
            base = name
        self._base = base
    def __getattr__(self, key):
        v = DummyStructure('.'.join([self._path, key]), base=self._base)
        self.__dict__[key] = v
        return v
    def extract(self):
        settings = []
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                if isinstance(v, DummyStructure):
                    if v._base == self._base:
                        for kk, vv in v.extract():
                            settings.append(('.'.join([k, kk]), vv))
                    else:
                        if '.' in v._path:
                            item, target = v._path.split('.', 1)
                            settings.append((k, item, target))
                        else:
                            settings.append((k, v._path, None))
                else:
                    settings.append((k, v))

        return settings


def safe_get(k, v):
    if v is None:
        return k
    elif '.' in v:
        v, vv = v.split('.', 1)
        return safe_get(getattr(k, v), vv)
    else:
        return getattr(k, v, None)


def same(x, y):
    return (x == y) and (x is not None)


class FCG(object):
    def __init__(self):
        self.structures = set()
        self.constructions = set()
        self.matching = dict(produce={}, comprehend={})
        self.applied = set()

    def make_structure(self):
        s = Structure()
        s._id = 's%d' % len(self.structures)
        self.structures.add(s)
        return s

    def add_construction(self, c):
        self.constructions.add(c)

        for fn in ['produce', 'comprehend']:
            f = getattr(c, fn).im_func
            args = inspect.getargspec(f).args
            ds = [DummyStructure(a) for a in args]

            f(*ds)

            match_funcs = []
            for i, arg in enumerate(args):
                for m in ds[i].extract():
                    if len(m) == 2:
                        f = lambda x, i=i, key=m[0], v=m[1]: safe_get(x[i],key)==v
                    elif len(m) == 3:
                        j = args.index(m[1])
                        f = lambda x, i=i, key=m[0], j=j, key2=m[2]: same(safe_get(x[i],key),safe_get(x[j], key2))

                    match_funcs.append(f)

            m = self.matching[fn]
            if len(args) not in m:
                m[len(args)] = {}
            m[len(args)][c] = match_funcs


    def generate_all_combos(self, count):
        if count == 1:
            for s in self.structures:
                yield [s]
        else:
            for s in self.structures:
                for ss in self.generate_all_combos(count-1):
                    yield [s] + ss

    def find_matches(self, style):
        for count, cons in self.matching[style].items():
            for items in self.generate_all_combos(count):
                for c, ms in cons.items():
                    for m in ms:
                        if not m(items):
                            break
                    else:
                        if (c, tuple(items)) not in self.applied:
                            yield c, items

    def step(self, style):
        m = list(self.find_matches(style))
        print 'found %d matches' % len(m)
        if len(m) == 0:
            return

        c, items = m[0]
        print 'applying %s.%s(%s)' % (c.__name__, style, ','.join(x._id for x in items))

        for fn in ['produce', 'comprehend']:
            if fn != style:
                getattr(c, fn).im_func(*items)

        self.applied.add((c, tuple(items)))

        contribute = getattr(c, 'contribute').im_func
        args = inspect.getargspec(contribute).args
        while len(args) > len(items):
            items.append(self.make_structure())
        contribute(*items)


    def display(self):
        for s in self.structures:
            print s
            for k, v in s.extract():
                print '  %s: %r' % (k, v)

