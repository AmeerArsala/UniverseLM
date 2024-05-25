import _extends from '@babel/runtime/helpers/esm/extends';
import * as React from 'react';
import * as THREE from 'three';
import { Line } from './Line.js';

const Edges = /* @__PURE__ */React.forwardRef(({
  threshold = 15,
  ...props
}, fref) => {
  const ref = React.useRef(null);
  React.useImperativeHandle(fref, () => ref.current, []);
  const tmpPoints = React.useMemo(() => [0, 0, 0, 1, 0, 0], []);
  const memoizedGeometry = React.useRef();
  const memoizedThreshold = React.useRef();
  React.useLayoutEffect(() => {
    const parent = ref.current.parent;
    if (parent) {
      const geometry = parent.geometry;
      if (geometry !== memoizedGeometry.current || threshold !== memoizedThreshold.current) {
        memoizedGeometry.current = geometry;
        memoizedThreshold.current = threshold;
        const points = new THREE.EdgesGeometry(geometry, threshold).attributes.position.array;
        ref.current.geometry.setPositions(points);
        ref.current.geometry.attributes.instanceStart.needsUpdate = true;
        ref.current.geometry.attributes.instanceEnd.needsUpdate = true;
        ref.current.computeLineDistances();
      }
    }
  });
  return /*#__PURE__*/React.createElement(Line, _extends({
    segments: true,
    points: tmpPoints,
    ref: ref,
    raycast: () => null
  }, props));
});

export { Edges };
