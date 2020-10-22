#include <iostream>
#include <vector>
#include <cmath>
#include <chrono> 

using namespace std::chrono;

int main() {
    std::vector<int> squares;

    auto start = high_resolution_clock::now();
    for(size_t i(0); i <= 10'000'000; ++i) {
        squares.push_back(sqrt(i * i) + sqrt(i * i * i));
    }
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);

    std::cout << "0," << duration.count() << " seconds" << std::endl;

    return 0;
}
