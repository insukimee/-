import Capacitor

class MarketInsightBridgeViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(MiTopicsPlugin())
    }
}
