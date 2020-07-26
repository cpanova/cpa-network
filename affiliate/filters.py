from django_filters import Filter
from django_filters.constants import EMPTY_VALUES


class CommaSeparatedTextFilter(Filter):
    """Custom filter allow set multiple values to field filter.

    Note: it use case-sensitive search when choosing from list,
    you should use pre-annotate to lowercase and lookup __in in annotation
    """

    def filter(self, qs, value):

        # if field filled, - cplit by
        if value not in EMPTY_VALUES:
            value = value.split(',')

        # set lookup expression to choose in list or to default iexact
        # it'll be used in superclass
        self.lookup_expr = isinstance(value, list) and 'in' or 'iexact'

        return super(CommaSeparatedTextFilter, self).filter(qs, value)
