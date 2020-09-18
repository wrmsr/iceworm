import pytest


@pytest.mark.skip
def test_z3():
    import z3
    import time

    z3.set_option("sat.gc.burst", False)  # disable GC at every search. It is wasteful for these small queries.

    def diff_at_j_is_i(xs, j, i):
        assert (0 <= j and j + 1 < len(xs))
        assert (1 <= i and i < len(xs))
        return z3.Or([z3.And(xs[j][k], xs[j + 1][k - i]) for k in range(i, len(xs))] +
                     [z3.And(xs[j][k], xs[j + 1][k + i]) for k in range(0, len(xs) - i)])

    def ais(n):
        xij = [[z3.Bool("x_%d_%d" % (i, j)) for j in range(n)] for i in range(n)]
        s = z3.SolverFor("QF_FD")
        # Optionally replace by (slower) default solver if using
        # more then just finite domains (Booleans, Bit-vectors, enumeration types
        # and bounded integers)
        #   s = Solver()
        for i in range(n):
            s.add(z3.AtMost(xij[i] + [1]))
            s.add(z3.Or(xij[i]))
        for j in range(n):
            xi = [xij[i][j] for i in range(n)]
            s.add(z3.AtMost(xi + [1]))
            s.add(z3.Or(xi))
        dji = [[diff_at_j_is_i(xij, j, i + 1) for i in range(n - 1)] for j in range(n - 1)]
        for j in range(n - 1):
            s.add(z3.AtMost(dji[j] + [1]))
            s.add(z3.Or(dji[j]))
        for i in range(n - 1):
            dj = [dji[j][i] for j in range(n - 1)]
            s.add(z3.AtMost(dj + [1]))
            s.add(z3.Or(dj))
        return s, xij

    def process_model(s, xij, n):
        # x_ij integer i is at position j
        # d_ij difference between integer at position j, j+1 is i
        # sum_j d_ij = 1 i = 1,...,n-1
        # sum_j x_ij = 1
        # sum_i x_ij = 1
        m = s.model()
        block = []
        values = []
        for i in range(n):
            k = -1
            for j in range(n):
                if z3.is_true(m.eval(xij[i][j])):
                    assert (k == -1)
                    block += [xij[i][j]]
                    k = j
            values += [k]
        print(values)
        return block

    def all_models(n):
        count = 0
        s, xij = ais(n)
        start = time.clock()
        while z3.sat == s.check():
            print(count)
            block = process_model(s, xij, n)
            print(block)
            import sys
            sys.stdout.flush()
            s.add(z3.Not(z3.And(block)))
            count += 1
        print(s.statistics())
        print(time.clock() - start)
        print(count)

    z3.set_option(verbose=1)
    all_models(12)
