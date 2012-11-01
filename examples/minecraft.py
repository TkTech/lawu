#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
A template for scripts that modify the Minecraft client.
"""
if __name__ == '__main__':
    import sys
    from jawa import JarFile

    with JarFile(sys.argv[1]) as jf:
        for path, cf in jf.all_classes():

            # Do you modifications here.
            print cf.version

            with jf.open(path, 'w') as fout:
                cf.save(fout)

        jf.remove('META-INF/MOJANG_C.DSA')
        jf.remove('META-INF/MOJANG_C.SF')
        jf.save('minecraft.jar')
