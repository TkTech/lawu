# Jawa

Jawa is a pure-python Java disassembler and assembler currently under
development. Expect it to be buggy/broken at times.

*NOTE*: The assembler does _not_ currently implement Stack Maps, an
artificially complex requirement for ClassFiles generated for Java 7 and
above to properly verify (unless you turn it off with -XX:-UseSplitVerifier).
However, assembled files targetting Java 6 will still work with 7 and above.

## Documentation

Extensive API documentation is available at http://jawa.tkte.ch

## Licence

Jawa is available under the MIT licence. See LICENCE.
