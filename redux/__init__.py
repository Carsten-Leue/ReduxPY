""" Module doc """

# Version of ReduxPy package
__version__ = "0.0.0"

from .store import create_store
from .action import Action, create_action, select_action_payload, of_type
from .reducer import Reducer, handle_actions
from .feature import of_init_feature, create_feature_module, select_feature
from .epic import Epic, combine_epics
