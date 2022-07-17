Knobby:
The chunk_pc file is a loadable part of the world. It is what is needed for a physical chunk of the world. This includes the level geometry, level collision, sidewalk data, traffic splines, world objects, textures, etc. I say etc, but it really is probably just the tip of the iceberg. This is a massive monolithic file full of all kinds of things.



**sr2_chunk_extract_gmodels.py** extracts obj from g_chunk  
**sr2_chunk_extract_materials.py** extracts mtl from chunk  
**sr2_chunk_extract_texturelist.py** extracts a list of textures used in the chunk.  
**sr2_chunk_replace_gmodels.py** rebuild g_chunk from extracted models (and a very tiny bit of the old one).

Script usage:  
```python path/to/script.py path/to/chunkfile.chunk_pc```

Use this to get textures: https://www.saintsrowmods.com/forum/threads/saints-row-2-chunks-texture-tool.12877/  
Put textures to ./textures/ folder relative to mtl file.

Python 3.10 or newer required




#### Old blender scripts: 
**import_chunk_bbox1.py:**    Import bounding boxes  
**chunk_pc_import_mesh0.py:**    Old importer for models  
**sr2_chunk_pc_import.py:**    Old, broken.  
**traverse_the_file.py:**    For development   
