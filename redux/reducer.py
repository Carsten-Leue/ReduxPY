from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from .action import select_action_type
from .types import Action, PayloadType, Reducer, StateType


def default_reducer(initial_state: Optional[StateType]) -> Reducer:
    """ Creates a reducer that returns the original state or the default state. """
    return lambda state, action: state if state else initial_state


def handle_actions(
    action_map: Mapping[str, Reducer[StateType, PayloadType]],
    initial_state: Optional[StateType] = None,
) -> Reducer:
    """ Creates a new reducer from a mapping of action name to reducer for that action. """
    def_reducer = default_reducer(initial_state)
    return lambda state, action: action_map.get(
        select_action_type(action), def_reducer
    )(state, action)


def combine_reducers(reducers: Mapping[str, Reducer]) -> Reducer:
    """ Creates a new reducer from a mapping of reducers. """
    items = reducers.items()

    def combine(state: Dict[str, StateType], action: Action) -> Mapping[str, StateType]:
        """ Updates the state object from the reducer mappings. """
        result = state
        for key, value in items:
            current = state.get(key)
            updated = value(current, action)
            if not current is updated:
                if result is state:
                    result = dict(state)
                result[key] = updated
        return result

    return combine
