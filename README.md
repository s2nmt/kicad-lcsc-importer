# LCSC Importer for KiCad

A plugin for KiCad 10 on Windows. Enter an LCSC part number to export the symbol, footprint, and 3D model (if available) to the `maruyama` library.

## Installation and usage

1. Download `lcsc-importer-pcm.zip` from the repository's **Releases** section.
2. In KiCad Manager, open **Plugin and Content Manager → Install from File…** and select the ZIP. If KiCad prompts you to remove the previous version first, select **Uninstall**, then click **Apply Pending Changes**.
3. In **Preferences → Plugins**, turn on **Enable KiCad API**. Use the Python installation bundled with KiCad. KiCad installs the dependencies into the plugin's own environment the first time it loads.
4. Reopen PCB Editor and find **Import LCSC** in the toolbar. Its icon is a white arrow on a blue background. Enter a part number such as `C116151` and click **Import**.
5. Add `maruyama.kicad_sym` and `maruyama.pretty` to the symbol and footprint library tables, respectively. Use `maruyama` as the nickname in both tables. The default export folder is `Documents/KiCad/10.0/libs`. In **Preferences → Configure Paths…**, set `MARUYAMA_3D` to the `maruyama.3dshapes` folder inside the export folder.

If multiple parts share a footprint, the converter may stop when it encounters an existing file. Select **Overwrite existing library entries** to replace duplicate entries.

## Updating and packaging

The plugin uses [uPesy's easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) from [PyPI](https://pypi.org/project/easyeda2kicad/). The version is pinned in `plugins/requirements.txt` so every installation uses the same converter version. The upstream source code is licensed under AGPL-3.0.

When a new upstream version is released, update the pin in `plugins/requirements.txt`, bump the plugin version in `metadata.json`, and test importing a part with a 3D model. The plugin reads the footprint path from the converter's log when linking 3D models, so verify that the footprint still resolves its model through `MARUYAMA_3D` after upgrading.

To build the installation ZIP, run this command from the repository root. Only the person packaging the release needs to run it.

```powershell
python build.py
```

Attach `dist/lcsc-importer-pcm.zip` to the GitHub Release. Users can download the ZIP and install it directly in KiCad.
