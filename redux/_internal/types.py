"""
    Module doc
"""
from typing import (Any, Callable, Iterable, Mapping, NamedTuple, Optional,
                    TypeVar)

from rx import Observable

StateType = TypeVar("StateType")

PayloadType = TypeVar("PayloadType")

ReduxRootState = Mapping[str, StateType]


class Action(NamedTuple):
    """ Action implementation that takes a payload """
    type: str
    payload: Any


Epic = Callable[[Observable, Observable],
                Observable]

Reducer = Callable[[StateType, Action], StateType]


class ReduxFeatureModule(NamedTuple):
    """ Defines the feature module. The ID identifies the section in the state and
        is also used to globally discriminate features.

        After instantiating a feature store the store will fire an initialization action
        for that feature. Use `ofInitFeature` to register for these initialization actions.
    """
    id: str
    reducer: Optional[Reducer]
    epic: Optional[Epic]
    dependencies: Iterable[Any]


class ReduxRootStore(NamedTuple):
    """ Implementation of a store that manages sub-state as features. Features are added
        to the store automatically, when required by the select method.
    """
    as_observable: Callable[[], Observable]
    dispatch: Callable[[Action], None]
    add_feature_module: Callable[[ReduxFeatureModule], None]
    on_next: Callable[[Action], None]
    on_completed: Callable[[], None]
