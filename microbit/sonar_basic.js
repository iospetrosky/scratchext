let Distance = 0
basic.showIcon(IconNames.Snake)
basic.forever(function () {
    pins.digitalWritePin(DigitalPin.P0, 0)
    basic.pause(2)
    pins.digitalWritePin(DigitalPin.P0, 1)
    basic.pause(2)
    pins.digitalWritePin(DigitalPin.P0, 0)
    Distance = Math.idiv(pins.pulseIn(DigitalPin.P1, PulseValue.High), 58)
    if (Distance < 10) {
        basic.showIcon(IconNames.Sad)
    } else {
        if (Distance < 30) {
            basic.showLeds(`
                . # # # .
                . # # # .
                . . # . .
                . . . . .
                . . # . .
                `)
        } else {
            basic.showIcon(IconNames.Happy)
        }
    }
})
