/* Saca todo lo que dice la profesora en la caja magica (engine/magicbox.js)
 * como JSON, para que gen_audio_edge.py lo grabe con Edge TTS.
 *
 *     node tools/magicbox_lineas.js            -> ["linea", ...]
 *
 * El motor no es un modulo: se carga con un window de mentira. */
const path = require('path');
global.window = global;
window.LANG = 'en';
window.T = (en) => en;
window.VOCAB_ART = { get: () => null, base: k => k };
require(path.join(__dirname, '..', 'engine', 'magicbox.js'));
process.stdout.write(JSON.stringify(window.MAGICBOX.lineas()));
