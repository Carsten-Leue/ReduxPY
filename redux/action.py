from typing import Any, Callable, Generic, Optional, Tuple, TypeVar, Union

from rx.core.typing import Observable
from rx.operators import filter

from .types import Action, PayloadType


def create_action(ty: str) -> Callable[[PayloadType], Action[PayloadType]]:
    """ Action creator """
    return lambda payload: (ty, payload)


def select_action_type(action: Action) -> str:
    """ selects the type from the action """
    return action[0]


def select_action_payload(action: Action[PayloadType]) -> PayloadType:
    """ selects the payload from the action """
    return action[1]


def is_type(id: str) -> Callable[[Action], bool]:
    """ Returns a function that checks if the action is of a particular type """
    return lambda action: select_action_type(action) is id


of_type: Callable[
    [str], Callable[[Observable[Action]], Observable[Action]]
] = lambda id: filter(is_type(id))
