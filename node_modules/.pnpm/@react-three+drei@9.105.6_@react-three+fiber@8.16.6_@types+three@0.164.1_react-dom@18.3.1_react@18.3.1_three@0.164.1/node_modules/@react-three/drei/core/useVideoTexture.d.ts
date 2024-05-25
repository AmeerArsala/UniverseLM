import * as THREE from 'three';
import type { HlsConfig } from 'hls.js';
interface VideoTextureProps extends HTMLVideoElement {
    unsuspend?: 'canplay' | 'canplaythrough' | 'loadstart' | 'loadedmetadata';
    start?: boolean;
    hls?: HLSConfiguration;
}
interface HLSConfiguration {
    hls: HlsConfig;
}
export declare function useVideoTexture(src: string | MediaStream, props?: Partial<VideoTextureProps>): THREE.VideoTexture;
export {};
