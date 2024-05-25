import * as React from 'react';
import { Object3D } from 'three';
import { Falsey } from 'utility-types';
type Helper = Object3D & {
    update: () => void;
    dispose: () => void;
};
type Constructor = new (...args: any[]) => any;
type Rest<T> = T extends [infer _, ...infer R] ? R : never;
export declare function useHelper<T extends Constructor>(object3D: React.MutableRefObject<Object3D> | Falsey, helperConstructor: T, ...args: Rest<ConstructorParameters<T>>): React.MutableRefObject<Helper | undefined>;
export {};
