/**
 * 2024 PLAY Piano Capstone Group
 */

#pragma once

#include <cstdint>
#include <memory>

#include "playp_base/return_code.h"
#include "playp_base/led_color.h"


namespace playp { namespace control {

    enum class KeyPosition : uint8_t {
        UP,
        DOWN
    };

    class IKeyControl {
    public:
        typedef std::shared_ptr<IKeyControl> SharedPtr;

        virtual ~IKeyControl() = default;

        //! @brief Sets the color of an LED within a key
        //! @param[in] keyIdx the index of the key, keys are 0 indexed from left to right
        //! @param[in] ledIdx the index of the LED within each key, LEDs are 0 indexed from top to bottom
        //! @param[in] color the color to set the LED to
        //! @returns the status of setting the LED color
        virtual playp::ReturnCode setLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, const playp::LEDColor& color) = 0;

        //! @brief Sets the color of an LED within a key
        //! @param[in] keyIdx the index of the key, keys are 0 indexed from left to right
        //! @param[in] ledIdx the index of the LED within each key, LEDs are 0 indexed from top to bottom
        //! @param[out] color the current color of the LED
        //! @returns the status of getting the LED color
        virtual playp::ReturnCode getLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, playp::LEDColor& color) = 0;

        //! @brief Sets the position of a key on the piano
        //! @param[in] keyIdx the index of the key, keys are 0 indexed from left to right
        //! @param[in] position the position to set the key to, up or down
        //! @param[in] durationMs the time interval in ms that the transition should occur over TODO: re-eval after deciding servo vs actuator 
        //! @returns the status of setting the key position
        virtual playp::ReturnCode setKeyPosition(const uint32_t keyIdx, const KeyPosition position, const uint32_t durationMs) = 0;

        //! @brief Gets the position of a key on the piano
        //! @param[in] keyIdx the index of the key, keys are 0 indexed from left to right
        //! @param[out] position the current position of the key, up or down
        //! @returns the status of getting the key position
        virtual playp::ReturnCode getKeyPosition(const uint32_t keyIdx, KeyPosition& position) = 0;

    };

}} // playp::control