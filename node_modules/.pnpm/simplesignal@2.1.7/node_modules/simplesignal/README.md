# Simple Signal

[![npm](https://img.shields.io/npm/v/simplesignal.svg)](https://www.npmjs.com/package/simplesignal)
[![Build Status](https://travis-ci.org/zeh/simplesignal.svg?branch=master)](https://travis-ci.org/zeh/simplesignal)
[![Coverage Status](https://coveralls.io/repos/github/zeh/simplesignal/badge.svg?branch=master)](https://coveralls.io/github/zeh/simplesignal?branch=master)
[![Dependency Status](https://david-dm.org/zeh/simplesignal.svg)](https://david-dm.org/zeh/simplesignal)

This is a super-simple signals class inspired by [Robert Penner's AS3Signals](http://github.com/robertpenner/as3-signals).

Signals are like *Events*, *Delegates*, or *Callbacks* on other languages or platforms. You can create a signal that other parts of the code can "listen" to. When that signal is *dispatched*, all listeners are called with the passed parameters.

SimpleSignal is created with TypeScript, but aimed to be used as a standard JavaScript library.

## Install


```shell
npm install simplesignal
```

## Usage

First, import your signal:

```javascript
// Import (JavaScript ES5)
var SimpleSignal = require('simplesignal').default;

// Import (JavaScript ES6 and TypeScript)
import SimpleSignal from 'simplesignal';
```

Then, you can create a signal. For example, inside a class:

```javascript
public onSomethingHappened = new SimpleSignal();
```

Then other parts of the code can subscribe (listen) to that signal:

```javascript
myClassObject.onSomethingHappened.add(function(id) {
    console.log("Something happened with an id of " + id
});
```

Signals can then be dispatched with parameters:

```javascript
onSomethingHappened.dispatch("some-id");
```

This will call all subscribed functions with the given parameter.

## Full reference (JS)

```javascript
// Create
onSomethingHappened = new SimpleSignal();

// Subscribe
onSomethingHappened.add(myFunc);

// Anonymous functions are, of course, fine
onSomethingHappened.add(function() { ... });
onSomethingHappened.add(() => { ... });

// Unsubscribe
onSomethingHappened.remove(myFunc);

// Clear subscribers
onSomethingHappened.removeAll();

// Number of subscribers
console.log(onSomethingHappened.numItems);

// Dispatch
onSomethingHappened.dispatch(...args)
```

## Additional TypeScript reference

If your project already uses TypeScript, it has the advantage of using SimpleSignal's definition files for strict typing.

In this case, one can use a generic interface to enforce the correct dispatch/listener parameters:

```javascript
// Create, with a given interface as a Generic
onSomethingHappened = new SimpleSignal<(action:string) => void>();

// The listeners must fulfill the interface
function myFunc(action:string) {
    console.log(action);
}

// Subscribe
onSomethingHappened.add(myFunc);

// Dispatch must also respect the interface
onSomethingHappened.dispatch("some-action")
```

## License

[MIT](LICENSE.md).