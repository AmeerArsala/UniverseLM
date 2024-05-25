import { Texture } from 'three';
import * as React from 'react';
import { CubeCameraOptions } from './useCubeCamera';
type Props = Omit<JSX.IntrinsicElements['group'], 'children'> & {
    children: (tex: Texture) => React.ReactNode;
    frames?: number;
} & CubeCameraOptions;
export declare function CubeCamera({ children, frames, resolution, near, far, envMap, fog, ...props }: Props): React.JSX.Element;
export {};
