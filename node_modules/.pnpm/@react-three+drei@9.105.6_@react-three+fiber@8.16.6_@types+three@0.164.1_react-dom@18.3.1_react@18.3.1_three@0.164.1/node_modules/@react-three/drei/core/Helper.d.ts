import * as React from 'react';
import { Object3D } from 'three';
type HelperType = Object3D & {
    update: () => void;
    dispose: () => void;
};
type HelperConstructor = new (...args: any[]) => HelperType;
type HelperArgs<T> = T extends [infer _, ...infer R] ? R : never;
export type HelperProps<T extends HelperConstructor> = {
    type: T;
    args?: HelperArgs<ConstructorParameters<T>>;
};
export declare const Helper: <T extends HelperConstructor>({ type: helperConstructor, args, }: HelperProps<T>) => React.JSX.Element;
export {};
