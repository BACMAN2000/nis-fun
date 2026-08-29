    //
    // Con casillas y desplegables basta con vaciar valor y clase. Las
    // actividades cuya respuesta es un BOTON pasan su propia limpia(): a un
    // boton no se le puede borrar la clase entera, porque ahi va la suya.
    if (cfg.limpia) cfg.limpia();
    else cfg.entradas().forEach(i => { i.value = ''; i.className = ''; });