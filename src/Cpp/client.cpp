#include "lib/Client.h"
#include <iostream>
#include <vector>

// int main(int argc, char* argv[])
// zad1
// { 
//     std::vector<std::string> messages{"abc1", "0001", "hello", "world", "QUIT", "Hmmm?"};
//     std::string ip = "127.0.0.1";
//     int port = 2137;
//     if(argc > 2){
//         ip = argv[1];
//         port = atoi(argv[2]);
//     }
//     std::cout << ip << " " << port << std::endl;
//     Client* cl;
//     try{
//         cl = new Client(ip, port);
//     } catch (const std::exception& e){
//         std::cout << e.what() << std::endl;
//     }
//     for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
//         try{
//             cl->SendString(*it);
//             } catch (const std::exception& e){
//             std::cout << e.what() << std::endl;
//             }
//     }
//     delete cl;
// }

int main(int argc, char* argv[])
// zad 1.2
{ 
    
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    std::cout << ip << " " << port << std::endl;
    try{
        Client cl(ip, port);
    
    int iter = 0;
    while (1) {
        std::string mess(2 << iter, 'a');
        cl.SendString(mess);
        iter++;
        }
    }  
    catch (const std::exception& e){
            std::cout << e.what() << std::endl;
            
    }
}


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
//         Client cl(ip, port);
//         cl.SendStruct(s);
//     }  
//     catch (const std::exception& e){
//             std::cout << e.what() << std::endl;
            
//     }
// }