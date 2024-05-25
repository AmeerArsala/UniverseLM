import { Texture } from 'three';
export declare const IsObject: (url: unknown) => url is Record<string, string>;
type TextureArray<T> = T extends string[] ? Texture[] : never;
type TextureRecord<T> = T extends Record<string, string> ? {
    [key in keyof T]: Texture;
} : never;
type SingleTexture<T> = T extends string ? Texture : never;
export type MappedTextureType<T extends string[] | string | Record<string, string>> = TextureArray<T> | TextureRecord<T> | SingleTexture<T>;
export declare function useTexture<Url extends string[] | string | Record<string, string>>(input: Url, onLoad?: (texture: MappedTextureType<Url>) => void): MappedTextureType<Url>;
export declare namespace useTexture {
    var preload: (url: string | string[]) => undefined;
    var clear: (input: string | string[]) => void;
}
export {};
