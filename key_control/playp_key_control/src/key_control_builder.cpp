/**
 * 2024 PLAY Piano Capstone Group
 */

#include <memory>

#include "playp_key_control/key_control.h"
#include "mock_key_control_impl.h"
#include "playp_key_control/key_control_builder.h"

using namespace playp;
using namespace playp::control;

IKeyControl::SharedPtr KeyControlBuilder::createKeyControl(ReturnCode& status, const bool mock)
{
    if (mock) {
        status = { 0, "" };
        return std::make_shared<MockKeyControl>();
    }

    status = { -1, "NYI, only the mock implementation of key control is currently available" };
    return nullptr;
}