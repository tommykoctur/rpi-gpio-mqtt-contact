# rpi-gpio-mqtt-contact
This python script waiting for state change of specified GPIO pin (contact sensor - alarm).
On change, it will verify the signal and send message via MQTT to specified topic.
Multiple containers can run simultaneously with different env variables to setup gpio, topic etc...

## build docker image
```sh
docker build . -t rpi-gpio-mqtt-contact
```

## run docker container
```sh
docker run -d \
        -e GPIO_ID="26" \
        -e BROKER_IP="192.168.1.2" \
        -e BROKER_PORT="1883" \
        -e TOPIC="Home/Livingroom/window/contact" \
        -e AVAILABILITY_TOPIC="Home/Livingroom/window/availability" \
        -e MESSAGE_HIGH="open" \
        -e MESSAGE_LOW="closed" \
        -e MESSAGE_AVAILABLE="Online" \
        -e MESSAGE_UNAVAILABLE="Offline" \
        -e USER="mqtt_user" \
        -e PASSWORD="mqtt_password" \
        --device /dev/ttyAMA0:/dev/ttyAMA0 \
        --device /dev/mem:/dev/mem \
        --privileged \
        --name livingroom_light_sw \
        --restart always \
        rpi-gpio-mqtt-contact
```

##Acknowledgment
Thanks to Angel Castro Martinez, (https://github.com/kronos-cm) for docker multistage 
build recommendations for python projects.