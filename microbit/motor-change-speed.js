input.onButtonPressed(Button.A, function () {
    speed = speed - 100
    if (speed < 100) {
        speed = 200
    }
    pins.analogWritePin(AnalogPin.P1, speed)
    basic.showString("" + speed)
})
input.onButtonPressed(Button.B, function () {
    pins.analogWritePin(AnalogPin.P1, speed)
    speed = speed + 100
    basic.showString("" + speed)
})
let speed = 0
basic.showString("B")
speed = 400
pins.analogWritePin(AnalogPin.P1, speed)
basic.forever(function () {
	
})