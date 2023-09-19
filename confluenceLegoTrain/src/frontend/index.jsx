import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Button, Text } from '@forge/react';
import { invoke } from '@forge/bridge';


const App = () => {
  const [data, setData] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    invoke('getText', { example: 'my-invoke-variable' }).then(setData);
  }, []);

  return (
    <>
      <Text>{data ? data : 'Loading...'}</Text>
      <Button appearance='default' onClick={() => invoke('toggleTrainLights')}>Toggle Lights</Button>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
