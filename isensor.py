from abc import ABC, abstractmethod

class ISensor(ABC):
    """
    Defines the interface for a sensor
    """

    @abstractmethod
    def can_update(self):
        """
        Returns True if the sensor is ready to be read, otherwise False

        Returns invariant: Boolean
        """
        pass

    @abstractmethod
    async def read_sensor(self):
        """
        Reads the sensor value

        Returns invariant: Float
        """
        pass

