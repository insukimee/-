import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const androidDir = path.join(appDir, 'android');
const appGradle = path.join(androidDir, 'app', 'build.gradle');
const manifestPath = path.join(androidDir, 'app', 'src', 'main', 'AndroidManifest.xml');
const stringsPath = path.join(androidDir, 'app', 'src', 'main', 'res', 'values', 'strings.xml');
const variablesPath = path.join(androidDir, 'variables.gradle');
const rootGradle = path.join(androidDir, 'build.gradle');

function read(file) {
  return fs.readFileSync(file, 'utf8');
}

function write(file, text) {
  fs.writeFileSync(file, text);
  console.log('patched', path.relative(appDir, file));
}

function replaceOnce(file, from, to, label) {
  const text = read(file);
  if (text.includes(to)) {
    console.log('already', label);
    return;
  }
  if (!text.includes(from)) {
    throw new Error(`pattern missing for ${label} in ${path.relative(appDir, file)}`);
  }
  write(file, text.replace(from, to));
}

const config = JSON.parse(read(path.join(appDir, 'app.config.json')));
if (!fs.existsSync(appGradle)) {
  throw new Error('android/app/build.gradle is missing. Run npx cap add android first.');
}

let variables = read(variablesPath);
variables = variables.replace(/minSdkVersion\s*=\s*\d+/, 'minSdkVersion = 24');
variables = variables.replace(/compileSdkVersion\s*=\s*\d+/, 'compileSdkVersion = 36');
variables = variables.replace(/targetSdkVersion\s*=\s*\d+/, 'targetSdkVersion = 36');
write(variablesPath, variables);

let gradle = read(appGradle);
gradle = gradle.replace(/versionCode\s+\d+/, `versionCode ${config.versionCode}`);
gradle = gradle.replace(/versionName\s+"[^"]*"/, `versionName "${config.version}"`);
if (!gradle.includes('MI-SIGNING')) {
  const signing = `
    // MI-SIGNING: release is signed only when android/keystore.properties exists.
    def keystorePropertiesFile = rootProject.file("keystore.properties")
    def keystoreProperties = new Properties()
    if (keystorePropertiesFile.exists()) {
        keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
    }
`;
  gradle = gradle.replace(/android\s*\{/, `${signing}\nandroid {`);
  if (!/signingConfigs\s*\{/.test(gradle)) {
    gradle = gradle.replace(
      /buildTypes\s*\{/,
      `signingConfigs {
        release {
            if (keystorePropertiesFile.exists()) {
                storeFile rootProject.file(keystoreProperties['storeFile'])
                storePassword keystoreProperties['storePassword']
                keyAlias keystoreProperties['keyAlias']
                keyPassword keystoreProperties['keyPassword']
            }
        }
    }
    buildTypes {`,
    );
  }
  gradle = gradle.replace(
    /buildTypes\s*\{\s*release\s*\{/,
    `buildTypes {
        release {
            if (keystorePropertiesFile.exists()) {
                signingConfig signingConfigs.release
            }`,
  );
}
write(appGradle, gradle);

let root = read(rootGradle);
if (!root.includes('com.google.gms:google-services')) {
  root = root.replace(
    /dependencies\s*\{/,
    `dependencies {\n        classpath 'com.google.gms:google-services:4.4.2'`,
  );
  write(rootGradle, root);
} else {
  console.log('already google-services classpath');
}

let manifest = read(manifestPath);
if (!manifest.includes('com.google.android.gms.permission.AD_ID')) {
  manifest = manifest.replace(
    '<application',
    '<uses-permission android:name="com.google.android.gms.permission.AD_ID" />\n    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\n\n    <application',
  );
}
if (!manifest.includes('com.google.android.gms.ads.APPLICATION_ID')) {
  manifest = manifest.replace(
    '</application>',
    `    <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="@string/admob_app_id" />
    </application>`,
  );
}
write(manifestPath, manifest);

let strings = read(stringsPath);
if (!strings.includes('admob_app_id')) {
  strings = strings.replace(
    '</resources>',
    `    <string name="admob_app_id">${config.ads.androidTestAppId}</string>\n</resources>\n`,
  );
}
strings = strings.replace(
  /<string name="app_name">[\s\S]*?<\/string>/,
  `<string name="app_name">${config.appName}</string>`,
);
strings = strings.replace(
  /<string name="title_activity_main">[\s\S]*?<\/string>/,
  `<string name="title_activity_main">${config.appName}</string>`,
);
write(stringsPath, strings);

const colorsPath = path.join(androidDir, 'app', 'src', 'main', 'res', 'values', 'colors.xml');
if (!fs.existsSync(colorsPath)) {
  write(colorsPath, `<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#0D0D0D</color>
    <color name="colorPrimaryDark">#0D0D0D</color>
    <color name="colorAccent">#16C784</color>
</resources>
`);
}

const stylesPath = path.join(androidDir, 'app', 'src', 'main', 'res', 'values', 'styles.xml');
let styles = read(stylesPath);
styles = styles.replace(
  'parent="Theme.AppCompat.Light.DarkActionBar"',
  'parent="Theme.AppCompat.DayNight.NoActionBar"',
);
if (!styles.includes('android:statusBarColor')) {
  styles = styles.replace(
    '<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">',
    `<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="android:statusBarColor">#0D0D0D</item>
        <item name="android:navigationBarColor">#0D0D0D</item>
        <item name="android:windowBackground">#0D0D0D</item>`,
  );
}
write(stylesPath, styles);

const javaDir = path.join(androidDir, 'app', 'src', 'main', 'java', 'com', 'usmarketinsight', 'app');
fs.mkdirSync(javaDir, { recursive: true });
fs.copyFileSync(
  path.join(appDir, 'native-extras', 'MiTopicsPlugin.java'),
  path.join(javaDir, 'MiTopicsPlugin.java'),
);
const activityPath = path.join(javaDir, 'MainActivity.java');
let activity = read(activityPath);
if (!activity.includes('MiTopicsPlugin')) {
  if (!activity.includes('import android.os.Bundle;')) {
    activity = activity.replace('import com.getcapacitor.BridgeActivity;', 'import android.os.Bundle;\nimport com.getcapacitor.BridgeActivity;');
  }
  activity = activity.replace(
    'public class MainActivity extends BridgeActivity {}',
    `public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(MiTopicsPlugin.class);
        super.onCreate(savedInstanceState);
    }
}`,
  );
  if (!activity.includes('MiTopicsPlugin')) {
    throw new Error('Could not patch MainActivity. The Capacitor template shape changed.');
  }
  write(activityPath, activity);
} else {
  console.log('already MainActivity plugin');
}

const resSrc = path.join(appDir, 'resources', 'android');
const resDest = path.join(androidDir, 'app', 'src', 'main', 'res');
if (fs.existsSync(resSrc)) {
  fs.cpSync(resSrc, resDest, { recursive: true });
  console.log('copied launcher icons');
} else {
  console.log('resources/android missing; run python3 scripts/gen-icons.py');
}

fs.copyFileSync(
  path.join(appDir, 'native-extras', 'google-services.json.example'),
  path.join(androidDir, 'app', 'google-services.json.example'),
);
fs.copyFileSync(
  path.join(appDir, 'native-extras', 'keystore.properties.example'),
  path.join(androidDir, 'keystore.properties.example'),
);
console.log('native extras applied');
