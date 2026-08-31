#!/bin/sh

for file in shaping_input/*.toml; do
    if [ -f "$file" ]; then
        find ../fonts -name '*.ttf' \
            -not -path "../fonts/.intermediate.*" \
            -not -path "../fonts/android/*" \
            -not -path "../fonts/figma/*" \
            -print0 \
        | xargs --null python update_shaping_test_data.py "$file"
        echo "$file -> json write successful..."
    fi
done
