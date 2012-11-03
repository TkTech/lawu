#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
A template for scripts that modify the Minecraft client.
"""
import sys

from jawa import JarFile

if __name__ == '__main__':
    with JarFile(sys.argv[1]) as jf:
        for path, cf in jf.all_classes():
            for method in cf.methods.find(f=lambda m: m.code):
                for ins in method.code.disassemble():
                    print ins

            # Do you modifications here.

            with jf.open(path, 'w') as fout:
                cf.save(fout)

        jf.remove('META-INF/MOJANG_C.DSA')
        jf.remove('META-INF/MOJANG_C.SF')
        jf.save('minecraft.jar')
