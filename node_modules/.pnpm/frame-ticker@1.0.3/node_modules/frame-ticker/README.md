# FrameTicker

[![npm](https://img.shields.io/npm/v/frame-ticker.svg)](https://www.npmjs.com/package/frame-ticker)
[![Build Status](https://travis-ci.org/zeh/frame-ticker.svg?branch=master)](https://travis-ci.org/zeh/frame-ticker)
[![Coverage Status](https://coveralls.io/repos/github/zeh/frame-ticker/badge.svg?branch=master)](https://coveralls.io/github/zeh/frame-ticker?branch=master)
[![Dependency Status](https://david-dm.org/zeh/frame-ticker.svg)](https://david-dm.org/zeh/frame-ticker)

FrameTicker creates an object that continuously loops ("ticks") on every rendering frame, dispatching callbacks every time it does so.

It works on top of `requestAnimationFrame`, but with features of its own. It does not provide a polyfill for browsers that don't support `requestAnimationFrame`.

FrameTicker is written in TypeScript, but can be used both in JavaScript and TypeScript. In TypeScript, you get the benefit of automatic declarations (auto-completion, "intellisense").

## Installation

Simply install FrameTicker as a module dependency using NPM:

```shell
npm install frame-ticker --save
```

## Usage

Import:

```javascript
// Import (JavaScript ES5)
var FrameTicker = require('frame-ticker').default;

// Import (JavaScript ES6 and TypeScript)
import FrameTicker from 'frame-ticker';
```

Create an instance:

```javascript
let ticker = new FrameTicker(); // Create and start, at current browser FPS (60)
let ticker = new FrameTicker(30); // Create at 30fps and start
let ticker = new FrameTicker(30, 15); // Create at 30fps, but with a minimum of 15 calls per second, and start
let ticker = new FrameTicker(NaN, NaN, true); // Creates at paused state
```

Then, add callbacks using [simplesignal](https://www.npmjs.com/package/simplesignal) events:

```javascript
looper.onTick.add((timeSeconds, tickDeltaSeconds, currentFrame) => {
	console.log(`Executing for ${timeSeconds} seconds, delta since last tick is ${tickDeltaSeconds}, current frame is ${currentFrame}.`);
});
```

A typical implementation in games is moving things at a certain speed per seconds. Example:

```javascript
private function onTick(currentTimeSeconds:number, tickDeltaTimeSeconds:number, currentTick:number):void {
    let speed = 10; // Speed of the box, in pixels per seconds
    box.x += speed * tickDeltaTimeSeconds;
}

looper.onTick.add(onTick);
```

You can also pause/resume the looper to pause/resume the game loop:

```typescript
looper.pause();
looper.resume();
```

Ot change the time scale to make time go "faster" (reflected in `timeSeconds` and `tickDeltaSeconds`):

```typescript
looper.timeScale = 2; // 2x original speed (faster motion)
looper.timeScale = 0.5; // 0.5x original speed (slower motion)
```

When the `maxFPS` parameter is used, the looper is not dispatched more that number of times per second:

```typescript
// Max 30 fps dispatching; will only fire once every other visual frame on a 60fps browser
let looper = new FrameTicker(30);
```

When the `minFPS` parameter is used, the looper is always dispatched at least that amount of times per second, regardless of the number of frames:

```typescript
// Max 120 fps dispatching; will fire twice per visual frame on a 60fps browser
let looper = new FrameTicker(NaN, 120);
```

## Full reference

### `new FrameTicker(maxFPS:number = NaN, minFPS:number = NaN, paused:boolean = false):FrameTicker`

Generate a new FrameTicker instance.

Parameters:

* `maxFPS`: Desired maximum framerate. Cause `onTick` calls to be skipped if the desired maximum framerate is lower than the current environment maximum. `NaN` means no maximum.
* `minFPS`: Desired minimum framerate. Cause `onTick` calls to be repeated more than once per frame if the desired minimum framerate is higher than the current environment maximum. Careful when using this, since it can create performance problems in low-performance situations; it can't magically makes thing faster. `NaN` means no minimum.
* `paused`: Whether it's paused at start or not.

Return:

* A new `FrameTicker` instance.


### `updateOnce(callback:(timeSeconds:number, tickDeltaSeconds:number, currentFrame:number) => void)`

### `resume()`
### `pause()`
### `dispose()`
### `currentTick:number`
### `currentTimeSeconds:number`
### `tickDeltaTimeSeconds:number`
### `timeScale:number`
### `onResume:SimpleSignal`

Can use `.add(f)`, `.resume(f)`, `.removeAll`

### `onPause:SimpleSignal`
### `onTick:SimpleSignal`
### `onTickOncePerFrame:SimpleSignal`



## License

[MIT](LICENSE.md).