import mock

from st2tests.base import BaseSensorTestCase


from sensor1 import System_Sensor

class System_SensorTestCase(BaseSensorTestCase):
    sensor_cls = System_Sensor

    def test_poll(self):
        sensor = self.get_sensor_instance()

        sensor.poll()
        self.assertTriggerDispatched(trigger='new_proj.event1',
                                     payload={'Monitoring': 'Monitoring the System'})
