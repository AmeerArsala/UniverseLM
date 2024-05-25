import * as THREE from 'three';
import { CloneProps } from './Clone';
import { ForwardRefComponent } from '../helpers/ts-utils';
type GltfProps = Omit<JSX.IntrinsicElements['group'], 'children'> & Omit<CloneProps, 'object'> & {
    src: string;
};
export declare const Gltf: ForwardRefComponent<GltfProps, THREE.Object3D>;
export {};
