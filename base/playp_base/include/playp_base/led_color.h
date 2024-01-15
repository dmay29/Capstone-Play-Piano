/**
 * 2024 PLAY Piano Capstone Group
 */

#pragma once

#include <cstdint>

namespace playp {

    //! @brief A representation of an RGB color for LEDs
    //! @param red a number 0-255 representing the intensity of the red component of the light 0 is off and 255 is full intensity
    //! @param red a number 0-255 representing the intensity of the green component of the light 0 is off and 255 is full intensity
    //! @param red a number 0-255 representing the intensity of the blue component of the light 0 is off and 255 is full intensity
    struct LEDColor {
        uint8_t red;
        uint8_t green;
        uint8_t blue;
    };

} // namespace playp