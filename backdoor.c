#include <stdio.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define SERVER "watchersnet.ddns.net"
#define PORT 9904


void log(char* message)
{
    fprintf(stderr, message);
}

int main(int argc, char* argv[])
{
    WSADATA wsa;
    SOCKET sock;

    /* Start the socket */
    if(WSAStartup(MAKEWORD(2,2), &wsa) != 0)
    {
        log("Error: cannot initialize winsock.");
        return -1;
    }

    if((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET)
    {
        log("Error: cannot start socket.");
        return -1;
    }

    while(1 == 1)
    {

    }
    return 0;
}
