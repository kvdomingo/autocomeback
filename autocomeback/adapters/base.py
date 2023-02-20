import abc


class BaseAdapter(abc.ABC):
    @abc.abstractmethod
    async def get_listings(self):
        pass

    @abc.abstractmethod
    async def get_data(self, url):
        pass

    @staticmethod
    @abc.abstractmethod
    async def sync_data(data):
        pass
