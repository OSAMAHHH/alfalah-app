#!/bin/bash
sed -i '/<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" \/>/a \    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" \/>\n    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" \/>' app/src/main/AndroidManifest.xml
