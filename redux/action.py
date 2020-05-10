"""
    Implements action specific functions
"""

from typing import Any, Callable

from rx import Observable
from rx.operators import filter

from .types import Action, PayloadType


def create_action(type_name: str) -> Callable[[PayloadType], Action]:
    """ Creates a function that produces an action of the given type

        Args:
            type_name: type of the action

        Returns:
            A function that accepts the action payload and creates the action
    """

    def make_action(payload: PayloadType) -> Action:
        """ Curried function that constructs the final action

            Args:
                payload: payload of the action

            Returns:
                The action object

        """
        return Action(type_name, payload)

    return make_action


def select_action_type(action: Action) -> str:
    """ Selects the type from the action

        Args:
            action: the action object

        Returns:
            the type of the action
    """
    return action.type


def select_action_payload(action: Action) -> PayloadType:
    """ Selects the payload from the action

        Args:
            action: the action object

        Returns:
            the payload of the action
    """
    return action.payload


def is_by_selector(
    value: Any, selector: Callable[[Action], Any]
) -> Callable[[Action], bool]:
    """ Returns a function that checks if the selector on an action equals a particular value

        Args:
            value: the value to compare against
            selector: the selector to use to extract the value from the action

        Returns:
            Function to execute the check against an action
    """

    def check_by_selector(action: Action) -> bool:
        """ Checks if selector on an action matches a value

            Args:
                action: the action object

            Returns:
                true if the selector result of the action matches, else false

        """

        return selector(action) is value

    return check_by_selector


def is_type(type_name) -> Callable[[Action], bool]:
    """ Returns a function that checks if the action is of a particular type

        Args:
            type_name: type of the action to check for

        Returns:
            Function to execute the check against an action
    """

    return is_by_selector(type_name, select_action_type)


def of_type(
        type_name: str) -> Callable[[Observable], Observable]:
    """ Returns an rx operator that filters for actions of the given type

        Args:
            type_name: type of the action to filter for

        Returns:
            The filter operator function
    """
    return filter(is_type(type_name))
