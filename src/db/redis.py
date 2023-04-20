from redis.client import StrictRedis

from config import config


class RedisClient:
    __client: StrictRedis = None

    @property
    def client(self):
        if self.__client is None:
            self.__client = StrictRedis(
                host=config.redis.host,
                port=config.redis.port
            )
        return self.__client

    def close_connection(self):
        if self.__client:
            self.__client.close()
