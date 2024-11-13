//This script requires the sonar extension
let Distance = 0
basic.showIcon(IconNames.Snake)
basic.forever(function () {
    Distance = sonar.ping(
        DigitalPin.P0,
        DigitalPin.P1,
        PingUnit.Centimeters
    )
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
