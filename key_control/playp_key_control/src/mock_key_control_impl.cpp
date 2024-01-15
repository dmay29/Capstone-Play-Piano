/**
 * 2024 PLAY Piano Capstone Group
 */

#include "playp_base/led_color.h"
#include "playp_base/return_code.h"
#include "mock_key_control_impl.h"


using namespace playp;
using namespace playp::control;

MockKeyControl::MockKeyControl() {};

MockKeyControl::~MockKeyControl() {};

ReturnCode MockKeyControl::setLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, const LEDColor& color)
{
    return { 0, "" };
}

ReturnCode MockKeyControl::getLEDColor(const uint32_t keyIdx, const uint32_t ledIdx, LEDColor& color)
{
    return { 0, "" };
}

ReturnCode MockKeyControl::setKeyPosition(const uint32_t keyIdx, const KeyPosition position, const uint32_t durationMs)
{
    return { 0, "" };
}

ReturnCode MockKeyControl::getKeyPosition(const uint32_t keyIdx, KeyPosition& position)
{
    return { 0, "" };
}