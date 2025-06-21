Capabilities in WASI
What is a capability?

The Wasm language has no syscall instructions or built-in I/O facilities. To let programs interact with the outside world, Wasm programs can be provided with capabilities.

There are two main kinds of capabilities in WASI, link-time capabilities and runtime capabilities.

Link-time capabilities
In short, link-time capabilities are functions that you can import that do things.

They're called link-time capabilities because the exports that satisfy the imports are chosen at link time. And if someone wants to virtualize those capabilities, or attenuate them to provide a restricted functionality, they may use a component that provides the needed exports and link them in instead, also at link time.

Strictly speaking, link-time capabilities in the Wasm component model are instance imports. These imports request an already-instantiated instance. Being already instantiated, the instance already has some capabilities of its own that were granted to it at its own link time.

Link-time capabilities may also be called instantiation-time capabilities, because the linking we're talking about here is the linking that happens as part of instantiation.

When these imports are satisfied by the host, the host doesn't need to literally create a new Wasm instance, but from the perspective of the guest it behaves the same way.

Runtime capabilities
In short, runtime capabilities are [handles] that you can pass around that grant access to resources.

Handles are first-class, so they can flow anywhere at runtime, and they're unforgeable, so they can be used to pass around access to individual resources without exposing other resources.

In programming languages that can't directly manipulate unforgeable references, handles may be exposed to applications in the form of i32 indices into per-component-instance tables, that conceptually hold the real handles, and the bindings take care of the bookkeeping when handles are passed from one instance to another.

How should one decide when to use link-time vs. runtime capabilities?
If you have use cases that need multiple distinct resources live at the same time, and the ability to dynamically distinguish between them, you'll need runtime capabilities. For example, it's common for programs using filesystem to have multiple files open at once, so files need to be exposed as handles.

If you have an API where most use cases will only ever have one resource that gets used, such as a clock API with a "get the time" function where most users will just have one instance of the clock, link-time capabilities can be more convenient to use.

There may eventually be situations where an API has been designed to use link-time capabilities, and someone needs to use it with runtime capabilities. In our clock API example, if someone does wish to have multiple distinct clocks at runtime, they'll want handles. In the future, the component model will hopefully help out here, by adding features to allow component instances to be usable as handles, which would allow link-time capabilities to be used as runtime capabilities.
