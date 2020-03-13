# ReduxPY

Implementation of a Redux store with support for adding feature modules, dynamically. The store exposes a reactive API based on [RxPY](https://pypi.org/project/Rx/).

## Providing a feature module

Create and export an instance of `ReduxFeatureModule` for your module. The module definition consists of:

* a unique module identifier. This identifier is also used as a namespace in the redux state
* an optional reducer that operates on that namespace
* an optional epic to handle asynchronous actions
* an optional list of other feature modules this module depends on

### Example

```python
from redux import create_feature_module, ReduxFeatureModule

sample_feature_module: ReduxFeatureModule = create_feature_module(
    'SAMPLE_FEATURE', sample_reducer, sample_epic, [dep1, dep2]
)
```

## Registering a feature module

Register the feature module with the root store using the `add_feature_module` method. This will also register all dependent modules in topology order.

```python
from redux import create_store, ReduxRootStore

store: ReduxRootStore = create_store()
store.add_feature_module(sampleFeature)
```

## Consuming a feature module

Use the `select_feature` method to create a selector for the desired feature.

### Example

```python
from redux import select_feature

select_sample = select_feature(sample_feature)
```

## Side effects in Feature Modules

Feature modules may provide side effects, aka epics, for asynchronous processing. Sometimes such epics require an initialization event to execute bootstrapping logic. The store sends an initialization event for this purpose, after a feature module has been initialized. Use the `of_init_feature` method to subscribe to this event.

### Example

```python
from redux import of_init_feature, Epic
from rx.operators import map

initEpic: Epic = lambda actions_, state_: actions_.pipe(of_init_feature(sample_feature), map(...))
```
