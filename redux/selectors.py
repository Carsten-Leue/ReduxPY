"""
    Selector related helper functions
"""
from operator import is_
from typing import Callable, TypeVar

from rx import pipe
from rx import Observable
from rx.operators import distinct_until_changed, map, multicast, ref_count
from rx.subject import ReplaySubject

T1 = TypeVar('T1')
T2 = TypeVar('T2')
Mapper = Callable[[T1], T2]


def select(selector: Mapper[T1, T2]
           ) -> Callable[[Observable], Observable]:
    """ Reactive operator that applies a selector
        and shares the result across multiple subscribers

        Args:
            selector: the selector function

        Returns:
            The reactive operator
    """
    return pipe(
        map(selector),
        distinct_until_changed(comparer=is_),
        multicast(subject=ReplaySubject(1)),
        ref_count(),
    )
