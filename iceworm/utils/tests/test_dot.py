from .. import dot


def test_dot():
    print(dot.render(dot.Value.of('hi')))
    print(dot.render(dot.Value.of([['a', 'b'], ['c', 'd']])))

    def print_and_open(no):
        print(no)
        gv = dot.render(no)
        print(gv)
        # dot.open_dot(gv)

    print_and_open(dot.Graph(
        [
            dot.Node('a', {'shape': 'box'}),
            dot.Node('b', {'label': [['a', 'b'], ['c', 'd']]}),
            dot.Edge('a', 'b'),
        ],
    ))
