/**
 * 2024 PLAY Piano Capstone Group
 */

#pragma once

#include <string>


namespace playp {

    //! @brief A structure for returning an error and message as the status of an operation
    //! @param error 0 for success, otherwise a use case defined non 0 int. Examples include -1 for a generic failure, or an errno
    //! @param message a human readable description of the error
    struct ReturnCode {
        int error;
        std::string message;
    };

} // namespace playp
