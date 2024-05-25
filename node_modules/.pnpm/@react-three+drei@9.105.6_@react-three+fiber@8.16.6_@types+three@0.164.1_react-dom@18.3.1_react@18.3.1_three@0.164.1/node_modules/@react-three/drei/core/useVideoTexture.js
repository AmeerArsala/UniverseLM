import * as THREE from 'three';
import { useRef, useEffect } from 'react';
import { useThree } from '@react-three/fiber';
import { suspend } from 'suspend-react';

var _window$document, _window$navigator;
const IS_BROWSER = typeof window !== 'undefined' && typeof ((_window$document = window.document) == null ? void 0 : _window$document.createElement) === 'function' && typeof ((_window$navigator = window.navigator) == null ? void 0 : _window$navigator.userAgent) === 'string';
let _HLSModule = null;
async function getHLS(url, config) {
  if (IS_BROWSER && url.pathname.endsWith('.m3u8')) {
    var _HLSModule2;
    (_HLSModule2 = _HLSModule) !== null && _HLSModule2 !== void 0 ? _HLSModule2 : _HLSModule = await import('hls.js');
    if (_HLSModule.default.isSupported()) {
      return new _HLSModule.default({
        ...config
      });
    }
  }
  return null;
}
function useVideoTexture(src, props) {
  const {
    unsuspend,
    start,
    crossOrigin,
    muted,
    loop,
    hls,
    ...rest
  } = {
    unsuspend: 'loadedmetadata',
    crossOrigin: 'Anonymous',
    muted: true,
    loop: true,
    start: true,
    playsInline: true,
    hls: {},
    ...props
  };
  const url = new URL(typeof src === 'string' ? src : '', window.location.href);
  const hlsRef = useRef(null);
  const videoRef = useRef(null);
  const gl = useThree(state => state.gl);
  const texture = suspend(() => new Promise(async (res, rej) => {
    const video = Object.assign(document.createElement('video'), {
      src: typeof src === 'string' && src || undefined,
      srcObject: src instanceof MediaStream && src || undefined,
      crossOrigin,
      loop,
      muted,
      ...rest
    });
    videoRef.current = video;

    // hlsjs extension
    if (typeof src === 'string') {
      const _hls = hlsRef.current = await getHLS(url, hls);
      if (_hls) {
        _hls.attachMedia(video);
        _hls.on('hlsMediaAttached', () => {
          _hls.loadSource(src);
        });
      } else {
        video.src = src;
      }
    } else if (src instanceof MediaStream) {
      video.srcObject = src;
    }
    const texture = new THREE.VideoTexture(video);
    if ('colorSpace' in texture) texture.colorSpace = gl.outputColorSpace;else texture.encoding = gl.outputEncoding;
    video.addEventListener(unsuspend, () => res(texture));
  }), [src]);
  useEffect(() => {
    start && texture.image.play();
    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
        hlsRef.current = null;
      }
    };
  }, [texture, start]);
  return texture;
}

export { useVideoTexture };
