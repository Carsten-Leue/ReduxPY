from typing import Any
from rx import Observable, pipe
from rx.operators import do_action, filter, map, ignore_elements

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
    StateType,
    Action,
)

INIT_FEATURE = "INIT_FEATURE"

ADD_SAMPLE_ACTION = "ADD_SAMPLE_ACTION"

add_sample_action = create_action(ADD_SAMPLE_ACTION)
select_init_feature_module = select_feature(INIT_FEATURE)


def create_sample_feature() -> ReduxFeatureModule:
    """
        Constructs a new sample feature
    """

    def handle_sample_action(state: Any, action: Action) -> Any:
        return select_action_payload(action)

    sample_reducer = handle_actions({ADD_SAMPLE_ACTION: handle_sample_action})

    add_epic = pipe(of_type(ADD_SAMPLE_ACTION), ignore_elements(),)

    init_epic = pipe(
        of_init_feature(INIT_FEATURE), map(lambda x: add_sample_action("init")),
    )

    sample_epic = combine_epics(add_epic, init_epic)

    return create_feature_module(INIT_FEATURE, sample_reducer, sample_epic)

