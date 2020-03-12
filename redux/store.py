from rx.subject import BehaviorSubject, Subject
from rx.scheduler import TrampolineScheduler
from rx import Observable, never, merge
from rx.operators import map, distinct, share, take_until, filter, scan, flat_map, observe_on

class ActionTypes(object):
    INIT = '@@redux/INIT',
    INIT_FEATURE: '@@redux/INIT_FEATURE'

class ReduxRootStoreDict(dict):
    def as_observable(self) -> Observable:
        return self['as_observable']()
    def dispatch(self, action):
        return self['dispatch'](action)
    def add_feature_module(self, module):
        return self['add_feature_module'](module)

def init_feature_action(id: str):
    return {'type': ActionTypes.INIT_FEATURE, 'payload': id}

select_id = lambda module: module.get('id')
select_reducer = lambda module: module.get('reducer')
select_epic = lambda module: module.get('epic')

has_reducer = lambda module: 'reducer' in module
has_epic = lambda module: 'epic' in module

is_never = lambda: False

def combine_reducers(reducers: dict): 
    pass

def noop_reducer(state, action):
    return state

def create_store(initial_state=None) -> ReduxRootStoreDict:
    # current reducer
    reducer = noop_reducer

    def replace_reducer(new_reducer):
        reducer = new_reducer

    state = BehaviorSubject(initial_state)

    # shutdown trigger in case we need it some time
    done_ = Subject()

    # The set of known modules, to avoid cycles and duplicate registration
    modules = {}

    # Sequence of added modules
    module_subject = Subject();
    
    # Subscribe to the resolved modules
    module_ = module_subject.pipe(
        distinct(select_id),
        share()
    ) 

    # Build the reducers
    reducer_ = module_.pipe(
        filter(has_reducer),
        scan(lambda all, module: {**all, select_id(module) : select_reducer(module)}),
        map(combine_reducers)
    )

    # Build the epic
    epic_ = module_.pipe(
        filter(has_epic),
        map(select_epic)
    )

    # Root epic that combines all of the incoming epics
    def root_epic(action_: Observable) -> Observable: 
        return epic_.pipe(  
            flat_map(lambda epic: epic(action_))
        )

    # changes in the set of reducers
    reducer_added_ = reducer_.pipe(
        map(replace_reducer)
    )

    # notifications about new feature states
    new_module_ = module_.pipe(
        map(select_id),
        map(init_feature_action),
        observe_on(TrampolineScheduler),
        map(dispatch)
    )

    # all state
    internal_ = merge(reducer_added_, new_module_).pipe(filter(is_never))

    actions_ = Subject()
       
    def dispatch(action):
        actions_.on_next()

    def as_observable() -> Observable:
        return state

    def add_feature_module(module):
        pass

    merge(root_epic(actions_), actions_).pipe(
        map(lambda action: reducer(state.value, action))
    ).subscribe(state)

    dispatch({'type': ActionTypes.INIT})        

    return ReduxRootStoreDict(
        dispatch=dispatch,
        add_feature_module=add_feature_module,
        as_observable=as_observable
    )