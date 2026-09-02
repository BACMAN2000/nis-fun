
  /* ---------- las familias, en frances ----------

     No es la traduccion de la tabla inglesa, y no puede serlo: "bigger,
     biggest" no existe en frances (es plus grand, le plus grand), la s de
     he plays no tiene equivalente y el -ly de slowly es -ment. Traducir la
     caja inglesa enseñaria gramatica inglesa con palabras francesas.

     Asi que es OTRA tabla, con las reglas que si son del frances: el genero
     de un/une, el acuerdo del adjetivo, el partitif du/de la/des, el passe
     compose con avoir o con etre. Los dibujos son los mismos porque una
     caja y una pelota no tienen idioma.

     El regex busca en el grammar/topic/title de la unidad FRANCESA, que ya
     esta en frances: por eso son palabras francesas y no las inglesas. */
  const FAMILIAS_FR = [
    {
      id: 'genero',
      busca: /c'est un|c'est une|de quelle couleur|l'alphabet|comment ça s'écrit|les cris des animaux|c'est \/ c'est/i,
      titulo: 'un ou une ?',
      pasos: [
        { arte: () => bolas(1), pal: 'un',  fin: ' ballon', frase: 'Le ballon : un.' },
        { arte: () => bolas(1), pal: 'une', fin: ' pomme',  frase: 'La pomme : une.' },
        { arte: () => bolas(2), pal: 'des', fin: ' ballons', frase: 'Plus d\'un : des.' },
      ],
      pie: 'Chaque mot a son un ou son une. On les apprend ensemble.',
      reto: { p: "C'est ___ maison.", ops: ['un', 'une', 'des'], bien: 1 },
    },
    {
      id: 'pluriel',
      busca: /le pluriel|combien|nombres 11|nombres 20|nombres 1|il y a \+/i,
      titulo: 'Un, ou beaucoup ?',
      pasos: [
        { arte: () => bolas(1), pal: 'un ballon',     fin: '',  frase: 'Il y a un ballon.' },
        { arte: () => bolas(2), pal: 'deux ballon',   fin: 's', frase: 'Il y a deux ballons.' },
        { arte: () => bolas(3), pal: 'trois ballon',  fin: 's', frase: 'Il y a trois ballons !' },
      ],
      pie: 'Plus d\'un ? On ajoute un s… mais on ne l\'entend pas.',
      reto: { p: 'Je vois quatre…', ops: ['chat', 'chats', 'chatses'], bien: 1 },
    },
    {
      id: 'ou',
      busca: /préposition.*lieu|dans, sur|où est|derrière|entre|à côté de|indications|mouvement/i,
      titulo: 'Où est le ballon ?',
      pasos: [
        { arte: () => cajaCon('in'),    pal: 'dans', fin: '',  frase: 'Le ballon est dans la boîte.' },
        { arte: () => cajaCon('on'),    pal: 'sur',  fin: '',  frase: 'Le ballon est sur la boîte.' },
        { arte: () => cajaCon('under'), pal: 'sous', fin: '',  frase: 'Le ballon est sous la boîte.' },
      ],
      pie: 'La boîte ne bouge pas — le ballon, si.',
      reto: { p: 'Le chat dort ___ le lit.', ops: ['dans', 'sur', 'sous'], bien: 1 },
    },
    {
      id: 'savoir',
      busca: /savoir|je sais|il peut|pouvoir|je peux avoir/i,
      titulo: 'Qu\'est-ce que tu sais faire ?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'Je sais',       fin: ' nager', frase: 'Oui ! Je sais le faire.' },
        { arte: () => figura('triste', 'abajo'), pal: 'Je ne sais pas', fin: ' voler', frase: 'Non, je ne sais pas.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Tu sais',        fin: ' chanter ?', frase: 'Demande à un ami !' },
      ],
      pie: 'Pour dire non : ne… pas autour du verbe.',
      reto: { p: 'Un poisson dans la mer…', ops: ['sait nager', 'ne sait pas nager', 'sait voler'], bien: 0 },
    },
    {
      id: 'passe',
      busca: /passé composé|le passé|quand j'étais|imparfait|il y avait|biographies/i,
      titulo: 'Aujourd\'hui et hier',
      pasos: [
        { arte: () => reloj(9), pal: 'je joue',   fin: '',        frase: 'Aujourd\'hui.' },
        { arte: () => reloj(5), pal: 'j\'ai',     fin: ' joué',   frase: 'Hier : avoir + le participe.' },
        { arte: () => reloj(3), pal: 'je suis',   fin: ' allé',   frase: 'Aller, venir, partir : être !' },
      ],
      pie: 'Presque tous avec avoir. Aller et venir, avec être.',
      reto: { p: 'Hier nous ___ au zoo.', ops: ['allons', 'sommes allés', 'avons allé'], bien: 1 },
    },
    {
      id: 'futur',
      busca: /futur/i,
      titulo: 'Demain !',
      pasos: [
        { arte: () => reloj(9),  pal: 'je suis',   fin: ' ici',   frase: 'Maintenant.' },
        { arte: () => reloj(12), pal: 'je vais',   fin: ' partir', frase: 'Demain.' },
        { arte: () => reloj(2),  pal: 'je ne vais pas', fin: ' partir', frase: 'Pas demain !' },
      ],
      pie: 'aller + l\'infinitif : c\'est le futur proche.',
      reto: { p: 'Demain il ___ pleuvoir.', ops: ['va', 'était', 'allé'], bien: 0 },
    },
    {
      id: 'maintenant',
      busca: /en ce moment|maintenant|en train de|présent \(/i,
      titulo: 'En ce moment !',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je cours',            fin: '',           frase: 'Tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je suis en train de', fin: ' courir',    frase: 'Juste maintenant !' },
        { arte: () => figura('feliz', 'arriba'), pal: 'elle est en train de', fin: ' courir',   frase: 'Regarde-la !' },
      ],
      pie: 'Le français dit le même verbe — être en train de, c\'est pour insister.',
      reto: { p: 'Regarde ! Pip ___ .', ops: ['vole', 'voler', 'volé'], bien: 0 },
    },
    {
      id: 'avoir',
      busca: /^avoir|avoir \/|avoir \+|possessif|à qui|le mien|tu as|j'ai|voici mon/i,
      titulo: 'C\'est à qui ?',
      pasos: [
        { arte: () => caja(76, '#e8c49a'), pal: 'j\'ai',      fin: ' une boîte',  frase: 'C\'est la mienne.' },
        { arte: () => caja(76, '#d8b0d0'), pal: 'elle a',     fin: ' une boîte',  frase: 'C\'est sa boîte.' },
        { arte: () => caja(76, '#a8d0e8'), pal: 'ils ont',    fin: ' des boîtes', frase: 'Ce sont les leurs.' },
      ],
      pie: 'j\'ai, tu as, il a, nous avons, vous avez, ils ont.',
      reto: { p: 'Nico ___ un cerf-volant rouge.', ops: ['ai', 'a', 'as'], bien: 1 },
    },
    {
      id: 'routine',
      busca: /3e personne|les routines|d'habitude|toujours|souvent|le présent \+|le présent,|le présent :/i,
      titulo: 'je, tu, il… le verbe change',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je jou',    fin: 'e',   frase: 'Je joue tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'tu jou',    fin: 'es',  frase: 'Tu joues tous les jours.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'nous jou',  fin: 'ons', frase: 'Nous jouons tous les jours.' },
      ],
      pie: 'La fin du verbe suit la personne. On l\'écrit même si on ne l\'entend pas.',
      reto: { p: 'Pip ___ dans la mer chaque matin.', ops: ['nage', 'nages', 'nageons'], bien: 0 },
    },
    {
      id: 'hora',
      busca: /quelle heure|et quart|et demie|moins le quart|heures pile/i,
      titulo: 'Quelle heure est-il ?',
      pasos: [
        { arte: () => reloj(3), pal: 'trois heures',  fin: '',            frase: 'La grande aiguille est en haut.' },
        { arte: () => reloj(3), pal: 'trois heures',  fin: ' et demie',   frase: 'La grande aiguille est en bas.' },
        { arte: () => reloj(4), pal: 'quatre heures', fin: ' moins le quart', frase: 'Presque quatre heures !' },
      ],
      pie: 'Regarde d\'abord la grande aiguille.',
      reto: { p: 'La grande aiguille est en bas. Il est…', ops: ['quatre heures', 'quatre heures et demie', 'quatre heures moins le quart'], bien: 1 },
    },
    {
      id: 'cuando',
      busca: /en \+ mois|le \+ jour|les dates|saison|le matin \/ la nuit|quel âge|quand/i,
      titulo: 'en, le, à — quand ?',
      pasos: [
        { arte: () => reloj(12), pal: 'en', fin: ' juillet',   frase: 'Un mois entier.' },
        { arte: () => reloj(9),  pal: 'le', fin: ' lundi',     frase: 'Tous les lundis.' },
        { arte: () => reloj(7),  pal: 'à',  fin: ' sept heures', frase: 'Un moment précis.' },
      ],
      pie: 'Grande durée, jour, instant.',
      reto: { p: 'Mon anniversaire est ___ mai.', ops: ['en', 'le', 'à'], bien: 0 },
    },
    {
      id: 'deja',
      busca: /déjà|vient de|pas encore|ne… jamais|ne jamais/i,
      titulo: 'Déjà fait !',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je mange',      fin: '',            frase: 'Maintenant.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je viens de',   fin: ' manger',     frase: 'Il y a une minute !' },
        { arte: () => figura('triste', 'abajo'), pal: 'je n\'ai pas',  fin: ' encore mangé', frase: 'Pas encore…' },
      ],
      pie: 'venir de = ça vient de finir.',
      reto: { p: 'Kili ___ déjà apporté les lettres.', ops: ['a', 'est', 'va'], bien: 0 },
    },
    {
      id: 'consejo',
      busca: /devrait|devoir|il faut|la sécurité|les règles/i,
      titulo: 'Bonne idée, mauvaise idée',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'tu devrais',       fin: ' dormir', frase: 'Bonne idée !' },
        { arte: () => figura('triste', 'abajo'), pal: 'tu ne devrais pas', fin: ' crier',  frase: 'Pas une bonne idée.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je dois',           fin: ' aider',  frase: 'Là, c\'est obligé.' },
      ],
      pie: 'devrais = un conseil. dois = une obligation.',
      reto: { p: 'Tu es fatigué. Tu ___ aller au lit.', ops: ['devrais', 'ne devrais pas', 'ne peux pas'], bien: 0 },
    },
    {
      id: 'transporte',
      busca: /transport|en \+ véhicule|comment tu vas/i,
      titulo: 'Comment tu y vas ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'en', fin: ' bus',   frase: 'J\'y vais en bus.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'à',  fin: ' vélo',  frase: 'J\'y vais à vélo.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'à',  fin: ' pied',  frase: 'Et à pied aussi !' },
      ],
      pie: 'Dedans : en. Dessus : à.',
      reto: { p: 'Je marche jusqu\'à l\'école. J\'y vais ___ .', ops: ['en pied', 'à pied', 'en marche'], bien: 1 },
    },
    {
      id: 'deporte',
      busca: /jouer à|faire de|sport/i,
      titulo: 'jouer à ou faire de ?',
      pasos: [
        { arte: () => bolas(1),                  pal: 'je joue au',      fin: ' football', frase: 'Les jeux avec un ballon.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je fais de la',   fin: ' natation', frase: 'Les autres sports.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je fais du',      fin: ' judo',     frase: 'du, de la, de l\' — comme le mot.' },
      ],
      pie: 'Un ballon ? jouer à. Sinon ? faire de.',
      reto: { p: 'Samedi je ___ basket.', ops: ['joue au', 'fais au', 'joue de'], bien: 0 },
    },
    {
      id: 'imperativo',
      busca: /impératif|allons|et si on|on pourrait|tu veux/i,
      titulo: 'Fais-le !',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'Ouvre',       fin: ' la boîte !', frase: 'Le verbe tout seul.' },
        { arte: () => figura('triste', 'abajo'), pal: 'N\'ouvre pas', fin: ' la boîte !', frase: 'Pour dire non : ne… pas.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'Ouvrons',     fin: '-la !',      frase: 'Toi et moi ensemble.' },
      ],
      pie: 'Pas de je ni de tu devant — juste le verbe.',
      reto: { p: '___ pas dans le couloir !', ops: ['Ne cours', 'Non cours', 'Pas cours'], bien: 0 },
    },
    {
      id: 'adjetivo',
      busca: /adjectif|décrire|description|personnalité|en \+ matière|quel \+ adjectif/i,
      titulo: 'Comment c\'est ?',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'une grande',    fin: ' boîte',  frase: 'Grand, petit, joli : devant.' },
        { arte: () => caja(70, '#a8d0e8'), pal: 'une boîte',     fin: ' bleue',  frase: 'Les couleurs : derrière.' },
        { arte: () => caja(70, '#d8b0d0'), pal: 'la boîte est',  fin: ' bleue',  frase: 'Une boîte : bleue, avec un e.' },
      ],
      pie: 'L\'adjectif s\'habille comme le mot : bleu, bleue, bleus, bleues.',
      reto: { p: 'Laquelle est correcte ?', ops: ['une boîte rouge', 'une rouge boîte', 'une boîte rouges'], bien: 0 },
    },
    {
      id: 'gustar',
      busca: /aimer|adorer|j'aime/i,
      titulo: 'Oui merci, non merci',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'j\'aime',       fin: ' le gâteau', frase: 'Oui ! 😀' },
        { arte: () => figura('triste', 'abajo'), pal: 'je n\'aime pas', fin: ' le poisson', frase: 'Non… 🙁' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'tu aimes',      fin: ' le gâteau ?', frase: 'Demande à un ami !' },
      ],
      pie: 'Pour dire non, le ne… pas entoure le verbe.',
      reto: { p: 'Luna ___ les chats.', ops: ['n\'aime pas', 'pas aime', 'non aime'], bien: 0 },
    },
    {
      id: 'llevar',
      busca: /porter|emporter|mettre|il fait \+ adjectif/i,
      titulo: 'Qu\'est-ce que tu portes ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'je porte',     fin: ' un chapeau', frase: 'Sur moi, maintenant.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'elle porte',   fin: ' une écharpe', frase: 'Sur elle, maintenant.' },
        { arte: () => caja(66, '#e8c49a'),       pal: 'j\'emporte',   fin: ' un sac',     frase: 'Dans la main, pas sur moi !' },
      ],
      pie: 'Sur le corps ? porter. Dans la main ? emporter.',
      reto: { p: 'Erik ___ un grand sac bleu.', ops: ['porte', 'emporte', 'met'], bien: 1 },
    },
    {
      id: 'soy',
      busca: /je suis|il est|elle est|il s'appelle|un homme|une femme|un garçon/i,
      titulo: 'Qui est qui ?',
      pasos: [
        { arte: () => figura('feliz', 'arriba'), pal: 'je suis',   fin: ' Nico',   frase: 'Moi.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'il est',    fin: ' Nico',   frase: 'Un garçon.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'elle est',  fin: ' Astrid', frase: 'Une fille.' },
      ],
      pie: 'je, il, elle — un petit mot change tout.',
      reto: { p: '___ est ma sœur.', ops: ['Il', 'Elle', 'On'], bien: 1 },
    },
    {
      id: 'porque',
      busca: /parce que|alors|la cause|le résultat/i,
      titulo: 'Pourquoi ? et Alors ?',
      pasos: [
        { arte: () => figura('triste', 'abajo'), pal: 'je suis fatigué', fin: '',              frase: 'Ce qui se passe.' },
        { arte: () => figura('triste', 'abajo'), pal: 'parce que',       fin: ' j\'ai couru',  frase: 'La raison.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'alors',           fin: ' je m\'assois', frase: 'Ce qui arrive après.' },
      ],
      pie: 'parce que regarde en arrière. alors regarde devant.',
      reto: { p: 'Il pleuvait, ___ nous sommes restés à la maison.', ops: ['parce que', 'alors', 'mais'], bien: 1 },
    },
    {
      id: 'relativos',
      busca: /pronoms relatifs|qui, que/i,
      titulo: 'Une phrase, pas deux',
      pasos: [
        { arte: () => figura('feliz', 'abajo'), pal: 'la fille',  fin: ' qui court',    frase: 'qui — celui qui fait.' },
        { arte: () => bolas(1),                 pal: 'le livre',  fin: ' que je lis',   frase: 'que — celui qu\'on fait.' },
        { arte: () => caja(70, '#e8c49a'),      pal: 'la ville',  fin: ' où j\'habite', frase: 'où — pour les lieux.' },
      ],
      pie: 'qui fait, que subit, où situe.',
      reto: { p: 'C\'est le livre ___ j\'ai lu la semaine dernière.', ops: ['qui', 'que', 'où'], bien: 1 },
    },
    {
      id: 'manera',
      busca: /adverbe|bien, vite|-ment/i,
      titulo: 'Comment tu le fais ?',
      pasos: [
        { arte: () => figura('feliz', 'abajo'),  pal: 'lent',   fin: '',      frase: 'Comment c\'est.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'lente',  fin: 'ment',  frase: 'Comment on le fait.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'bien',   fin: '',      frase: 'Celui-là ne prend pas -ment !' },
      ],
      pie: 'On part du féminin : lente → lentement.',
      reto: { p: 'Elle chante très ___ .', ops: ['bon', 'bien', 'bonnement'], bien: 1 },
    },
    {
      id: 'faire',
      busca: /les expressions avec faire|il fait \+ météo|il fait soleil/i,
      titulo: 'Le verbe faire est partout',
      pasos: [
        { arte: () => reloj(12),                 pal: 'il fait',  fin: ' beau',       frase: 'Pour le temps qu\'il fait.' },
        { arte: () => figura('feliz', 'abajo'),  pal: 'je fais',  fin: ' mes devoirs', frase: 'Pour le travail.' },
        { arte: () => figura('feliz', 'arriba'), pal: 'je fais',  fin: ' du vélo',    frase: 'Et pour les sports.' },
      ],
      pie: 'Le temps, le travail, le sport : faire.',
      reto: { p: '___ froid aujourd\'hui.', ops: ['Il fait', 'Il est', 'C\'est'], bien: 0 },
    },
    {
      id: 'partitivo',
      busca: /partitif|du \/ de la|beaucoup de|un peu de|quelques|je prends/i,
      titulo: 'du, de la, des',
      pasos: [
        { arte: () => caja(70, '#e8c49a'), pal: 'du',     fin: ' pain',  frase: 'Le pain : du.' },
        { arte: () => caja(70, '#d8b0d0'), pal: 'de la',  fin: ' soupe', frase: 'La soupe : de la.' },
        { arte: () => bolas(3),            pal: 'des',    fin: ' pommes', frase: 'Plusieurs : des.' },
      ],
      pie: 'Une partie, pas le tout : du, de la, des.',
      reto: { p: 'Je voudrais ___ eau.', ops: ['du', 'de l\'', 'des'], bien: 1 },
    },
    {
      id: 'comparativo',
      busca: /comparatif|superlatif|plus .* que|le plus|le meilleur/i,
      titulo: 'Trois boîtes, trois phrases',
      pasos: [
        { arte: () => caja(64, '#e8c49a'),  pal: 'grande',        fin: '',        frase: 'Cette boîte est grande.' },
        { arte: () => caja(92, '#e0b784'),  pal: 'plus',          fin: ' grande', frase: 'Celle-là est plus grande !' },
        { arte: () => caja(124, '#d8a96c'), pal: 'la plus',       fin: ' grande', frase: 'Et celle-là est la plus grande !' },
      ],
      pie: 'plus… que pour comparer, le plus… pour gagner.',
      reto: { p: 'Cette boîte est ___ des trois.', ops: ['grande', 'plus grande', 'la plus grande'], bien: 2 },
    },
    {
      id: 'si',
      busca: /si \+ présent|quand \+ présent|peut-être|la possibilité/i,
      titulo: 'Si… alors',
      pasos: [
        { arte: () => reloj(12), pal: 's\'il pleut',  fin: ', je reste',   frase: 'La condition d\'abord.' },
        { arte: () => reloj(3),  pal: 'quand il pleut', fin: ', je reste', frase: 'quand : ça arrive toujours.' },
        { arte: () => reloj(9),  pal: 'peut-être',    fin: ' qu\'il pleut', frase: 'Ça, c\'est moins sûr !' },
      ],
      pie: 'Après si, on garde le présent.',
      reto: { p: '___ il fait beau, on sort.', ops: ['Si', 'Alors', 'Mais'], bien: 0 },
    },
    {
      id: 'demasiado',
      busca: /trop \+|pas assez/i,
      titulo: 'Trop, ou pas assez ?',
      pasos: [
        { arte: () => caja(124, '#d8a96c'), pal: 'trop',        fin: ' grande', frase: 'Elle ne passe pas la porte !' },
        { arte: () => caja(64, '#e8c49a'),  pal: 'pas assez',   fin: ' grande', frase: 'Tout ne rentre pas dedans.' },
        { arte: () => caja(92, '#e0b784'),  pal: 'assez',       fin: ' grande', frase: 'Celle-là va très bien.' },
      ],
      pie: 'trop, c\'est en excès. pas assez, c\'est en manque.',
      reto: { p: 'Le sac est ___ lourd, je ne peux pas le porter.', ops: ['trop', 'assez', 'pas assez'], bien: 0 },
    },
    {
      id: 'hay',
      busca: /il y a/i,
      titulo: 'Il y a',
      pasos: [
        { arte: () => bolas(1), pal: 'il y a',       fin: ' un ballon',    frase: 'Un seul.' },
        { arte: () => bolas(3), pal: 'il y a',       fin: ' trois ballons', frase: 'Ça ne change pas au pluriel !' },
        { arte: () => bolas(1), pal: 'il n\'y a pas', fin: ' de ballon',   frase: 'Et au négatif : pas de.' },
      ],
      pie: 'il y a reste pareil — c\'est ce qui suit qui change.',
      reto: { p: 'Dans la boîte ___ deux pommes.', ops: ['il y a', 'ils y ont', 'il y ont'], bien: 0 },
    },
  ];

  /* Las de repaso y las de estrategia de examen no llevan caja, igual que
     en ingles: no ensenan ninguna regla nueva. */
  const SIN_CAJA_FR = /bilan|stratégie|strategies/i;
