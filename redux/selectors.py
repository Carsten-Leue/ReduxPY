"""
    Selector related helper functions
"""
from operator import is_
from typing import Callable

from rx import pipe
from rx.core.typing import T1, T2, Mapper, Observable
from rx.operators import distinct_until_changed, map, multicast, ref_count
from rx.subject import ReplaySubject


def select(selector: Mapper) -> Callable[[Observable[T1]], Observable[T2]]:
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
