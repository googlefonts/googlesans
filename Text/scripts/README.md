# Building “Brace” fonts with Fontmake

To build a VF with virtual masters or braces just move the folder “buildBraces” to the same directory as your source file. Then run the following command:

```
source buildBraces/build.sh glyphs-file-without-extension
```

## Troubleshooting

For fontmake to establish accurate min and max values for axes it relies on instance values. When using virtual masters make sure these ranges are covered by instances in the font. 
I believe there is a way to set an instance as hidden so that it does not show up in the final ttf while also influencnig the determination of axes extremes, but have not set that up just yet.

Please note that the `HVAR` table values for any brace layer glyphs is not being passed through into the final VF font. This can cause any character with an advance width change to not have updated metrics.

Author: Mike LaGattuta