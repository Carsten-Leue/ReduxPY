"""
    Implements epic specific functions
"""

from functools import partial
from inspect import getfullargspec
from logging import getLogger
from typing import Iterable, cast

from rx import merge
from rx.core import Observable
from rx.core.typing import Mapper

from .types import Epic

logger = getLogger(__name__)


def _wrapped_epic(epic: Mapper[Observable, Observable],
                  action_: Observable, _: Observable) -> Observable:
    return epic(action_)


def normalize_epic(epic: Epic) -> Epic:
    """Creates a callback for an epic that expects two arguments

    Args:
        epic: the epic

    Returns:
        the normalized epic
    """
    count = len(getfullargspec(epic)[0])
    assert count in (1, 2)
    return epic if count == 2 else cast(Epic, partial(_wrapped_epic, epic))


def run_epic(action_: Observable, state_: Observable) -> Mapper[Epic, Observable]:
    """ Runs a single epic agains the given action and state observables

        Args:
            action_: the action observable
            state_: the state observable

        Returns:
            A callback function that will run the given epic on the observables
    """

    assert isinstance(action_, Observable)
    assert isinstance(state_, Observable)

    def _dispatch(epic: Epic) -> Observable:
        return epic(action_, state_)

    return _dispatch


def combine_epics(*epics: Iterable[Epic]) -> Epic:
    """ Combines a sequence of epics into one single epic by merging them

        Args:
            epics: the epics to merge

        Returns:
            The merged epic
    """
    norm_epics: Iterable[Epic] = tuple(map(normalize_epic, epics))

    def _dispatch(
        action_: Observable, state_: Observable
    ) -> Observable:
        """ Merges the epics into one

            Args:
                action_: the action observable
                state_: the state observable

            Returns:
                the merged epic
        """
        return merge(*map(run_epic(action_, state_), norm_epics))

    return _dispatch
