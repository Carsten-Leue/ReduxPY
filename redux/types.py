"""
    Type definitions
"""

from typing import Callable, Mapping, Sequence, TypeVar, NamedTuple

from rx.core.typing import Observable

StateType = TypeVar("StateType")

PayloadType = TypeVar("PayloadType")

ReduxRootState = Mapping[str, StateType]

Action = NamedTuple("Action", [("type", str), ("payload", PayloadType)])

Epic = Callable[[Observable[Action], Observable[ReduxRootState]], Observable[Action]]

Reducer = Callable[[StateType, Action], StateType]

ReduxFeatureModule = NamedTuple(
    "ReduxFeatureModule",
    [("id", str), ("reducer", Reducer), ("epic", Epic), ("dependencies", Sequence)],
)

ReduxRootStore = NamedTuple(
    "ReduxRootStore",
    [
        ("as_observable", Callable[[], Observable[ReduxRootState]]),
        ("dispatch", Callable[[Action], Action]),
        ("add_feature_module", Callable[[ReduxFeatureModule], None]),
        ("on_next", Callable[[Action], Action]),
        ("on_completed", Callable[[], None]),
    ],
)

