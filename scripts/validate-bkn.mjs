/**
 * Load bkn/ with @kweaver-ai/bkn. Requires the package on NODE_PATH, e.g.:
 *   NODE_PATH="$(npm root -g)" node scripts/validate-bkn.mjs
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const require = createRequire(import.meta.url);
const root = join(dirname(fileURLToPath(import.meta.url)), '..');

let loadNetwork, allObjects, allRelations;
try {
  ({ loadNetwork, allObjects, allRelations } = require('@kweaver-ai/bkn'));
} catch {
  console.error('Install or set NODE_PATH to global node_modules (npm root -g).');
  process.exit(1);
}

const net = await loadNetwork(join(root, 'bkn'));
console.log('OK object_types:', allObjects(net).length, 'relation_types:', allRelations(net).length);
