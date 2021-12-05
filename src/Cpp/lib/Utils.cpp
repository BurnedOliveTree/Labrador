#include "Utils.h"

namespace Utils{

std::vector<char> addHeader(char* ptr, size_t len_st, std::vector<char> vc){
    std::vector<char> result(ptr, ptr+len_st*sizeof(char));
    result.insert(result.end(), vc.begin(), vc.end());
    return result;
}

std::vector<char> addHeader(std::vector<char> st, std::vector<char> vc){
    std::vector<char> result = st;
    result.insert(result.end(), vc.begin(), vc.end());
    return result;
}

std::pair<std::vector<char>,std::vector<char>> divideHeader(size_t h_len, std::vector<char> vc){
    return std::make_pair(std::vector<char>(vc.begin(), vc.begin()+h_len),std::vector<char>(vc.begin()+h_len, vc.end()));
}

void printVector(std::vector<char> vc){
    std::cout << "VecSize: " << vc.size()<<"|\t";
    for(auto i = vc.begin(); i!= vc.end(); i++){
        std::cout << " " << unsigned(*i); 
    }
    std::cout << std::endl;
}

}