input.onButtonPressed(Button.A, function () {
    for (let one_letter of letters) {
        basic.showString("" + one_letter)
        basic.pause(500)
    }
})
input.onButtonPressed(Button.B, function () {
    basic.clearScreen()
    led.setBrightness(10)
    for (let X = 0; X <= 4; X++) {
        for (let Y = 0; Y <= 4; Y++) {
            led.plotBrightness(X, Y, led.brightness())
            led.setBrightness(led.brightness() + 5)
        }
    }
})
let letters: string[] = []
letters = ["a", "b", "!", "6"]
letters.push("Ciao")
led.setBrightness(119)
basic.showLeds(`
    # # # # #
    . . # . .
    . # # # .
    . . # . .
    # # # # #
    `)
