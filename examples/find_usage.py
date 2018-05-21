import click

from jawa.classloader import ClassLoader
from jawa.constants import ConstantClass


@click.command()
@click.argument('search-class')
@click.argument('class-path', nargs=-1, type=click.Path(exists=True))
def main(search_class, class_path):
    loader = ClassLoader(*class_path)

    def _filter(c):
        if isinstance(c, ConstantClass):
            if c.name.value == search_class:
                return True
        return False

    for class_ in loader.classes:
        for constant in loader.search_constant_pool(path=class_, f=_filter):
            print(constant)


if __name__ == '__main__':
    main()
