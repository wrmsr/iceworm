from .. import parsing


def test_minml():
    print(parsing.parse('{"hi": 1}'))

    for s in [
        '1',
        '"a": null',
        '"b": null, \n "c": 420',
        '{"b": null, "c": 420}',
        '{a: b}',
        '{a: b,}',
    ]:
        if not s.startswith('{') and s.startswith('}'):
            s = '{' + s + '}'
        print(parsing.parse(s))
