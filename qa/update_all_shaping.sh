#!/bin/sh

for file in shaping_input/*.toml; do
    if [ -f "$file" ]; then
        python3 update_shaping_test_data.py "$file" "../build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf" "../build/GoogleSans/variable/GoogleSans-Italic[GRAD,opsz,wght].ttf" ../build/GoogleSans/static/GoogleSans-BoldItalic.ttf ../build/GoogleSans/static/GoogleSans-Bold.ttf ../build/GoogleSans/static/GoogleSans-Italic.ttf ../build/GoogleSans/static/GoogleSans-MediumItalic.ttf ../build/GoogleSans/static/GoogleSans-Medium.ttf ../build/GoogleSans/static/GoogleSans-Regular.ttf ../build/GoogleSans/static/GoogleSansText-BoldItalic.ttf ../build/GoogleSans/static/GoogleSansText-Bold.ttf ../build/GoogleSans/static/GoogleSansText-Italic.ttf ../build/GoogleSans/static/GoogleSansText-MediumItalic.ttf ../build/GoogleSans/static/GoogleSansText-Medium.ttf ../build/GoogleSans/static/GoogleSansText-Regular.ttf
        echo "$file -> json write successful..."
    fi
done
