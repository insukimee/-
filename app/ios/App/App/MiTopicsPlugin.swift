import Capacitor

/// Same JS name as the Android topic bridge.
/// Firebase Messaging is not linked until the owner adds GoogleService-Info.plist
/// and the Firebase Apple SDK, so this build does not crash on launch.
@objc(MiTopicsPlugin)
public class MiTopicsPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "MiTopicsPlugin"
    public let jsName = "MiTopics"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "subscribe", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "unsubscribe", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "isAvailable", returnType: CAPPluginReturnPromise)
    ]

    @objc func isAvailable(_ call: CAPPluginCall) {
        call.resolve(["firebaseOnClasspath": false])
    }

    @objc func subscribe(_ call: CAPPluginCall) {
        call.reject("Firebase Messaging is not linked. Add GoogleService-Info.plist and the Firebase Apple SDK, then rebuild.")
    }

    @objc func unsubscribe(_ call: CAPPluginCall) {
        call.reject("Firebase Messaging is not linked. Add GoogleService-Info.plist and the Firebase Apple SDK, then rebuild.")
    }
}
