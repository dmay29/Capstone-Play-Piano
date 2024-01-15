/**
 * 2024 PLAY Piano Capstone Group
 */

#include <iostream>

#include "playp_base/led_color.h"
#include "playp_base/return_code.h"
#include "playp_key_control/key_control.h"
#include "playp_key_control/key_control_builder.h"


using namespace playp;
using namespace playp::control;

int main () {
    ReturnCode ret = { 0, "" };

    auto key_ctrl = KeyControlBuilder::createKeyControl(ret, true);
    if (ret.error != 0) {
        std::cout << "Failed to create key control object: " << ret.message << std::endl;
    } else {
        std::cout << "Created mock key control" << std::endl;
    }

    // Set the first LED on the first key to purple
    ret = key_ctrl->setLEDColor(0, 0, { 255, 0, 255 });
    if (ret.error != 0) {
        std::cout << "Failed to set LED color on mock: " << ret.message << std::endl;
    } else {
        std::cout << "Successfully set LED color on mock" << std::endl;
    }

}