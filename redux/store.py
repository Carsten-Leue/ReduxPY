from typing import Any, Callable, Mapping, Optional, Sequence, List, Dict

from rx import merge, never
from rx.core.typing import Observable
from rx.operators import (
    distinct,
    do_action,
    filter,
    flat_map,
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
)

init_feature_action = create_action(INIT_ACTION)

select_id: Callable[[ReduxFeatureModule], str] = lambda module: module[0]
select_dependencies: Callable[
    [ReduxFeatureModule], Sequence[ReduxFeatureModule]
] = lambda module: module[3]
select_reducer: Callable[[ReduxFeatureModule], Reducer] = lambda module: module[1]
select_epic: Callable[[ReduxFeatureModule], Epic] = lambda module: module[2]

has_reducer: Callable[[ReduxFeatureModule], bool] = lambda module: bool(
    select_reducer(module)
)

is_never = lambda x: False


identity_reducer: Reducer = lambda state, action: state


def create_store(initial_state: Optional[ReduxRootState] = {}) -> ReduxRootStore:
    """ Constructs a new store that can handle feature modules. 
    
        Args:
            initial_state: optional initial state of the store, will typically be the empty dict

        Returns:
            An implementation of the store
    """

    # current reducer
    reducer: List[Reducer] = [identity_reducer]

    def replace_reducer(new_reducer: Reducer) -> None:
        reducer[0] = new_reducer

    actions = Subject()

    actions_ = actions.pipe(
        do_action(lambda a: print("dispatching %s" % (str(a)))), share()
    )

    def _dispatch(action: Action) -> None:
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
        scan(
            lambda all, module: {**all, select_id(module): select_reducer(module)}, {}
        ),
        map(combine_reducers),
        map(replace_reducer),
    )

    # Build the epic
    epic_ = module_.pipe(map(select_epic), filter(bool))

    # Root epic that combines all of the incoming epics
    root_epic: Epic = lambda action_, state_: epic_.pipe(
        flat_map(run_epic(action_, state_)), map(_dispatch),
    )

    # notifications about new feature states
    new_module_ = module_.pipe(
        map(select_id), map(init_feature_action), map(_dispatch),
    )

    def _add_feature_module(module: ReduxFeatureModule):
        """ Registers a new feature module """
        module_id = select_id(module)
        if not module_id in modules:
            modules[module_id] = module
            for dep in select_dependencies(module):
                _add_feature_module(dep)
            module_subject.on_next(module)

    #: all state
    internal_ = merge(root_epic(actions_, state), reducer_, new_module_).pipe(
        filter(is_never)
    )

    def _as_observable() -> Observable:
        return state

    _on_next = _dispatch
    _on_complete = lambda: done_.on_next(None)

    merge(actions_, internal_).pipe(
        map(lambda action: reducer[0](state.value, action)), take_until(done_),
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
            _on_next(value)

        def on_completed(self) -> None:
            _on_complete()

        def on_error(self, error) -> None:
            pass

        def add_feature_module(self, module: ReduxFeatureModule) -> None:
            _add_feature_module(module)

    return ReduxRootStoreImpl()
