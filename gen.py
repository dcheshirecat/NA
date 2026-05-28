import os, shutil

def write(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

write('settings.gradle', """\
rootProject.name = "Clarity"
include ':app'
""")

write('build.gradle', """\
buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:8.2.2' }
}
allprojects { repositories { google(); mavenCentral() } }
""")

write('gradle.properties', """\
android.useAndroidX=true
android.enableJetifier=true
org.gradle.jvmargs=-Xmx2048m
""")

write('app/build.gradle', """\
plugins { id 'com.android.application' }
android {
    namespace 'com.clarity.recovery'
    compileSdk 34
    defaultConfig {
        applicationId "com.clarity.recovery"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    signingConfigs {
        release {
            storeFile file("${rootDir}/keystore.jks")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            minifyEnabled false
            signingConfig signingConfigs.release
        }
    }
}
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.webkit:webkit:1.9.0'
}
""")

write('app/src/main/AndroidManifest.xml', """\
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <application
        android:label="Clarity"
        android:theme="@style/AppTheme"
        android:networkSecurityConfig="@xml/network_security_config"
        android:hardwareAccelerated="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

write('app/src/main/res/values/strings.xml', """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Clarity</string>
</resources>
""")

# Theme.AppCompat.NoActionBar is always available via appcompat dependency
write('app/src/main/res/values/styles.xml', """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.NoActionBar">
        <item name="android:windowBackground">#0f1117</item>
        <item name="android:statusBarColor">#0f1117</item>
        <item name="android:navigationBarColor">#0f1117</item>
        <item name="android:windowFullscreen">true</item>
    </style>
</resources>
""")

write('app/src/main/res/xml/network_security_config.xml', """\
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true"/>
</network-security-config>
""")

# Use AppCompatActivity so the AppCompat theme resolves correctly
write('app/src/main/java/com/clarity/recovery/MainActivity.java', """\
package com.clarity.recovery;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.View;
import android.view.WindowManager;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setTextZoom(100);

        webView.setWebViewClient(new WebViewClient());
        webView.setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
            View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            View.SYSTEM_UI_FLAG_FULLSCREEN
        );
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
}
""")

os.makedirs('app/src/main/assets', exist_ok=True)
shutil.copy('index.html', 'app/src/main/assets/index.html')

print("Android project generated successfully.")
