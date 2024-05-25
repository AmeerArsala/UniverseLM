import * as React from 'react';
import { useThree, addAfterEffect } from '@react-three/fiber';
import Stats from 'stats-gl';

function StatsGl({
  className,
  parent,
  ...props
}) {
  const gl = useThree(state => state.gl);
  const stats = React.useMemo(() => {
    const stats = new Stats({
      ...props
    });
    stats.init(gl);
    return stats;
  }, [gl]);
  React.useEffect(() => {
    if (stats) {
      const node = parent && parent.current || document.body;
      node == null || node.appendChild(stats.dom);
      if (className) stats.container.classList.add(...className.split(' ').filter(cls => cls));
      const end = addAfterEffect(() => stats.update());
      return () => {
        node == null || node.removeChild(stats.dom);
        end();
      };
    }
  }, [parent, stats, className]);
  return null;
}

export { StatsGl };
