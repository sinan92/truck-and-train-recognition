import config as config
from data import api


def main():
    api_thread = api.Api(config.HOST, config.PORT[0])
    api_thread.start()


if __name__ == '__main__':
    main()
