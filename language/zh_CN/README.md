# 存档翻译提取器

一个从MC存档中提取可翻译文本以便于本地化的工具。

## 基本功能

该工具可扫描整个存档及其相关文件，定位到 JSON 文本组件（以及适用时的纯文本），并将其替换为翻译后的 JSON 组件。

目前支持 Minecraft Java 版 1.21。NBT 结构的管理代码是模块化的，允许针对不同的 Minecraft 版本定义不同的提取器，并进行动态加载。

工具依赖：[Amulet World Editor](https://www.amuletmc.com/) API。

## 使用方法

World Translation Extractor 目前提供命令行界面。

```
python main.py [-h] --world WORLD [--out OUT] [--force | -f]
                                   [--lang LANG] [--extract EXTRACT] [--dimension DIMENSION]
                                   [--keepdup | -k] [--sort | -s]
                                   [--indent INDENT] [--batch BATCH]
                                   [--versionless | -v]
```

选项说明：
- `-h, --help`：显示帮助信息并退出。
- `--world WORLD, -w WORLD`：目标存档的路径。
- `--out OUT, -o OUT`：输出翻译文件的路径，默认路径为 `<WORLD>_wte`。
- `--force, --no-force, -f`：在提取前删除 `<OUT>` 中的现有内容。
- `--lang LANG, -l LANG`：指定输出翻译 JSON 文件的路径，默认为 `wte_lang.json`。
- `--extract EXTRACT, -e EXTRACT`：指定要运行的提取器，可以指定多个。不指定时将运行所有可用的提取器。
- `--dimension DIMENSION, -d DIMENSION`：指定要扫描的维度，可以选择多个。若不指定，则扫描所有维度。
- `--keepdup, --no-keepdup, -k`：保留重复的翻译文本作为单独的键。
- `--sort, --no-sort, -s`：按字母顺序排序输出 JSON。
- `--indent INDENT, -i INDENT`：设置输出 JSON 的缩进空格数。
- `--batch BATCH, -b BATCH`：每处理 `<BATCH>` 个区块时保存一次。
- `--versionless, --no-versionless, -v`：忽略提取器与数据版本的兼容性问题。

例如，运行 `python main.py -w "C:\Users\Administrator\AppData\Roaming\.minecraft\saves\WTE_Test"` 将使用默认设置从名为 WTE_Test 的存档中提取翻译内容。

提取后的存档将复制到原始存档目录中，并在工作目录下创建一个包含提取字符串的 JSON 文件。该文件格式与 Minecraft 资源包的语言文件相同。

## 安装

需要 [Python](https://www.python.org/downloads/) 3.9+（推荐 3.11+）。

下载或克隆此仓库后，使用以下命令安装所需依赖项：

```bash
python -m pip install -r requirements.txt
```

## 提取器

此存储库包含以下提取器模块，支持 Minecraft 1.21 版本，部分提取器还支持较旧的 Minecraft 数据版本。详细信息请参阅各模块的源文件。

### 方块实体提取器

- `bee`：处理 `beehive` 和 `bee_nest`，提取 `bees` 标签中的实体。
- `command_block`：处理 `command_block`，提取 `Command` 字段中的组件。
- `container`：处理多个容器，提取 `CustomName` 和 `Items`。
- `item_tile`：提取 `jukebox`、`lectern` 和 `decorated_pot` 中的项目。
- `sign`：处理 `sign` 和 `hanging_sign`，提取 `front_text` 和 `back_text` 中的消息。
- `spawner`：处理 `mob_spawner`，提取 `SpawnData` 和 `SpawnPotentials` 中的实体。

### 实体提取器

- `command_block_minecart`：处理 `command_block_minecart`，提取 `Command` 字段中的组件。
- `entity`：运行于所有实体，提取 `CustomName` 和 `Passengers` 中的其他实体。
- `item_entity`：提取多个实体中的 `item` 项目。

### 物品提取器

- `book`：处理 `written_book`，提取 `pages` 和 `title` 中的文本。
- `item`：运行于所有物品，提取 `custom_name`、`item_name` 和 `lore`。

### 数据文件提取器
- `level`：处理 `level
.dat` 文件，提取 `Player` 和 `CustomBossEvents` 中的 bossbar 标题。

### 文本文件提取器

- `function`：处理所有数据包中的 `mcfunction` 文件，提取文本组件和命令中的纯文本。

## 致谢

使用此工具时不强制致谢，但若项目中明确提及本工具，我们将不胜感激。

## 贡献

我们欢迎任何形式的贡献，尤其是关于新增提取器或针对新 Minecraft 版本的提取器更新。

此外，您也可以为此工具本身进行翻译（请查看 `language` 文件夹），并欢迎将其翻译成其他语言！
