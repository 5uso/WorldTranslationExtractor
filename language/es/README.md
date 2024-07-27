# WorldTranslationExtractor
 
Una herramienta para extraer textos traducibles de mundos de Minecraft para permitir localizarlos.

## Qué hace?

Escanea una save entera, con sus archivos asociados, encontrando componentes de texto json (así como texto plano donde sea aplicable) y reemplazándolos con componentes de traducción json.

Actualmente soporta Minecraft Java Edition 1.21. El código que maneja las estructuras de NBT es modular, con diferentes extractores que se cargan dinámicamente y se pueden definir para distintas versiones de Minecraft.

Depende en la API de [Amulet world editor](https://www.amuletmc.com/).

## Uso
World Translation Extractor está provisto de una interfaz de línea de comandos.
```
python3 main.py [-h] --world WORLD [--out OUT] [--force | -f]
                                   [--lang LANG] [--extract EXTRACT] [--dimension DIMENSION]
                                   [--keepdup | -k] [--sort | -s]
                                   [--indent INDENT] [--batch BATCH]
                                   [--versionless | -v]
options:
  -h, --help            muestra este mensaje de ayuda
  --world WORLD, -w WORLD
                        Ruta al mundo a extraer.
  --out OUT, -o OUT     Ruta en la que crear una copia traducida del mundo.
                        Por defecto, <WORLD>_wte.
  --force, --no-force, -f
                        Borrar los anteriores contenidos de <OUT> antes de empezar.
  --lang LANG, -l LANG  Ruta en la que escribir el json de traducción.
                        Por defecto, wte_lang.json.
  --extract EXTRACT, -e EXTRACT
                        Un extractor que ejecutar sobre el mundo, se pueden seleccionar varios.
                        Si no se especifican extractores, se ejecutarán todos los disponibles.
  --dimension DIMENSION, -d DIMENSION
                        Una dimensión para escanear, se pueden seleccionar varias.
                        Si no se especifican dimensiones, se escanearán todas.
  --keepdup, --no-keepdup, -k
                        Mantener textos duplicados bajo distintas keys de traducción.
  --sort, --no-sort, -s
                        Ordenar los contenidos del json de salida alfabéticamente.
  --indent INDENT, -i INDENT
                        Cantidad de espacios con la que se indenta el json de salida.
  --batch BATCH, -b BATCH
                        Mientras se itera el mundo, guardar cada <BATCH> chunks.
  --versionless, --no-versionless, -v
                        Ignorar incompatibilidades de versión de datos en los extractores.
```
Por ejemplo, `python3 main.py -w "C:\Users\el sus\AppData\Roaming\.minecraft\saves\WTE_Test"` extraería las traducciones de un mundo nombrado WTE_Test con ajustes por defecto.

El mundo editado se copia a una nueva carpeta en el mismo directorio que el original. Un archivo json que contiene las cadenas de texto extraídas, asociadas a keys de traducción, se crea en el directorio de trabajo. Este archivo tiene el mismo formato que un lang de resourcepack.

## Instalación
La herramienta se ejecuta en [Python](https://www.python.org/downloads/) 3.9+ (recomendado 3.11+). Si usas Windows, puede ser conveniente instalar python a través de la Microsoft Store.

Descarga o clona este repo, e instala las dependencias requeridas haciendo `python3 -m pip install -r requirements.txt` .

## Extractores
Los siguientes módulos de extracción están incluidos en este repositorio. Todos funcionan en Minecraft 1.21, aunque algunos soportan DataVersions menores. Comprueba su código para más detalles.
### Extractores de bloques
Los extractores de bloques se ejecutan sobre todas las block entities del mundo, así como en las que se encuentren en estructuras de datapacks o la carpeta generated.
#### `bee`
Maneja `beehive` y `bee_nest`. Extrae entidades de la tag `bees`.
#### `command_block`
Maneja `command_block`. Extrae componentes del campo `Command`.
#### `container`
Maneja los siguientes contenedores: `'chest', 'furnace', 'shulker_box', 'barrel', 'smoker', 'blast_furnace', 'trapped_chest', 'hopper', 'dispenser', 'dropper', 'brewing_stand', 'campfire', 'chiseled_bookshelf', 'crafter'`. Extrae su `CustomName`, así como los `Items` que contengan.
#### `item_tile`
Extrae `RecordItem` de las `jukebox`, `Book` de los `lectern`, y `item` de los `decorated_pot`.
#### `sign`
Maneja tanto `sign` como `hanging_sign`. Extrae `messages` de `front_text` y `back_text`.
#### `spawner`
Maneja `mob_spawner`. Extrae entidades de `SpawnData` y `SpawnPotentials`.
#### `trial_spawner`
Maneja `trial_spawner`. Extrae entidades de `spawn_data`, y para `spawn_potentials` tanto de `normal_config` como `ominous_config`.
#### `vault`
Maneja `vault`. Extrae items de `key_item`, `display_item`, y `items_to_eject`.
### Extractores de entidades
Los extractores de entidades se ejecutan sobre todas las entidades del mundo, así como en las que se encuentren en estructuras de datapacks o la carpeta generated.
#### `command_block_minecart`
Maneja `command_block_minecart`. Extrae componentes del campo `Command`.
#### `container_entity`
Extrae los `Items` de `'hopper_minecart', 'chest_minecart', 'chest_boat', 'trader_llama', 'mule', 'llama', 'donkey'`; y los `Inventory` de `'wandering_trader', 'villager', 'pillager', 'player', 'piglin', 'allay'`.
#### `entity`
Se ejecuta para todas las entidades. Extrae `CustomName`, así como otras entidades en `Passengers`.
#### `item_entity`
Extrae `item` de `'arrow', 'spectral_arrow', 'ominous_item_spawner', 'trident', 'item_display'`; `Item` de `'item_frame', 'eye_of_ender', 'item', 'snowball', 'small_fireball', 'potion', 'fireball', 'experience_bottle', 'ender_pearl', 'egg'`; `FireworksItem` de `'firework_rocket'`; `SaddleItem` de `'zombie_horse', 'skeleton_horse', 'mule', 'horse', 'donkey'`; y `weapon` de `'arrow', 'spectral_arrow'`.
#### `mob`
Se ejecuta para todas las entidades (para asegurar compatibilidad futura). Extrae items de `ArmorItems`, `HandItems`, y `body_armor_item`.
#### `player`
Maneja `player`. Extrae items de `EnterItems`, y entidades de `ShoulderEntityLeft` y `ShoulderEntityRight`.
#### `spawner_minecart`
Maneja `spawner_minecart`. Extrae entidades de `SpawnData` y `SpawnPotentials`.
#### `text_display`
Maneja `text_display`. Extrae `text`.
#### `villager`
Maneja `villager`, `zombie_villager`, y `wandering_trader`. Extrae items dentro de `Offers`.
### Extractores de items
Los extractores de items se ejecutan sobre todos los items que se encuentren en entidades, block entities, u otros items.
#### `book`
Maneja `written_book`. Extrae texto desde `pages` y `title`. La traducción de `title` se copia al `custom_name` si este no existe ya. El campo `author` se omite. Esto es porque tanto `title` como `author` no soportan componentes json.
#### `item`
Se ejecuta para todos los items. Extrae `custom_name`, `item_name`, y `lore`; así como block entities desde `block_entity_data`, items dentro de `container`, y entidades desde `entity_data`.
### Extractores de archivos de datos
Los extractores de archivos de datos trabajan con archivos en formato dat específicos dentro de la carpeta de la save.
#### `level`
Maneja `level.dat`. Extrae al `Player`, así como títulos de bossbar desde `CustomBossEvents`.
#### `score`
Maneja `scoreboard.dat`. Extrae nombres de objetivos de scoreboard desde `Objectives`; y nombres, prefijos, and sufijos de equipo desde `Teams`.
#### `storage`
Maneja todos los archivos dat relacionados con data storage. Itera todos los posibles componentes de forma recursiva, reemplazando sólo las instancias en las que se usan componentes de texto json.
### Extractores de archivos de texto
Los extractores de archivos de texto trabajan con archivos en texto plano dentro de los datapacks.
#### `function`
Maneja todos los archivos en formato mcfunction. Extrae cualquier componente de texto que se encuentre, así como texto plano si encaja como parte del comando `bossbar`.
#### `json`
Maneja todos los archivos en formato json. Extrae cualquier componente de texto que se encuentre.

## Créditos
Dar crédito explícito dentro de los proyectos para los que se use esta herramienta no es estrictamente necesario, pero se aprecia igualmente.

## Contribuciones
Las contribuciones, especialmente aquellas que aporten nuevos extractores o actualicen los existentes a nuevas versiones de Minecraft, son bienvenidas.

Esta herramienta también se puede traducir (a través de la carpeta `language`). Se aprecian traducciones a otros idiomas!
