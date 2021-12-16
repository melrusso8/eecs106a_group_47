#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define MESSAGE_FREQ 1

int sockfd, portno, n, choice = 1;
struct sockaddr_in serv_addr;
struct hostent *server;
char buffer[1];
uint port_num = 8088;
const char *host_name = "192.168.1.3"; // ---------> subject to change?
bool echoMode = true; //want terminal to read back values

// send characters to start and stop seed distrubution
char start_seed = 'y';
char stop_seed = 'n';


void error(const char *msg) {
    perror(msg);
    exit(0);
}

extern "C" int connect_to_mcu(){
    printf("%s\n", "Connection to ESP32...");
    portno = port_num;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    server = gethostbyname(host_name);
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(portno);


    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    printf("Successfully connected!");
    return(0);

}

extern "C" int distribute_seeds() {

    printf("%s\n", "Made it inside C file to distribute seeds...");
    printf("%c\n", start_seed);
    //write message to microntroller to begin seed distribution
    buffer[0] = 'a';
    while (buffer[0] != 'z') {
        n = write(sockfd, &start_seed, 1);

        if (n < 0) 
            error("ERROR writing to socket");
    //if (echoMode) {
	   bzero(buffer, 1);
	   n = read(sockfd,buffer, 1);
	   if (n < 0)
	       error("ERROR reading reply");
	   printf("%s\n", buffer);
    }
    buffer[0] = 'a';
    //}

    //zero out buffer
    //bzero(buffer, 1);

    //copy message to buffer to stop seed distribution
    //strcpy(buffer, stop_seed)
    //write message to microcontroller to stop seed distribution
    // n = write(sockfd, &stop_seed, 1);

    // if (n < 0) 
    //      error("ERROR writing to socket");
    // if (echoMode) {
    //     bzero(buffer, 1);
    //     n = read(sockfd,buffer, 1);
    //     if (n < 0)
    //         error("ERROR reading reply");
    //     printf("%s\n", buffer);
    // }

	return 0;
}
