""" Module doc """

# Version of ReduxPy package
__version__ = "0.1.4"

from typing import Tuple
from ._internal.store import create_store
from ._internal.action import create_action, select_action_payload, of_type
from ._internal.reducer import handle_actions, combine_reducers
from ._internal.feature import of_init_feature, create_feature_module, select_feature
from ._internal.epic import combine_epics
from ._internal.types import Action, Reducer, Epic, ReduxRootStore, ReduxFeatureModule, StateType
from ._internal.selectors import select

__all__: Tuple[str, ...] = (
    'Action',
    'combine_epics',
    'combine_reducers',
    'create_action',
    'create_feature_module',
    'create_store',
    'Epic',
    'handle_actions',
    'of_init_feature',
    'of_type',
    'Reducer',
    'ReduxFeatureModule',
    'ReduxRootStore',
    'select_action_payload',
    'select_feature',
    'select',
    'StateType',
)
