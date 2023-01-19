from abc import ABC, abstractmethod

class SensorHook(ABC):
    """
    Defines the interface for a sensor
    """

    @abstractmethod
    def __init__(self, addr):
        pass


    @abstractmethod
    async def read_sensor(self):
        """
        Reads the sensor value

        Returns invariant: Float
        """
        pass

