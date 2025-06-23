from py_micro_services.discovery_server import DiscoveryServer, DiscoveryServerConfig

if __name__ == "__main__":

    config = DiscoveryServerConfig.load("config/discovery_server_config.json")

    server = DiscoveryServer(config)
    server.start()