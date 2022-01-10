import subprocess
import RPi.GPIO as GPIO
import time
import click


@click.command()
@click.option('--gpio', required=True, help='RaspberryPi GPIO number', type=int)
@click.option('--broker_ip', required=True, help='MQTT broker ip', type=str)
@click.option('--broker_port', required=True, default="1883", help='MQTT broker port', type=str)
@click.option('--topic', required=True, help='MQTT topic', type=str)
@click.option('--availability_topic', required=True, help='MQTT availability topic', type=str)
@click.option('--message_high', required=True, help='MQTT message on GPIO HIGH', type=str)
@click.option('--message_low', required=True, help='MQTT message on GPIO LOW', type=str)
@click.option('--message_available', required=True, help='MQTT availability message ', type=str)
@click.option('--message_unavailable', required=True, help='MQTT unavailability message on GPIO LOW', type=str)
@click.option('--user', required=True, help='MQTT user name', type=str)
@click.option('--password', required=True, help='MQTT password', type=str)
def contact(gpio, broker_ip, broker_port, topic, availability_topic,
            message_high, message_low, message_available, message_unavailable, user, password):

    # configure variables
    gpio_id = gpio
    broker_ip = broker_ip
    broker_port = broker_port
    mqtt_topic = topic
    mqtt_availability_topic = availability_topic
    message_high = message_high
    message_low = message_low
    message_available = message_available
    message_unavailable = message_unavailable
    mqtt_user = user
    mqtt_password = password

    def state_online():
        subprocess.call(["mosquitto_pub",
                         "-h", broker_ip,
                         "-p", broker_port,
                         "-t", mqtt_availability_topic,
                         "-m", message_available,
                         "-u", mqtt_user,
                         "-P", mqtt_password])

    def state_offline():
        subprocess.call(["mosquitto_pub",
                         "-h", broker_ip,
                         "-p", broker_port,
                         "-t", mqtt_availability_topic,
                         "-m", message_unavailable,
                         "-u", mqtt_user,
                         "-P", mqtt_password])

    def state_open():
        subprocess.call(["mosquitto_pub",
                         "-h", broker_ip,
                         "-p", broker_port,
                         "-t", mqtt_topic,
                         "-m", message_high,
                         "-u", mqtt_user,
                         "-P", mqtt_password])
        state_online()

    def state_closed():
        subprocess.call(["mosquitto_pub",
                         "-h", broker_ip,
                         "-p", broker_port,
                         "-t", mqtt_topic,
                         "-m", message_low,
                         "-u", mqtt_user,
                         "-P", mqtt_password])
        state_online()

    GPIO.setmode(GPIO.BCM)
    # Setup GPIO - pull up to reduce interference
    GPIO.setup(gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set initial state
    if GPIO.input(gpio_id):
        prev_state = 1
        state_open()
    else:
        prev_state = 0
        state_closed()

    while True:
        # Wait for gpio state change
        GPIO.wait_for_edge(gpio_id, GPIO.BOTH, bouncetime=200)
        time.sleep(0.1)
        # Check if state is really changed (compare with previous state)
        if GPIO.input(gpio_id) == GPIO.HIGH and prev_state == 0:
            state_open()
            prev_state = 1

        if GPIO.input(gpio_id) == GPIO.LOW and prev_state == 1:
            state_closed()
            prev_state = 0

    state_offline()
    GPIO.cleanup()


if __name__ == '__main__':
    contact()
