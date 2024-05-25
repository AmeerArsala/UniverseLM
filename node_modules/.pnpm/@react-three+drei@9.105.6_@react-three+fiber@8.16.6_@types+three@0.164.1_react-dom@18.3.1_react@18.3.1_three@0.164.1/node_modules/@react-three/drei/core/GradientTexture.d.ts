import * as React from 'react';
export declare enum GradientType {
    Linear = "linear",
    Radial = "radial"
}
type Props = {
    stops: Array<number>;
    colors: Array<string>;
    attach?: string;
    size?: number;
    width?: number;
    type?: GradientType;
    innerCircleRadius?: number;
    outerCircleRadius?: string | number;
} & JSX.IntrinsicElements['texture'];
export declare function GradientTexture({ stops, colors, size, width, type, innerCircleRadius, outerCircleRadius, ...props }: Props): React.JSX.Element;
export {};
