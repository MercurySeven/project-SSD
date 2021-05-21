#!/bin/sh
briefcase create
briefcase build
cd macOS
mv app/ssd ssd
rm -r app
cd ssd
cat >launch.sh <<- "EOF"
#!/bin/sh
v1=$(pwd)
var2="/ssd.app/Contents/MacOS"
var3="$v1$var2"

cd $var3

open ssd
EOF

chmod +x launch.sh
cd ..
zip SSD_macOS.zip ssd -r
