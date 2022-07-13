# --- Jyl's SR2 g_chunk utility --- #
#

from utils.binny import *
from utils.sr2_chunk_classes import *
from utils.modelhandler import mdl_export_format

if __name__ == '__main__':
    print("Run the main chunk importer instead!")

# g_chunks are all model data.

# --- Part 1:
# Vertices are stored in a couple different blobs, like 7 or 8 of them.
# Indices are in one continuous blob after verts.
# Dunno how to separate these models.

# --- Part 2:
# Not blobs. Separate models; verts followed by indices.
# Vsize varies with each model. No clue where to get anything.

def gchunk2mesh(filepath, vsizes, vcounts, icount, gmodels):

    f = open(filepath, 'rb')

    # --- Part 1 --- #
    vblob_count = len(vsizes)

    models = []

    vert_banks = []
    index_blob = []

    # --- Vertices --- #
    for i in range(vblob_count):
        vert_blob = []

        # size ranges at least from 20B to 36B
        # vsizes[i]:

        match vsizes[i]:
            case 24:

                for _ in range(vcounts[i]):

                    x = read_float(f, '<')
                    y = read_float(f, '<')
                    z = read_float(f, '<')

                    unk1 = read_uint(f, '<')   # affects shading
                    #unk2 = read_uint(f, '<')

                    f.read(4)   # uvs?
                    f.read(4)   # uvs?

                    vert_blob.append((x, y, z))

                vert_banks.append(vert_blob)
                SeekToNextRow(f)

            case _:
                for _ in range(vcounts[i]):

                    bytes_left = vsizes[i]

                    # regardless of type the vert begins with position.
                    x = read_float(f, '<')
                    y = read_float(f, '<')
                    z = read_float(f, '<')
                    bytes_left -= 12

                    f.read(bytes_left)
                    vert_blob.append((x, y, z))

                vert_banks.append(vert_blob)
                SeekToNextRow(f)

    # --- Indices --- #
    for _ in range(icount):
        index_blob.append(read_short(f, '<'))

    # --- Assemble this mess --- #
    models = []

    for i, gmodel in enumerate(gmodels):
        model = []
        for gmesh in gmodel.meshes0:
            mesh = [[],[],[]]   # [verts], [uvs], [faces]
            gmesh.vert_count = 0

            # --- V count isn't stored explicitly so gotta pull it if from indices.
            for ind_i in range(gmesh.index_count):
                index = index_blob[gmesh.index_offset + ind_i]
                gmesh.vert_count = max(gmesh.vert_count, index + 1)

            # --- Vertices
            for v_i in range(gmesh.vert_count):
                mesh[0].append(vert_banks[gmesh.vert_bank][gmesh.vert_offset + v_i])
            
            # --- Faces
            for ind_i in range(gmesh.index_count-2):
                i0 = index_blob[gmesh.index_offset + ind_i]+1
                i1 = index_blob[gmesh.index_offset + ind_i+1]+1
                i2 = index_blob[gmesh.index_offset + ind_i+2]+1

                mesh[2].append((i0,i1,i2))

            model.append(mesh)
        models.append(model)

    # --- Part 2 --- #
    # You tell me ¯\_(ツ)_/¯

    return models