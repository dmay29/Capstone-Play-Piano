/**
 * 2024 PLAY Piano Capstone Group
 */

#pragma once

#include "playp_key_control/key_control.h"

namespace playp { namespace control {

    class MockKeyControl : public IKeyControl {
    public:
        MockKeyControl();

        ~MockKeyControl();

        playp::ReturnCode setLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, const playp::LEDColor& color) override;
        playp::ReturnCode getLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, playp::LEDColor& color) override;

        playp::ReturnCode setKeyPosition(const uint32_t keyIdx, const KeyPosition position, const uint32_t durationMs) override;
        playp::ReturnCode getKeyPosition(const uint32_t keyIdx, KeyPosition& position) override;

    };

}} // playp::control