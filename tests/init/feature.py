from rx import Observable, pipe
from rx.operators import do_action, filter, map

from redux import (
    Epic,
    Reducer,
    ReduxFeatureModule,
    combine_epics,
    create_action,
    create_feature_module,
    handle_actions,
    of_init_feature,
    of_type,
    select_action_payload,
    select_feature,
)

INIT_FEATURE = "INIT_FEATURE"

ADD_SAMPLE_ACTION = "ADD_SAMPLE_ACTION"

add_sample_action = create_action(ADD_SAMPLE_ACTION)

sample_reducer = handle_actions(
    {ADD_SAMPLE_ACTION: lambda state, action: select_action_payload(action)}
)

add_epic: Epic = lambda action_, state_: action_.pipe(
    of_type(ADD_SAMPLE_ACTION),
    do_action(lambda action: print(f"addEpic: {action}")),
    filter(lambda x: False),
)

init_epic: Epic = lambda action_, state_: action_.pipe(
    of_init_feature(INIT_FEATURE), map(lambda x: add_sample_action("init")),
)

sample_epic: Epic = combine_epics(add_epic, init_epic)

init_feature_module: ReduxFeatureModule = create_feature_module(
    INIT_FEATURE, sample_reducer, sample_epic
)

select_init_feature_module = select_feature(INIT_FEATURE)
