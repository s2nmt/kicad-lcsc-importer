# Kicad LCSC Importer

A plugin for KiCad 10 on Windows. Enter an LCSC part number to export the symbol, footprint, and 3D model (if available) to a library of your choice.

## Installation and usage

1. Download `lcsc-importer-pcm.zip` from the repository's **Releases** section.
2. In KiCad Manager, open **Plugin and Content Manager → Install from File…** and select the ZIP. If you installed a company-branded release, uninstall it and click **Apply Pending Changes** before installing this ZIP. The new package uses a different identifier.
3. In **Preferences → Plugins**, turn on **Enable KiCad API**. Use the Python installation bundled with KiCad. KiCad installs the dependencies into the plugin's own environment the first time it loads.
4. Reopen PCB Editor and find **Import LCSC** in the toolbar. Its icon is a white arrow on a blue background. Enter a part number such as `C116151` and a **Library name** such as `my_parts`, then click **Import**. The default library name is `lcsc_importer`. Library names can contain letters A–Z, digits, underscores, and hyphens. Windows device names are reserved.
5. Add the exported symbol file and footprint folder to the corresponding library tables. For `my_parts`, add `my_parts.kicad_sym` and `my_parts.pretty` and use `my_parts` as the nickname in both tables. The default export folder is `Documents/KiCad/10.0/libs`.
6. If the import includes a 3D model, use **Preferences → Configure Paths…** to set the variable shown in the import result. For `my_parts`, set `MY_PARTS_3D` to the `my_parts.3dshapes` folder inside the export folder. Use distinct library names for libraries in different folders that you want to use together.

If multiple parts share a footprint, the converter may stop when it encounters an existing file. Select **Overwrite existing library entries** to replace duplicate entries.

The dialog remembers the library name from your last successful import and fills it in the next time you open it.

## Updating and packaging

The plugin uses [uPesy's easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) from [PyPI](https://pypi.org/project/easyeda2kicad/). The version is pinned in `plugins/requirements.txt` so every installation uses the same converter version. The upstream source code is licensed under AGPL-3.0.

When a new upstream version is released, update the pin in `plugins/requirements.txt`, bump the plugin version in `metadata.json`, and test importing a part with a 3D model. The plugin reads the footprint path from the converter's log when linking 3D models, so verify that the footprint still resolves its model through the library's path variable after upgrading.

To build the installation ZIP, run this command from the repository root. Only the person packaging the release needs to run it.

```powershell
python build.py
```

Attach `dist/lcsc-importer-pcm.zip` to the GitHub Release. Users can download the ZIP and install it directly in KiCad.
