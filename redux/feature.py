from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from rx import pipe
from rx.core.typing import Observable
from rx.operators import do_action, filter, map, take

from .action import select_action_payload, select_action_type
from .constants import INIT_ACTION
from .types import Action, Epic, Reducer, StateType, ReduxFeatureModule

is_init_feature_action: Callable[[Action], bool] = lambda action: (
    select_action_type(action) is INIT_ACTION
)

def has_payload(payload: Any) -> Callable[[Action], bool]:
    """ Tests if the action payload matches the given payload """
    return lambda action: select_action_payload(action) is payload


def of_init_feature(id: str) -> Callable[[Observable[Action]], Observable[str]]:
    """ Operator to test for the initialization action of a feature """
    is_payload = has_payload(id)
    return pipe(
        filter(is_init_feature_action), filter(is_payload), take(1), map(lambda x: id)
    )


def create_feature_module(
    id: str,
    reducer: Reducer = None,
    epic: Epic = None,
    dependencies: Sequence[ReduxFeatureModule] = [],
) -> ReduxFeatureModule:
    """ Constructs a new feature module descriptor """
    return (id, reducer, epic, dependencies)


def select_feature(
    id: str, initial_state: StateType = None
) -> Callable[[Mapping[str, StateType]], Optional[StateType]]:
    """ Selects a feature state """
    return lambda state: state.get(id, initial_state)
