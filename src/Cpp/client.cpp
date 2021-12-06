#include "lib/SocketUDP.h"
#include "lib/SocketTCP.h"
#include "lib/Host.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[])
// zad1
{ 
    // std::vector<std::string> messages{"abc1", "0001", "hello", "world", "QUIT", "Hmmm?"};
    std::vector<SimpleStruct> messages{{300, 2,2}, {20, 1,50}}; 
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    std::cout << ip << " " << port << std::endl;
    SocketInterface* sockint;
    Host* cl;
    try{
        // sockint = new SocketUDP(ip, port, false);
        sockint = new SocketTCP(ip, port, false);
        cl = new Host(sockint);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }
    // for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
    for(std::vector<SimpleStruct>::iterator it = messages.begin(); it != messages.end(); ++it) {

        try{
            cl->Send(*it);
            } catch (const std::exception& e){
            std::cout << e.what() << std::endl;
            }
    }
    delete cl;
    delete sockint;
}

// int main(int argc, char* argv[])
// // zad 1.2
// { 
    
//     std::string ip = "127.0.0.1";
//     int port = 2137;
//     if(argc > 2){
//         ip = argv[1];
//         port = atoi(argv[2]);
//     }
//     std::cout << ip << " " << port << std::endl;
//     try{
//         Host cl(ip, port);
    
//     int iter = 0;
//     while (1) {
//         std::string mess(2 << iter, 'a');
//         cl.SendString(mess);
//         iter++;
//         }
//     }  
//     catch (const std::exception& e){
//             std::cout << e.what() << std::endl;
            
//     }
// }


// int main(int argc, char* argv[])
// // zad 2.2
// { 
//     struct SimpStruct s;
//     s.a = 20;
//     s.b = 2;
//     s.c = 8000;
//     std::string ip = "127.0.0.1";
//     int port = 2137;
//     if(argc > 2){
//         ip = argv[1];
//         port = atoi(argv[2]);
//     }
//     std::cout << ip << " " << port << std::endl;
//     try{
//         Host cl(ip, port);
//         cl.SendStruct(s);
//     }  
//     catch (const std::exception& e){
//             std::cout << e.what() << std::endl;
            
//     }
// }