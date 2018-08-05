#include <iostream>
#include "restc-cpp/restc-cpp.h"

using namespace restc_cpp;

int main() {
    auto rest_client = RestClient::Create();
    rest_client->CloseWhenReady(true);
    std::cout << "Test OK"; 
}
