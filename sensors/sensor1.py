import eventlet
import os
from st2reactor.sensor.base import PollingSensor


class System_Sensor(PollingSensor):
    def __init__(self, sensor_service, config,poll_interval=5):
        super(System_Sensor, self).__init__(sensor_service=sensor_service, config=config,poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False

    def setup(self):
        pass

    def poll(self):
      
            self._logger.debug('System_Sensor dispatching trigger')
            payload = {'greeting': 'Yo, StackStorm!'}
            self.sensor_service.dispatch(trigger='new_proj.event1', payload=payload)
            
           

    def cleanup(self):
        pass

   
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

