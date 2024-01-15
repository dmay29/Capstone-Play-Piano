/**
 * 2024 PLAY Piano Capstone Group
 */

#include "playp_base/return_code.h"
#include "key_control.h"

namespace playp { namespace control {

    class KeyControlBuilder {
    public:
        //! @brief Creates a key control object
        //! @param status the status of creating the key control object
        //! @param mock creates a mock key control if true, false by default
        //! @returns a shared pointer to the key control object or nullptr is creating the object failed
        static IKeyControl::SharedPtr createKeyControl(playp::ReturnCode& status, const bool mock = false);
    };

}} // playp::control