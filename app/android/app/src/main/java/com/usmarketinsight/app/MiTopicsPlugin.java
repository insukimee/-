package com.usmarketinsight.app;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.lang.reflect.Proxy;

/**
 * Thin FCM topic bridge. Firebase Messaging is added to the Gradle
 * classpath only when google-services.json exists, so this class talks to
 * it through reflection and the debug app still launches without Firebase.
 */
@CapacitorPlugin(name = "MiTopics")
public class MiTopicsPlugin extends Plugin {

    @PluginMethod
    public void subscribe(PluginCall call) {
        invoke("subscribeToTopic", call);
    }

    @PluginMethod
    public void unsubscribe(PluginCall call) {
        invoke("unsubscribeFromTopic", call);
    }

    @PluginMethod
    public void isAvailable(PluginCall call) {
        JSObject result = new JSObject();
        result.put("firebaseOnClasspath", firebasePresent());
        call.resolve(result);
    }

    private boolean firebasePresent() {
        try {
            Class.forName("com.google.firebase.messaging.FirebaseMessaging");
            return true;
        } catch (ClassNotFoundException exception) {
            return false;
        }
    }

    private void invoke(String method, PluginCall call) {
        String topic = call.getString("topic");
        if (topic == null || topic.isEmpty()) {
            call.reject("topic is required");
            return;
        }
        if (!firebasePresent()) {
            call.reject("Firebase Messaging is not in this build. Add android/app/google-services.json and rebuild.");
            return;
        }
        try {
            Class<?> messagingClass = Class.forName("com.google.firebase.messaging.FirebaseMessaging");
            Object messaging = messagingClass.getMethod("getInstance").invoke(null);
            Object task = messagingClass.getMethod(method, String.class).invoke(messaging, topic);
            Class<?> listenerClass = Class.forName("com.google.android.gms.tasks.OnCompleteListener");
            Object listener = Proxy.newProxyInstance(
                listenerClass.getClassLoader(),
                new Class<?>[] { listenerClass },
                (proxy, proxyMethod, args) -> {
                    if ("onComplete".equals(proxyMethod.getName()) && args != null && args.length > 0) {
                        Object completed = args[0];
                        boolean successful = (Boolean) completed.getClass().getMethod("isSuccessful").invoke(completed);
                        if (successful) {
                            call.resolve();
                        } else {
                            Object error = completed.getClass().getMethod("getException").invoke(completed);
                            call.reject(error == null ? "topic request failed" : error.toString());
                        }
                    }
                    return null;
                }
            );
            task.getClass().getMethod("addOnCompleteListener", listenerClass).invoke(task, listener);
        } catch (Throwable error) {
            call.reject(error.getMessage() == null ? "topic request failed" : error.getMessage());
        }
    }
}
