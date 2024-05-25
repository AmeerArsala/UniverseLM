import { GLTFLoader, DRACOLoader, MeshoptDecoder } from 'three-stdlib';
import { useLoader } from '@react-three/fiber';

let dracoLoader = null;
let decoderPath = 'https://www.gstatic.com/draco/versioned/decoders/1.5.5/';
function extensions(useDraco, useMeshopt, extendLoader) {
  return loader => {
    if (extendLoader) {
      extendLoader(loader);
    }
    if (useDraco) {
      if (!dracoLoader) {
        dracoLoader = new DRACOLoader();
      }
      dracoLoader.setDecoderPath(typeof useDraco === 'string' ? useDraco : decoderPath);
      loader.setDRACOLoader(dracoLoader);
    }
    if (useMeshopt) {
      loader.setMeshoptDecoder(typeof MeshoptDecoder === 'function' ? MeshoptDecoder() : MeshoptDecoder);
    }
  };
}
function useGLTF(path, useDraco = true, useMeshOpt = true, extendLoader) {
  return useLoader(GLTFLoader, path, extensions(useDraco, useMeshOpt, extendLoader));
}
useGLTF.preload = (path, useDraco = true, useMeshOpt = true, extendLoader) => useLoader.preload(GLTFLoader, path, extensions(useDraco, useMeshOpt, extendLoader));
useGLTF.clear = input => useLoader.clear(GLTFLoader, input);
useGLTF.setDecoderPath = path => {
  decoderPath = path;
};

export { useGLTF };
