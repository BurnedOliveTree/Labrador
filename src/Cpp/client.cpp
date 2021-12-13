#include "lib/SocketUDP.h"
#include "lib/SocketTCP.h"
#include "lib/Host.h"
#include <iostream>
#include <vector>

void printVariant(std::variant<std::string, SimpleStruct> msg){
    if(std::get_if<std::string>(&msg)){ 
        std::cout << "Received string message: " << std::get<std::string>(msg) << std::endl;
    }
    if(std::get_if<SimpleStruct>(&msg)){ 
        std::cout << "Received struct message: " << std::get<SimpleStruct>(msg).a << " " << unsigned(std::get<SimpleStruct>(msg).b) << " " << unsigned(std::get<SimpleStruct>(msg).c) << std::endl;
    }
}

int main(int argc, char* argv[])
// zad1
{ 
    std::vector<std::string> messages1{"abc1", "0001", "hello", "world", "QUIT", "Hmmm?"};
    std::vector<SimpleStruct> messages2{{300, 2,2}, {20, 1,50}}; 
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    std::cout << ip << " " << port << std::endl;
    SocketInterface* sockstring; 
    SocketInterface* sockstruct;
    Host* cl1;
    Host* cl2;
    try{
        // sockint = new SocketUDP(ip, port, false);
        sockstring = new SocketTCP(ip, port, false);
        sockstruct = new SocketTCP(ip, port, false);
        cl1 = new Host(sockstring);
        cl2 = new Host(sockstruct);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }
    try{
        cl1->Send(messages1[0]);
        printVariant(cl1->Receive());
        cl1->Send(messages1[1]);
        printVariant(cl1->Receive());
        cl2->Send(messages2[0]);
        printVariant(cl2->Receive());
        cl1->Send(messages1[2]);
        printVariant(cl1->Receive());
        cl1->Send(messages1[3]);
        printVariant(cl1->Receive());
        cl2->Send(messages2[1]);
        printVariant(cl2->Receive());
        cl1->Send(messages1[4]);
        printVariant(cl1->Receive());
        cl1->Send(messages1[5]);
        printVariant(cl1->Receive());

    } catch (const std::exception& e){
    std::cout << e.what() << std::endl;
    }

    delete cl1, cl2;
    delete sockstring, sockstruct;
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