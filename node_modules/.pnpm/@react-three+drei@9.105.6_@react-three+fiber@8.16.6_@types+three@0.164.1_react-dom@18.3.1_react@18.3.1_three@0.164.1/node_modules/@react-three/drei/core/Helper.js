import { useThree, useFrame } from '@react-three/fiber';
import * as React from 'react';

const Helper = ({
  type: helperConstructor,
  args = []
}) => {
  const objectRef = React.useRef(null);
  const helperRef = React.useRef();
  const scene = useThree(state => state.scene);
  React.useLayoutEffect(() => {
    var _objectRef$current;
    const parent = (_objectRef$current = objectRef.current) == null ? void 0 : _objectRef$current.parent;
    if (!helperConstructor || !parent) return;
    const helper = new helperConstructor(parent, ...args);
    helperRef.current = helper;

    // Prevent the helpers from blocking rays
    helper.traverse(child => child.raycast = () => null);
    scene.add(helper);
    return () => {
      helperRef.current = undefined;
      scene.remove(helper);
      helper.dispose == null || helper.dispose();
    };
  }, [scene, helperConstructor, ...args]);
  useFrame(() => {
    var _helperRef$current;
    return void ((_helperRef$current = helperRef.current) == null || _helperRef$current.update == null ? void 0 : _helperRef$current.update());
  });
  return /*#__PURE__*/React.createElement("object3D", {
    ref: objectRef
  });
};

export { Helper };
