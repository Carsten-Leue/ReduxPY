"""
    Type definitions
"""

from abc import ABC, abstractmethod
from typing import Callable, Mapping, Sequence, Tuple, TypeVar

from rx.core.typing import Observable, Observer

StateType = TypeVar("StateType")

PayloadType = TypeVar("PayloadType")

ReduxRootState = Mapping[str, StateType]

Action = Tuple[str, PayloadType]

Epic = Callable[[Observable[Action], Observable[ReduxRootState]], Observable[Action]]

Reducer = Callable[[StateType, Action[PayloadType]], StateType]

ReduxFeatureModule = Tuple[str, Reducer, Epic, Sequence]


class AbstractReduxRootStore(ABC):
    """ReduxRootStore abstract base class. Untyped."""

    @abstractmethod
    def as_observable(self):
        raise NotImplementedError

    @abstractmethod
    def dispatch(self, action):
        raise NotImplementedError

    @abstractmethod
    def add_feature_module(self, module):
        raise NotImplementedError


class ReduxRootStore(AbstractReduxRootStore, Observer[Action]):
    """ReduxRootStore abstract base class."""

    @abstractmethod
    def as_observable(self) -> Observable[ReduxRootState]:
        """ Returns the state as an observable

        Returns:
            The observable version of the store
        """

        return NotImplemented

    @abstractmethod
    def dispatch(self, action: Action) -> Action:
        """ Dispatches an action. It is the only way to trigger a state change.
    
        The `reducer` function, used to create the store, will be called with the
        current state tree and the given `action`. Its return value will be
        considered the **next** state of the tree, and the change listeners will
        be notified.

        Args:
            action: A tuple representing “what changed”. The first element in the tuple
                    is considered to be the identifier of the action, the second element
                    is the action payload

        Returns:
            The same action as was passed in
        """

        return NotImplemented

    @abstractmethod
    def add_feature_module(self, module: ReduxFeatureModule) -> None:
        """ Registers a feature module with the root store

        Args:
            module: the feature model

        """

        return NotImplemented
