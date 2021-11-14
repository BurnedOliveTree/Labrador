#include "Client.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[])
{
    std::vector<std::string> messages{"abc1", "0001", "hello", "world", "QUIT","Hmmm?"};
    char* ip = "127.0.0.1";
    if(argc > 1){
        ip = argv[1];
    }   
    Client cl(ip);
    for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
        cl.Send(*it);
    }

}

