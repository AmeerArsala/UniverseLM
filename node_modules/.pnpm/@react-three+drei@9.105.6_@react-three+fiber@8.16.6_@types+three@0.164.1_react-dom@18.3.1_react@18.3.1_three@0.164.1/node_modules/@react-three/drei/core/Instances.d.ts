import * as THREE from 'three';
import * as React from 'react';
import { ReactThreeFiber } from '@react-three/fiber';
import { ForwardRefComponent } from '../helpers/ts-utils';
declare global {
    namespace JSX {
        interface IntrinsicElements {
            positionMesh: ReactThreeFiber.Object3DNode<PositionMesh, typeof PositionMesh>;
        }
    }
}
type Api = {
    getParent: () => React.MutableRefObject<InstancedMesh>;
    subscribe: <T>(ref: React.MutableRefObject<T>) => void;
};
export type InstancesProps = JSX.IntrinsicElements['instancedMesh'] & {
    range?: number;
    limit?: number;
    frames?: number;
};
export type InstanceProps = JSX.IntrinsicElements['positionMesh'] & {
    context?: React.Context<Api>;
};
type InstancedMesh = Omit<THREE.InstancedMesh, 'instanceMatrix' | 'instanceColor'> & {
    instanceMatrix: THREE.InstancedBufferAttribute;
    instanceColor: THREE.InstancedBufferAttribute;
};
declare class PositionMesh extends THREE.Group {
    color: THREE.Color;
    instance: React.MutableRefObject<THREE.InstancedMesh | undefined>;
    instanceKey: React.MutableRefObject<JSX.IntrinsicElements['positionMesh'] | undefined>;
    constructor();
    get geometry(): THREE.BufferGeometry | undefined;
    raycast(raycaster: THREE.Raycaster, intersects: THREE.Intersection[]): void;
}
export declare const Instance: React.ForwardRefExoticComponent<Omit<InstanceProps, "ref"> & React.RefAttributes<unknown>>;
export declare const Instances: ForwardRefComponent<InstancesProps, InstancedMesh>;
export interface MergedProps extends InstancesProps {
    meshes: THREE.Mesh[];
    children: React.ReactNode;
}
export declare const Merged: ForwardRefComponent<any, THREE.Group>;
export {};
