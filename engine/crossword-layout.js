/* Auto-diagramación determinista de crucigramas.
   Entrada: [{word, clue}] — salida: [{word, clue, row, col, dir}] en el MISMO orden.
   La usan engine/index.html y book-builder/book.html: mismo algoritmo ⇒ misma grilla
   en digital y en papel. Si las palabras ya traen row/col/dir, no se usa. */
function layoutCrossword(words) {
  const sorted = [...words].sort((a, b) =>
    b.word.length - a.word.length || (a.word < b.word ? -1 : 1));
  const grid = {};                      // "r,c" -> letra
  const get = (r, c) => grid[r + ',' + c];
  const place = (w, row, col, dir) => {
    [...w.word].forEach((ch, i) => {
      const r = row + (dir === 'down' ? i : 0), c = col + (dir === 'across' ? i : 0);
      grid[r + ',' + c] = ch;
    });
    placements.set(w.word, { row, col, dir });
  };
  const fits = (word, row, col, dir) => {
    const dr = dir === 'down' ? 1 : 0, dc = dir === 'across' ? 1 : 0;
    // celda antes del inicio y después del final: vacías
    if (get(row - dr, col - dc) !== undefined) return false;
    if (get(row + dr * word.length, col + dc * word.length) !== undefined) return false;
    let crosses = 0;
    for (let i = 0; i < word.length; i++) {
      const r = row + dr * i, c = col + dc * i, ch = get(r, c);
      if (ch !== undefined) {
        if (ch !== word[i]) return false;
        crosses++;
      } else {
        // laterales de una celda nueva deben estar vacíos
        if (get(r + dc, c + dr) !== undefined) return false;
        if (get(r - dc, c - dr) !== undefined) return false;
      }
    }
    return crosses > 0;
  };
  const placements = new Map();
  place(sorted[0], 0, 0, 'across');
  for (let k = 1; k < sorted.length; k++) {
    const w = sorted[k];
    let done = false;
    // recorrer las palabras ya colocadas en orden determinista
    for (const prev of sorted.slice(0, k)) {
      const p = placements.get(prev.word);
      if (!p) continue;
      for (let j = 0; j < prev.word.length && !done; j++) {
        for (let i = 0; i < w.word.length && !done; i++) {
          if (prev.word[j] !== w.word[i]) continue;
          const jr = p.row + (p.dir === 'down' ? j : 0);
          const jc = p.col + (p.dir === 'across' ? j : 0);
          const dir = p.dir === 'across' ? 'down' : 'across';
          const row = dir === 'down' ? jr - i : jr;
          const col = dir === 'across' ? jc - i : jc;
          if (fits(w.word, row, col, dir)) { place(w, row, col, dir); done = true; }
        }
      }
      if (done) break;
    }
    if (!done) {
      // sin cruce posible: fila aparte debajo de todo
      let maxR = 0;
      Object.keys(grid).forEach(k2 => { maxR = Math.max(maxR, +k2.split(',')[0]); });
      place(w, maxR + 2, 0, 'across');
    }
  }
  // normalizar a origen 0,0
  let minR = Infinity, minC = Infinity;
  placements.forEach(p => { minR = Math.min(minR, p.row); minC = Math.min(minC, p.col); });
  return words.map(w => {
    const p = placements.get(w.word);
    return { ...w, row: p.row - minR, col: p.col - minC, dir: p.dir };
  });
}
if (typeof module !== 'undefined') module.exports = { layoutCrossword };
