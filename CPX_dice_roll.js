// When button A is pressed, show a rainbow animation for a random amount of time, then reset each LED
input.buttonA.onEvent(ButtonEvent.Click, function () {
   light.showAnimation(light.rainbowAnimation, randint(500, 6000))
   light.setAll(0x000000)

   /* Simulate a single random dice roll, 1-4, with one LED group.
    Light up certain LED lights to correspond to that certain roll. */

   roll = randint(1, 4)
   if (roll == 1) {
    // LED 0 (red)
       light.setPixelColor(0, 0xff0000)
   } else if (roll == 2) {
    // LEDs 1 and 2 (green)
       light.setPixelColor(1, 0x00ff00)
       light.setPixelColor(2, 0x00ff00)
   } else if (roll == 3) {
    // LEDs 3, 4, and 5 (yellow)
       light.setPixelColor(3, 0xffff00)
       light.setPixelColor(4, 0xffff00)
       light.setPixelColor(5, 0xffff00)
   } else {
    // LEDs 6, 7, 8, and 9 (cyan)
       light.setPixelColor(6, 0x00ffff)
       light.setPixelColor(7, 0x00ffff)
       light.setPixelColor(8, 0x00ffff)
       light.setPixelColor(9, 0x00ffff)
   }

   // Play a power-up sound to signify successful roll
   music.powerUp.play()
})

// When button B is pressed, show a rainbow animation for a random amount of time, then reset each LED
input.buttonB.onEvent(ButtonEvent.Click, function () {
   light.showAnimation(light.rainbowAnimation, randint(500, 6000))
   light.setAll(0x000000)

   /* Simulate two random dice rolls, 1-4 each, with two LED groups.
    Light up certain LED lights to correspond to those certain rolls. */

   // First roll
   roll = randint(1, 4)
   if (roll == 1) {
    // Single LED lights up (red)
       light.setPixelColor(4, 0xff0000)
   } else if (roll == 2) {
    // Two LEDs light up (green)
       light.setPixelColor(4, 0x00ff00)
       light.setPixelColor(3, 0x00ff00)
   } else if (roll == 3) {
    // Three LEDs light up (yellow)
       light.setPixelColor(4, 0xffff00)
       light.setPixelColor(3, 0xffff00)
       light.setPixelColor(2, 0xffff00)
   } else {
    // Four LEDs light up (cyan)
       light.setPixelColor(4, 0x00ffff)
       light.setPixelColor(3, 0x00ffff)
       light.setPixelColor(2, 0x00ffff)
       light.setPixelColor(1, 0x00ffff)
   }

   // Second roll
   roll = randint(1, 4)
   if (roll == 1) {
    // Single LED lights up (red)
       light.setPixelColor(5, 0xff0000)
   } else if (roll == 2) {
    // Two LEDs light up (green)
       light.setPixelColor(5, 0x00ff00)
       light.setPixelColor(6, 0x00ff00)
   } else if (roll == 3) {
    // Three LEDs light up (yellow)
       light.setPixelColor(5, 0xffff00)
       light.setPixelColor(6, 0xffff00)
       light.setPixelColor(7, 0xffff00)
   } else {
    // Four LEDs light up (cyan)
       light.setPixelColor(5, 0x00ffff)
       light.setPixelColor(6, 0x00ffff)
       light.setPixelColor(7, 0x00ffff)
       light.setPixelColor(8, 0x00ffff)
   }

   // Play a pew-pew sound to signify successful rolls
   music.pewPew.play()
})

// Set initial roll to 0
let roll = 0
// Set all LEDs to a random color at start-up
light.setAll(light.rgb(randint(0, 255), randint(0, 255), randint(0, 255)))