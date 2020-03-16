# ReduxPY

Implementation of a Redux store with support for adding feature modules, dynamically. The store exposes a reactive API based on [RxPY](https://pypi.org/project/Rx/).

## What is Redux and Why

Complex applications - client or server - often need to maintain state and the more complex the application becomes the harder it is to keep track of that state. The Redux pattern addresses the management of complex state by following the ideas of [Flux](http://facebook.github.io/flux/), [CQRS](https://martinfowler.com/bliki/CQRS.html), and [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html). 

The [basic principle](https://redux.js.org/introduction/three-principles) boils down to:

- **Single source of truth:** The state of your whole application is stored in an object tree within a single store.
- **State is read-only:** The only way to change the state is to emit an action, an object describing what happened.
- **Changes are made with pure functions:** To specify how the state tree is transformed by actions, you write pure reducers.

### The State Tree

All state is kept in a single, read-only dictionary of type `ReaduxRootState`. This state is maintained and managed by the `ReduxRootStore` object that can be created using the `create_store()` method. The store allows to dispatch actions, listen for state changes and add new features.

### Actions

State cannot be changed but we can create new state based on existing state and an [action](https://redux.js.org/basics/actions). The action describes how the current state will be transformed. 

All state transforms are **synchronous** operations and will be executed by a reducer. 

### Reducers

[Reducers](https://redux.js.org/basics/reducers) are pure functions that transform a current state object into a new state object given an action.

### Epics

It is a basic redux principle that all operations that compute new state are executed by synchronous reducers. In order to implement asynchronous operations we introduce the concept of [Epics](https://redux-observable.js.org/). An epic transforms an action into another action or set of actions and this transform may be executed asynchronously. The resulting actions could in turn give rise to new actions via an epic or they could be interpreted by a reducer.

We represent an epic as a [reactive operator](https://rxpy.readthedocs.io/en/latest/operators.html) that transforms an action input sequence (and optionally also a state sequence) into an action otput sequence.

### Feature Module

There should only be one single redux store instance per application. In traditional redux this means that the set of reducers and epics must be known at instantiation time of the store. This makes it hard to compose the overall application from a set of reusable modules.

We introduce the concept of a feature module, motivated by [dynamic modules](https://github.com/microsoft/redux-dynamic-modules) and [feature store](https://ngrx.io/guide/schematics/feature). 

A feature module defines a unique identifier and optionally a reducer, epic and dependencies. The identifier is used to scope state in a top level dictionary and it is possible to add a new feature module to an existing store at any point in time.



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
