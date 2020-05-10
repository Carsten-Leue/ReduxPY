""" Module doc """

# Version of ReduxPy package
__version__ = "0.1.0"

from .store import create_store
from .action import create_action, select_action_payload, of_type
from .reducer import handle_actions
from .feature import of_init_feature, create_feature_module, select_feature
from .epic import combine_epics
from .types import Action, Reducer, Epic, ReduxRootStore, ReduxFeatureModule, StateType
from .selectors import select
