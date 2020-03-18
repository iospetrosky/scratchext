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
    serial.writeLine("Current light: " + input.lightLevel())
    serial.writeLine("Current temp : " + input.temperature() + " Celsius")
    basic.pause(1000)
    basic.showIcon(IconNames.No)
    basic.pause(1000)
})
basic.forever(function () {
    if (input.buttonIsPressed(Button.A)) {
        serial.writeLine("Button A")
    }
    if (input.buttonIsPressed(Button.B)) {
        serial.writeLine("Button B")
    }
})
