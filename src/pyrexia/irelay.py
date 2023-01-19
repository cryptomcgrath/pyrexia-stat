from abc import ABC, abstractmethod

class IRelay(ABC):
    """
    Defines the interface for a relay
    """

    @abstractmethod
    def command(self, onoff):
        """
        Turns the relay on or off 

        Parameter onoff - True to turn on, False to turn off
        """
        pass

    # returns if the relay is currently on (True) or off (False)
    @abstractmethod
    def is_on(self):
        """
        Returns the current state of the relay 
       
        Returns invariant: Boolean 
        True - on
        False - off
        """
        pass



