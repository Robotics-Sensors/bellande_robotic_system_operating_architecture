#include "common_msgs.hpp"
#include <iostream>
#include <chrono>
#include <thread>

class Example_package {
public:
    void run() {
        while (true) {
            // TODO: Implement node logic
            std::cout << "Running example_package" << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
};

int main(int argc, char** argv) {
    Example_package node;
    node.run();
    return 0;
}
