#include <stdio.h>      /*标准输入输出定义*/
#include <stdlib.h>
#include <unistd.h>     /*Unix标准函数定义*/
#include <sys/types.h>  /**/
#include <sys/stat.h>   /**/
#include <sys/wait.h>	/*waitpid*/
#include <fcntl.h>      /*文件控制定义*/
#include <termios.h>    /*PPSIX终端控制定义*/
#include <errno.h>      /*错误号定�?*/
#include <getopt.h>
#include <string.h>
#include <linux/serial.h>
#define TIOCGRS485  0x542E
#define TIOCSRS485  0x542F
#define FALSE 1
#define TRUE 0


void rs485_enable(int fd, int enable )
{
struct serial_rs485  rs485conf;
if(ioctl(fd,TIOCGRS485,&rs485conf)<0)
	fprintf(stderr,"Error reading ioctl port(%d):%s\n",errno, strerror(errno));
else
	printf("Port currently RS485 mode is %s\n",(rs485conf.flags&SER_RS485_ENABLED)? "set":"Not set");
 if(enable)
  {
    printf("RS485 mode will be set\n");
    //rs485conf.flags|=SER_RS485_ENABLED|SER_RS485_RTS_ON_SEND;
    rs485conf.flags|=SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND;
	rs485conf.delay_rts_before_send=0;
	rs485conf.delay_rts_after_send=0;
  }
 else
 {
    printf("RS485 mode will disabled!\n");
    rs485conf.flags&=~SER_RS485_ENABLED;
 }
//set ioctl
if (ioctl(fd,TIOCSRS485,&rs485conf)<0)
	fprintf(stderr,"Error setting ioctl port(%d):%s\n",errno, strerror(errno));

	printf("Confirm RS485 mode is %s\n",(rs485conf.flags&SER_RS485_ENABLED)? "set":"Not set");
}

char *recchr="We received:\"";

int speed_arr[] = { 
	B921600, B460800, B230400, B115200, B57600, B38400, B19200, 
	B9600, B4800, B2400, B1200, B300, B38400, B19200, B9600, 
	B4800, B2400, B1200, B300, 
};
int name_arr[] = {
	921600, 460800, 230400, 115200, 57600, 38400,  19200,  
	9600,  4800,  2400,  1200,  300, 38400,  19200,  9600, 
	4800, 2400, 1200,  300, 
};

void set_speed(int fd, int speed)
{
	int   i;
	int   status;
	struct termios   Opt;
	tcgetattr(fd, &Opt);

	for ( i= 0;  i < sizeof(speed_arr) / sizeof(int);  i++) {
		if  (speed == name_arr[i])	{
			tcflush(fd, TCIOFLUSH);
			cfsetispeed(&Opt, speed_arr[i]);
			cfsetospeed(&Opt, speed_arr[i]);
			status = tcsetattr(fd, TCSANOW, &Opt);
			if  (status != 0)
				perror("tcsetattr fd1");
				return;
		}
		tcflush(fd,TCIOFLUSH);
   }
}
/*
	*@brief   设置串口数据位，停止位和效验�?	*@param  fd     类型  int  打开的串口文件句�?
	*@param  databits 类型  int 数据�?  取�?�?7 或�?*
	*@param  stopbits 类型  int 停止�?  取值为 1 或�?*
	*@param  parity  类型  int  效验类型 取值为N,E,O,,S
        *@param  flowctrl   类型 int 流控开�?取值为0�?
*/
int set_Parity(int fd,int databits,int stopbits,int parity,int flowctrl)
{
	struct termios options;
	if  ( tcgetattr( fd,&options)  !=  0) {
		perror("SetupSerial 1");
		return(FALSE);
	}
	options.c_cflag &= ~CSIZE ;
	switch (databits) /*设置数据位数*/ {
	case 7:
		options.c_cflag |= CS7;
	break;
	case 8:
		options.c_cflag |= CS8;
	break;
	default:
		fprintf(stderr,"Unsupported data size\n");
		return (FALSE);
	}
	
	switch (parity) {
	case 'n':
	case 'N':
		options.c_cflag &= ~PARENB;   /* Clear parity enable */
		options.c_iflag &= ~INPCK;     /* Enable parity checking */
	break;
	case 'o':
	case 'O':
		options.c_cflag |= (PARODD | PARENB);  /* 设置为奇效验*/
		options.c_iflag |= INPCK;             /* Disnable parity checking */
	break;
	case 'e':
	case 'E':
		options.c_cflag |= PARENB;     /* Enable parity */
		options.c_cflag &= ~PARODD;   /* 转换为偶效验*/ 
		options.c_iflag |= INPCK;       /* Disnable parity checking */
	break;
	case 'S':	
	case 's':  /*as no parity*/
		options.c_cflag &= ~PARENB;
		options.c_cflag &= ~CSTOPB;
	break;
	default:
		fprintf(stderr,"Unsupported parity\n");
		return (FALSE);
	}
 	/* 设置停止�?/  
  	switch (stopbits) {
   	case 1:
    	options.c_cflag &= ~CSTOPB;
  	break;
 	case 2:
  		options.c_cflag |= CSTOPB;
  	break;
 	default:
  		fprintf(stderr,"Unsupported stop bits\n");
  		return (FALSE);
 	}
	/* Set flow control */
	if (flowctrl)
		options.c_cflag |= CRTSCTS;
	else
		options.c_cflag &= ~CRTSCTS;

  	/* Set input parity option */
  	if (parity != 'n')
    	options.c_iflag |= INPCK;
  	options.c_cc[VTIME] = 150; // 15 seconds
    options.c_cc[VMIN] = 0;

	options.c_lflag &= ~(ECHO | ICANON);

  	tcflush(fd,TCIFLUSH); /* Update the options and do it NOW */
  	if (tcsetattr(fd,TCSANOW,&options) != 0) {
    	perror("SetupSerial 3");
  		return (FALSE);
 	}
	return (TRUE);
}

/**
	*@breif 打开串口
*/
int OpenDev(char *Dev)
{
	int fd = open( Dev, O_RDWR );         //| O_NOCTTY | O_NDELAY
 	if (-1 == fd) { /*设置数据位数*/
   		perror("Can't Open Serial Port");
   		return -1;
	} else
		return fd;
}


/* The name of this program */
const char * program_name;

/* Prints usage information for this program to STREAM (typically
 * stdout or stderr), and exit the program with EXIT_CODE. Does not
 * return.
 */

void print_usage (FILE *stream, int exit_code)
{
    fprintf(stream, "Usage: %s option [ dev... ] \n", program_name);
    fprintf(stream,
            "\t-h  --help     Display this usage information.\n"
            "\t-d  --device   The device ttyS[0-3] or ttyEXT[0-3]\n"
            "\t-s  --string   Write the device data\n"
	    "\t-f  --flow     Flow control switch\n"
	    "\t-b  --speed    Set speed bit/s\n"
	    "\t-e  --rs485    Enable rs485 mode!\n");
    exit(exit_code);
}



/*
	*@breif  main()
 */
int main(int argc, char *argv[])
{
    int  fd, next_option, havearg = 0;
    char *device = "/dev/ttyS1"; /* Default device */
	int speed = 115200;
	int flowctrl = 0;
	int enable=0;//RS485 enable selection!

 	int nread;			/* Read the counts of data */
 	char buff[512];		/* Recvice data buffer */
	pid_t pid;
	char *xmit = "1234567890"; /* Default send data */ 

    /*** ext Uart Test program ***/
    char recv_buff[512];
    unsigned long total = 0;
    unsigned long samecnt = 0;

    const char *const short_options = "hd:b:s:fe";

    const struct option long_options[] = {
        { "help",   0, NULL, 'h'},
        { "device", 1, NULL, 'd'},
        { "string", 1, NULL, 's'},
	{ "speed",  1, NULL, 'b'},
	{ "flow",   0, NULL, 'f'},
	{ "rs485",  0, NULL, 'e'},
        { NULL,     0, NULL, 0  }
    };

    program_name = argv[0];

    do {
        next_option = getopt_long (argc, argv, short_options, long_options, NULL);
        switch (next_option) {
            case 'h':
                print_usage (stdout, 0);
            case 'd':
                device = optarg;
				havearg = 1;
				break;
            case 's':
                xmit = optarg;
				havearg = 1;
				break;
			case 'b':
				speed = atoi (optarg);
				havearg = 1;
				break;
			case 'f':
				flowctrl = 1;
				break;
			case 'e':
                enable = 1;
				break;
            case -1:
				if (havearg)  break;
            case '?':
                print_usage (stderr, 1);
            default:
                abort ();
        }
    }while(next_option != -1);

 	sleep(1);
 	fd = OpenDev(device);

 	if (fd > 0) {
      	set_speed(fd,speed);
 	} else {
	  	fprintf(stderr, "Error opening %s: %s\n", device, strerror(errno));
  		exit(1);
 	}
	if (set_Parity(fd,8,1,'N', flowctrl)== FALSE) {
		fprintf(stderr, "Set Parity Error\n");
		close(fd);
      	exit(1);
   	}
  //add rs485 setting!
  if(enable>0)
	  rs485_enable(fd,enable);

	pid = fork();	
	if (pid < 0) { 
		fprintf(stderr, "Error in fork!\n"); 
    } else if (pid == 0){
		while(1) {
                        sleep (1);
			nread = read(fd, buff, sizeof(buff));
			if (nread > 0) {
				buff[nread] = '\0';
				printf("RECV: %s\n", buff);
			}
		}
		exit(0);
    } else { 
		while(1) {
			pid_t pr = waitpid(pid, NULL, WNOHANG);
			if(pr == pid) return 0;		// Success

			printf("SEND: %s\n",xmit);
			write(fd, xmit, strlen(xmit));

                        sleep (1);
		}
    }

    close(fd);
    exit(0);
}

