import Resolver from '@forge/resolver';
import React, { useState } from 'react';
import { fetch } from '@forge/api';

const resolver = new Resolver();

resolver.define('toggleTrainLights', async () => {
  const response = await fetch("https://ca2e-159-196-169-219.ngrok-free.app/lights")
  console.log(response);
  return response;
});

resolver.define('getText', (req) => {
  console.log(req);

  return 'Hello, world!';
});

export const handler = resolver.getDefinitions();
