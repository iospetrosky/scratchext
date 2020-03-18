basic.forever(function () {
    if (input.isGesture(Gesture.Shake)) {
        basic.showIcon(IconNames.Butterfly)
        serial.writeLine("Earthquake")
    }
})
/**
 * Micro:bit code to test the serial line and store data on the computer
 */
basic.forever(function () {
    if (Math.randomBoolean()) {
        basic.showIcon(IconNames.Happy)
        serial.writeLine("Testa")
    } else {
        basic.showIcon(IconNames.Sad)
        serial.writeLine("Croce")
    }
    serial.writeLine("Current light:" + input.lightLevel())
    serial.writeLine("Current temp :" + input.temperature())
    basic.pause(1000)
    basic.showIcon(IconNames.No)
    basic.pause(1000)
})
