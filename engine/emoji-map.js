/* Mapa palabra->emoji compartido por engine y book-builder */
const EMOJI = {
  // ropa y objetos
  umbrella:'☂️',gloves:'🧤',belt:'🩹',pocket:'👖',uniform:'🎽',suitcase:'🧳',ring:'💍',sunhat:'👒',scarf:'🧣',socks:'🧦',
  jacket:'🧥',jumper:'🧶',boots:'👢',trousers:'👖',skirt:'👗',shirt:'👕','t-shirt':'👕',cap:'🧢',dress:'👗',shoes:'👟',hat:'🎩',shorts:'🩳',coat:'🧥',sweater:'🧶',
  // comida
  butter:'🧈',cereal:'🥣',flour:'🌾',honey:'🍯',jam:'🍓',pepper:'🌶️',salt:'🧂',sugar:'🍬',yoghurt:'🥛',snack:'🍪',
  cheese:'🧀',tomato:'🍅',mushroom:'🍄',olives:'🫒',onion:'🧅',oven:'🔥',bread:'🍞',chicken:'🍗',chips:'🍟',egg:'🥚',rice:'🍚',fish:'🐟',cake:'🎂','ice cream':'🍦',pizza:'🍕',
  pasta:'🍝',soup:'🍲',salad:'🥗',sausage:'🌭',milkshake:'🥤',vegetables:'🥦',meat:'🥩',
  grapes:'🍇',pear:'🍐',lemon:'🍋',coconut:'🥥',carrot:'🥕',potato:'🥔',beans:'🫘',kiwi:'🥝',basket:'🧺',
  apple:'🍎',banana:'🍌',orange:'🍊',mango:'🥭',watermelon:'🍉',pineapple:'🍍',strawberry:'🍓',juice:'🧃',
  water:'💧',milk:'🥛',lemonade:'🍋','hot chocolate':'☕',cup:'☕',glass:'🥛',sandwich:'🥪',biscuit:'🍪',biscuits:'🍪',napkin:'🧻',
  toast:'🍞',pancakes:'🥞',menu:'📋',bill:'🧾',spoon:'🥄',
  // animales
  bat:'🦇',dolphin:'🐬',kangaroo:'🦘',lion:'🦁',panda:'🐼',parrot:'🦜',penguin:'🐧',shark:'🦈',snail:'🐌',whale:'🐋',
  cow:'🐮',sheep:'🐑',goat:'🐐',horse:'🐴',duck:'🦆',hen:'🐔',donkey:'🫏',pig:'🐷',
  monkey:'🐵',snake:'🐍',tiger:'🐯',crocodile:'🐊',elephant:'🐘',jungle:'🌴',bear:'🐻',giraffe:'🦒',hippo:'🦛',
  crab:'🦀',octopus:'🐙',starfish:'⭐',jellyfish:'🎐',shell:'🐚',wave:'🌊',
  dog:'🐶',cat:'🐱',bird:'🐦',rabbit:'🐰',mouse:'🐭',pet:'🐾',zoo:'🦁',
  // lugares y naturaleza
  museum:'🏛️',theatre:'🎭',castle:'🏰',stadium:'🏟️',airport:'✈️',funfair:'🎡',bridge:'🌉',restaurant:'🍽️',
  island:'🏝️',waterfall:'💦',cave:'🕳️',hill:'⛰️',path:'🛤️',wood:'🌳',stream:'🏞️',tent:'⛺',fire:'🔥',sky:'☁️',
  lake:'🏞️',forest:'🌲',mountain:'🏔️',rock:'🪨',boat:'⛵',picnic:'🧺',
  house:'🏠',kitchen:'🍳',bathroom:'🛁',bedroom:'🛏️',garden:'🌷',door:'🚪',window:'🪟',
  library:'📚',cinema:'🎬',shop:'🏪',supermarket:'🛒',hospital:'🏥',school:'🏫','café':'☕',playground:'🛝',bank:'🏦','swimming pool':'🏊',
  village:'🏘️',field:'🌾',church:'⛪',street:'🛣️',beach:'🏖️',park:'🌳',sea:'🌊',sand:'🏖️',
  balcony:'🪟',basement:'🕳️',stairs:'🪜',lift:'🛗',gate:'🚧',roof:'🏠',shelf:'📚',cupboard:'🗄️',fridge:'🧊',corner:'📐',
  // transporte
  bicycle:'🚲',bike:'🚲',motorway:'🛣️',platform:'🚉',railway:'🛤️',taxi:'🚕',tram:'🚋',ambulance:'🚑','fire engine':'🚒',helicopter:'🚁',traffic:'🚦',
  bus:'🚌',train:'🚂',car:'🚗',lorry:'🚚',motorbike:'🏍️',ticket:'🎫',seat:'💺',driver:'🧑‍✈️',stop:'🛑',
  // escuela
  maths:'➗',science:'🔬',art:'🎨',music:'🎵',history:'📜',geography:'🗺️',sport:'⚽',timetable:'📅',homework:'📓',
  pen:'🖊️',pencil:'✏️',book:'📖',bag:'🎒',eraser:'🧽',ruler:'📏',chair:'🪑',table:'🪑',board:'🖼️',crayon:'🖍️',crayons:'🖍️',
  'pencil case':'👝',rubber:'🧽',scissors:'✂️',glue:'🧴',notebook:'📓',sharpener:'🔪',backpack:'🎒',diary:'📔',
  // cuerpo y salud
  shoulder:'💪',stomach:'🫃',tongue:'👅',knee:'🦵',beard:'🧔',elbow:'💪',moustache:'👨',back:'🔙',neck:'🦒',finger:'👆',fingers:'👆',
  head:'🙂',arm:'💪',hand:'✋',leg:'🦵',foot:'🦶',feet:'🦶',body:'🧍',toes:'🦶',
  face:'🙂',eyes:'👀',ears:'👂',nose:'👃',mouth:'👄',hair:'💇',teeth:'🦷',smile:'😊',
  headache:'🤕',toothache:'😖',cold:'🤧',cough:'😷',temperature:'🌡️',medicine:'💊',doctor:'🧑‍⚕️',nurse:'🧑‍⚕️',dentist:'🦷',hurt:'🤕',ill:'🤒',
  hospital2:'🏥','X-ray':'🩻',card:'💌',flowers:'💐',brave:'🦸',
  // clima y tiempo
  storm:'⛈️',lightning:'⚡',thunder:'🌩️',fog:'🌫️',ice:'🧊',flood:'🌊',dry:'🏜️',wet:'💦',
  sunny:'☀️',rainy:'🌧️',windy:'💨',snowy:'❄️',cloudy:'☁️',hot:'🥵',rainbow:'🌈',snow:'⛄',sunshine:'🌞',season:'🍂',
  spring:'🌸',summer:'☀️',autumn:'🍁',winter:'⛄',cloud:'☁️',wind:'💨',weather:'🌤️',
  sun:'☀️',moon:'🌙',star:'⭐',stars:'✨',night:'🌃',morning:'🌅',
  // objetos casa
  sofa:'🛋️',armchair:'🛋️',carpet:'🟫',curtains:'🪟',lamp:'💡',mirror:'🪞',drawer:'🗄️',pillow:'🛏️',blanket:'🛌',box:'📦',
  bed:'🛏️',desk:'🖥️',wardrobe:'👗',poster:'🖼️',clock:'🕐','toy box':'🧸',picture:'🖼️',rug:'🟫',
  // varios
  planet:'🪐',rocket:'🚀',spaceship:'🛸',alien:'👽',Earth:'🌍',astronaut:'🧑‍🚀',space:'🌌',
  treasure:'💰',map:'🗺️',north:'🧭',south:'🧭',east:'🧭',west:'🧭',cross:'❌',dig:'⛏️',secret:'🤫',
  postcard:'💌',stamp:'📮',address:'🏠',envelope:'✉️',send:'📤',greetings:'👋',sign:'✍️',letter:'💌',
  ball:'⚽',kite:'🪁',doll:'🪆',teddy:'🧸',toy:'🧸',robot:'🤖',game:'🎲','board game':'🎲',puzzle:'🧩',
  volleyball:'🏐',skating:'⛸️',sledging:'🛷',snowboarding:'🏂',golf:'⛳',race:'🏁',prize:'🏆',team:'👥',medal:'🏅',champion:'🏆',
  football:'⚽',basketball:'🏀',tennis:'🎾',swimming:'🏊',running:'🏃',goal:'🥅',win:'🏆',winner:'🏆',
  guitar:'🎸',drum:'🥁',song:'🎵',dance:'💃',sing:'🎤',
  birthday:'🎂',party:'🎉',present:'🎁',candle:'🕯️',balloon:'🎈',guest:'🧑‍🤝‍🧑',wish:'🌠',celebrate:'🥳',
  phone:'📞',mobile:'📱',message:'💬',camera:'📷',photo:'📸',album:'📔',TV:'📺',screen:'📺',channel:'📺',
  firefighter:'🧑‍🚒',journalist:'🎤',engineer:'🧑‍🔧',pilot:'🧑‍✈️',waiter:'🧑‍🍳','police officer':'👮',cook:'🧑‍🍳',manager:'💼',
  farmer:'🧑‍🌾',vet:'🧑‍⚕️',inventor:'🧑‍🔬',writer:'✍️',designer:'🎨',singer:'🎤',scientist:'🔬',footballer:'⚽',artist:'🎨',explorer:'🧭',
  happy:'😊',sad:'😢',angry:'😠',worried:'😟',surprised:'😲',proud:'😌',cry:'😭',laugh:'😂',hug:'🤗',tired:'😴',hungry:'😋',thirsty:'🥤',scared:'😨',
  lighthouse:'🗼',certificate:'📜',graduation:'🎓',adventure:'🗺️',together:'🤝',future:'🔮',dream:'💭',
  one:'1️⃣',two:'2️⃣',three:'3️⃣',four:'4️⃣',five:'5️⃣',six:'6️⃣',seven:'7️⃣',eight:'8️⃣',nine:'9️⃣',ten:'🔟',
  red:'🔴',blue:'🔵',green:'🟢',yellow:'🟡',purple:'🟣',pink:'🩷',black:'⚫',white:'⚪',brown:'🟤',
  Monday:'📅',Tuesday:'📅',Wednesday:'📅',Thursday:'📅',Friday:'📅',Saturday:'🎉',Sunday:'🏡',week:'🗓️',today:'📌',tomorrow:'➡️',weekend:'🎉',
  alphabet:'🔤','letter-abc':'🔠',spell:'🔤',name:'📛'
};
if (typeof module !== 'undefined') module.exports = { EMOJI };
