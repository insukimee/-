import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const config = JSON.parse(fs.readFileSync(path.join(appDir, 'app.config.json'), 'utf8'));
const errors = [];

if (config.appIdConfirmed !== true) {
  errors.push('appIdConfirmed is not true. Confirm the Play applicationId before the first upload.');
}
if (!config.ads || config.ads.useTestAds !== false) {
  errors.push('ads.useTestAds is not false. Production must not ship Google sample ad units.');
}
const banner = config.ads && config.ads.bannerAdUnitId;
const appId = config.ads && config.ads.androidAppId;
if (!banner || String(banner).includes('REPLACE')) errors.push('bannerAdUnitId is still a placeholder.');
if (!appId || String(appId).includes('REPLACE')) errors.push('androidAppId is still a placeholder.');

const strings = fs.readFileSync(path.join(appDir, 'android/app/src/main/res/values/strings.xml'), 'utf8');
if (strings.includes('ca-app-pub-3940256099942544')) {
  errors.push('strings.xml still contains the Google sample AdMob app id.');
}
if (!fs.existsSync(path.join(appDir, 'android/keystore.properties'))) {
  errors.push('android/keystore.properties is missing, so bundleRelease is unsigned.');
}
if (!fs.existsSync(path.join(appDir, 'android/app/google-services.json'))) {
  errors.push('android/app/google-services.json is missing, so FCM will not register.');
}

if (errors.length) {
  console.error('Not ready for a Play production upload:');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}
console.log('Release checks passed.');
