import { TextureLoader, Texture } from 'three';
import { useThree, useLoader } from '@react-three/fiber';
import { useLayoutEffect, useEffect, useMemo } from 'react';

const IsObject = url => url === Object(url) && !Array.isArray(url) && typeof url !== 'function';
function useTexture(input, onLoad) {
  const gl = useThree(state => state.gl);
  const textures = useLoader(TextureLoader, IsObject(input) ? Object.values(input) : input);
  useLayoutEffect(() => {
    onLoad == null || onLoad(textures);
  }, [onLoad]);

  // https://github.com/mrdoob/three.js/issues/22696
  // Upload the texture to the GPU immediately instead of waiting for the first render
  // NOTE: only available for WebGLRenderer
  useEffect(() => {
    if ('initTexture' in gl) {
      let textureArray = [];
      if (Array.isArray(textures)) {
        textureArray = textures;
      } else if (textures instanceof Texture) {
        textureArray = [textures];
      } else if (IsObject(textures)) {
        textureArray = Object.values(textures);
      }
      textureArray.forEach(texture => {
        if (texture instanceof Texture) {
          gl.initTexture(texture);
        }
      });
    }
  }, [gl, textures]);
  const mappedTextures = useMemo(() => {
    if (IsObject(input)) {
      const keyed = {};
      let i = 0;
      for (const key in input) keyed[key] = textures[i++];
      return keyed;
    } else {
      return textures;
    }
  }, [input, textures]);
  return mappedTextures;
}
useTexture.preload = url => useLoader.preload(TextureLoader, url);
useTexture.clear = input => useLoader.clear(TextureLoader, input);

export { IsObject, useTexture };
