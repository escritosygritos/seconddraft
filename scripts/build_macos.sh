#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
app="dist/Second Draft.app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp second_draft.py "$app/Contents/Resources/second_draft.py"
cat > "$app/Contents/MacOS/SecondDraft" <<'LAUNCHER'
#!/bin/bash
here="$(cd "$(dirname "$0")/../Resources" && pwd)"
exec /usr/bin/python "$here/second_draft.py"
LAUNCHER
chmod +x "$app/Contents/MacOS/SecondDraft"
cat > "$app/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleName</key><string>Second Draft</string>
<key>CFBundleDisplayName</key><string>Second Draft</string>
<key>CFBundleIdentifier</key><string>org.seconddraft.writer</string>
<key>CFBundleExecutable</key><string>SecondDraft</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleShortVersionString</key><string>0.1.0</string>
<key>LSMinimumSystemVersion</key><string>10.8.5</string>
</dict></plist>
PLIST
echo "Built $app"
