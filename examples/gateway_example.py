from py_micro_services.gateway import Gateway, GatewayConfig

if __name__ == "__main__":

    config = GatewayConfig.load("config/gateway_config.json")

    server = Gateway(config)
    server.start()