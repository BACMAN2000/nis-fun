/* El idioma del curso, para todo el motor.
 *
 * index.html no es el unico que pinta texto: el banner de la unidad, la
 * caja magica y las pantallas de nivel tambien, y esos son archivos aparte
 * que se cargan ANTES que el script de la pagina. Si T() naciera alli
 * dentro, estos cuatro no lo verian y se quedarian en ingles —que es
 * exactamente lo que pasaba—, asi que nace aqui y se carga el primero.
 *
 * Sin ?lang=fr no cambia nada: T() devuelve el ingles de siempre.
 */
(function () {
  var lang = 'en';
  try {
    lang = new URLSearchParams(location.search).get('lang') === 'fr' ? 'fr' : 'en';
  } catch (e) {}
  window.LANG = lang;
  window.T = function (en, fr) { return lang === 'fr' ? fr : en; };
})();
