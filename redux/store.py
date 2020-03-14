"""
    Basic implementation of the store
"""

from typing import Any, Callable, Dict, Mapping, Optional, Sequence

from rx import merge
from rx.core.typing import Observable
from rx.operators import (
    distinct,
    do_action,
    filter,
    flat_map,
    ignore_elements,
    map,
    scan,
    share,
    take_until,
)
from rx.subject import BehaviorSubject, Subject

from .action import create_action
from .constants import INIT_ACTION
from .epic import run_epic
from .reducer import combine_reducers
from .types import (
    Action,
    Epic,
    Reducer,
    ReduxFeatureModule,
    ReduxRootState,
    ReduxRootStore,
    StateType,
)

init_feature_action = create_action(INIT_ACTION)


def select_id(module: ReduxFeatureModule) -> str:
    """ Selects the ID from a module

        Args:
            module: the module
        
        Returns:
            The module identifier
    """
    return module[0]


def select_dependencies(module: ReduxFeatureModule) -> Sequence[ReduxFeatureModule]:
    """ Selects the dependencies from a module

        Args:
            module: the module
        
        Returns:
            The module dependencies
    """
    return module[3]


def select_reducer(module: ReduxFeatureModule) -> Optional[Reducer]:
    """ Selects the reducer from a module

        Args:
            module: the module
        
        Returns:
            The module reducer
    """
    return module[1]


def select_epic(module: ReduxFeatureModule) -> Optional[Epic]:
    """ Selects the epic from a module

        Args:
            module: the module
        
        Returns:
            The module epic
    """
    return module[2]


def has_reducer(module: ReduxFeatureModule) -> bool:
    """ Tests if a module defines a reducer

        Args:
            module: the module

        Returns:
            True if the module has a reducer, else False

    """
    return bool(select_reducer(module))


def identity_reducer(state: StateType, action: Action) -> Action:
    """ Reducer function that returns the original state
    """
    return state


def reduce_reducers(
    dst: Mapping[str, Reducer], module: ReduxFeatureModule
) -> Mapping[str, Reducer]:
    """ Reduces the reducer on a module into a dictionary

        Args:
            dst: the target dictionary
            module: the module to reduce

        Returns:
            the reduced dictionary

    """
    return {**dst, select_id(module): select_reducer(module)}


def create_store(initial_state: Optional[ReduxRootState] = {}) -> ReduxRootStore:
    """ Constructs a new store that can handle feature modules. 
    
        Args:
            initial_state: optional initial state of the store, will typically be the empty dict

        Returns:
            An implementation of the store
    """

    # current reducer
    reducer = identity_reducer

    def replace_reducer(new_reducer: Reducer) -> None:
        """ Callback that replaces the current reducer

            Args:
                new_reducer: the new reducer
        
        """
        nonlocal reducer
        reducer = new_reducer

    actions = Subject()

    # the shared action observable
    actions_ = actions.pipe(share())

    def _dispatch(action: Action) -> None:
        """ Dispatches an action to the store

            Args:
                action: the action to dispatch
        """
        actions.on_next(action)

    state = BehaviorSubject(initial_state)

    # shutdown trigger
    done_ = Subject()

    # The set of known modules, to avoid cycles and duplicate registration
    modules: Dict[str, ReduxFeatureModule] = {}

    # Sequence of added modules
    module_subject = Subject()

    # Subscribe to the resolved modules
    module_ = module_subject.pipe(distinct(select_id), share())

    # Build the reducers
    reducer_ = module_.pipe(
        filter(has_reducer),
        scan(reduce_reducers, {}),
        map(combine_reducers),
        map(replace_reducer),
    )

    # Build the epic
    epic_ = module_.pipe(map(select_epic), filter(bool))

    # Root epic that combines all of the incoming epics
    def root_epic(
        action_: Observable[Action], state_: Observable[ReduxRootState]
    ) -> Observable[ReduxRootState]:
        """ Implementation of the root epic. If listens for new epics
            to come in and automatically subscribes.

            Args:
                action_: the action observable
                state_: the state observable
            
            Returns
                The observable of resulting actions
        """
        return epic_.pipe(flat_map(run_epic(action_, state_)), map(_dispatch),)

    # notifications about new feature states
    new_module_ = module_.pipe(
        map(select_id), map(init_feature_action), map(_dispatch),
    )

    def _add_feature_module(module: ReduxFeatureModule):
        """ Registers a new feature module 

            Args: 
                module: the new feature module
    
        """
        module_id = select_id(module)
        if not module_id in modules:
            modules[module_id] = module
            for dep in select_dependencies(module):
                _add_feature_module(dep)
            module_subject.on_next(module)

    # all state
    internal_ = merge(root_epic(actions_, state), reducer_, new_module_).pipe(
        ignore_elements()
    )

    def _as_observable() -> Observable[ReduxRootState]:
        """ Returns the state as an observable

            Returns:
                the observable
        """
        return state

    def _on_complete() -> None:
        """ Triggers the done event """
        done_.on_next(None)

    merge(actions_, internal_).pipe(
        map(lambda action: reducer(state.value, action)), take_until(done_),
    ).subscribe(state)

    class ReduxRootStoreImpl(ReduxRootStore):
        """ Implementation of the ReduxRootStore. We use the class
            only as an interface and dispatch to the closure for
            all implementation
        """

        def dispatch(self, action: Action) -> Action:
            return _dispatch(action)

        def as_observable(self) -> Observable[ReduxRootState]:
            return _as_observable()

        def on_next(self, value: Action) -> None:
            _dispatch(value)

        def on_completed(self) -> None:
            _on_complete()

        def on_error(self, error) -> None:
            state.on_error(error)

        def add_feature_module(self, module: ReduxFeatureModule) -> None:
            _add_feature_module(module)

    return ReduxRootStoreImpl()
