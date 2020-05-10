"""
    Implements epic specific functions
"""

from inspect import getfullargspec
from typing import Callable, Iterable

from rx import merge
from rx import Observable

from .types import Action, Epic, ReduxRootState


def run_epic(
    action_: Observable, state_: Observable
) -> Callable[[Epic], Observable]:
    """ Runs a single epic agains the given action and state observables

        Args:
            action_: the action observable
            state_: the state observable

        Returns:
            A callback function that will run the given epic on the observables
    """
    args = (action_, state_)

    def dispatch(epic: Epic) -> Observable:
        """ Dispatches to an epic. This method supports epics that
            only use a single action_ observable to support creating
            epics directly from a pipe.

            Args:
                epic: the epic to dispatch to

            Returns:
                the resulting obserable
        """
        count = len(getfullargspec(epic)[0])
        return epic(*args[:count])

    return dispatch


def combine_epics(*epics: Iterable[Epic]) -> Epic:
    """ Combines a sequence of epics into one single epic by merging them

        Args:
            epics: the epics to merge

        Returns:
            The merged epic
    """

    def dispatch(
        action_: Observable, state_: Observable
    ) -> Epic:
        """ Merges the epics into one

            Args:
                action_: the action observable
                state_: the state observable

            Returns:
                the merged epic
        """
        return merge(*map(run_epic(action_, state_), epics))

    return dispatch
