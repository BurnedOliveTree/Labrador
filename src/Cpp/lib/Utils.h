#include <vector>
#include <iostream>
#include <string>
#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <optional>
#include <functional>


namespace Utils{

struct ex_struct{
    uint16_t a;
    uint8_t b;
    uint8_t c;
};   

template<typename T>
std::vector<char> serializeStruct(T s){
    size_t len_st = sizeof(s);
    char* ptr = reinterpret_cast<char*>(&s);
    std::vector<char> result(ptr, ptr+len_st*sizeof(char));
    return result;
}

template<typename T>
T deserializeStruct(std::vector<char> vc){
    T* st = reinterpret_cast<T*>(vc.data());
    return *st;
}

std::vector<char> serializeString(std::string s);
std::string deserializeString(std::vector<char> vc);



template<typename T>
std::vector<char> serialize(T s){
    if(std::is_same<T, std::string>::value || std::is_same<T, std::string>::value ){
        return serializeString(s);
    }
    return serializeStruct<T>(s);
}

template<typename T>
T deserialize(std::vector<char> s){
    if(std::is_same<T, std::string>::value){
        std::string buf = deserializeString(s);
        T* buff = reinterpret_cast<T*>(&buf);
        return *buff;
    }
    return deserializeStruct<T>(s);
}


template<typename T>
std::vector<char> addHeader(T st, std::vector<char> vc){
    size_t len_st = sizeof(st);
    char* ptr = reinterpret_cast<char*>(&st);
    std::vector<char> result(ptr, ptr+len_st*sizeof(char));
    result.insert(result.end(), vc.begin(), vc.end());
    return result;
}
std::vector<char> addHeader(char* ptr, size_t len_st, std::vector<char> vc);
std::vector<char> addHeader(std::vector<char> st, std::vector<char> vc);

std::pair<std::vector<char>,std::vector<char>> divideHeader(size_t h_len, std::vector<char> vc);

void printVector(std::vector<char> vc);






// Following is used for deception only. 
template<typename T = std::string>
std::vector<char> serializeString(T s){
    return std::vector<char>();
}
template<typename T = std::string>
T deserializeString(std::vector<char> vc){
    return T();
}
}