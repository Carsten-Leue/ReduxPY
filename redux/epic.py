from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from rx import merge, never
from rx.core.typing import Observable

from .types import Action, Epic, PayloadType, ReduxRootState, StateType


def run_epic(
    action_: Observable[Action], state_: Observable[ReduxRootState]
) -> Callable[[Epic], Observable[ReduxRootState]]:
    """ Runs a single epic agains the given action and state observables """
    return lambda epic: epic(action_, state_)


def combine_epics(*epics: Sequence[Epic]) -> Epic:
    """ Combines a sequence of epics into one single epic by merging them """
    return lambda action_, state_: merge(*map(run_epic(action_, state_), epics))
