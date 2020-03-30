function too_close () {
    basic.showIcon(IconNames.Sad)
    pins.digitalWritePin(DigitalPin.P1, 1)
    music.playTone(587, music.beat(BeatFraction.Half))
    music.playTone(784, music.beat(BeatFraction.Half))
    pins.digitalWritePin(DigitalPin.P1, 0)
}
function check_distance () {
    pins.digitalWritePin(DigitalPin.P2, 0)
    control.waitMicros(20)
    pins.digitalWritePin(DigitalPin.P2, 1)
    control.waitMicros(20)
    pins.digitalWritePin(DigitalPin.P2, 0)
    Distance = Math.idiv(pins.pulseIn(DigitalPin.P8, PulseValue.High), 58)
}
function warning () {
    basic.showLeds(`
        . # # # .
        . # # # .
        . . # . .
        . . . . .
        . . # . .
        `)
    pins.digitalWritePin(DigitalPin.P16, 1)
    music.playTone(262, music.beat(BeatFraction.Whole))
    pins.digitalWritePin(DigitalPin.P16, 0)
}
let Distance = 0
basic.showString("7")
basic.forever(function () {
    check_distance()
    if (Distance < 10) {
        if (Distance != 0) {
            too_close()
        } else {
            // 0 is probably due to a wrong connection
            basic.showString("Error!")
        }
    } else {
        if (Distance < 30) {
            warning()
        } else {
            basic.showIcon(IconNames.Happy)
        }
    }
})
