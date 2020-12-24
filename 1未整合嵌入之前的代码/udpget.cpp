#include<stdio.h>
#include<stdlib.h>
#include<pcap.h>
#include<errno.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<netinet/in.h>
struct ethernet
{
    u_int8_t src_address[6];
    u_int8_t dst_address[6];
    u_int16_t type;
};
struct ip_header
{
    u_int8_t head_length:4,version:4;
    u_int8_t tos;
    u_int16_t length;
    u_int16_t mark;
    u_int16_t offset;
    u_int8_t ttl;
    u_int8_t protocol;
    u_int16_t crc;
    u_int8_t src_address[4];
    u_int8_t dst_address[4];
};
struct udp_head{
    u_int16_t src_port;
    u_int16_t dst_port;
    u_int16_t len;
    u_int16_t crc;
};
struct dns_header{
    u_int16_t id;
    u_int16_t flags;
    u_int16_t question_num;
    u_int16_t answer_num;
    u_int16_t ana;
    u_int16_t addtion;
};
struct s_string{
    char *a;
    int length;
    s_string(){
        length=0;
    }
    void add(char x){
        if(length==0){
            a=(char * )malloc(sizeof(char));
        }else{
            a=(char * )realloc(a,(length+1)*sizeof(char));
        }
        a[length++]=x;
    }
    void display(){
        for(int i=0;i<length-1;++i)
            printf("%c",a[i]);
        printf("\n");
    }
};
pcap_t*t;
void dns_callback(u_char *argument,const struct pcap_pkthdr*pkthdr_head,const u_char *packet_content)
{
    dns_header *dns=(dns_header*)packet_content;
 //   printf("dns id is %04x\n",ntohs(dns->id));
    int flag=dns->flags&0x8000;
    bool mark=false;
    if(flag==0){
        mark=true;
       // printf("this is dns request\n");
        u_char * c=(u_char *)packet_content+12;
        struct s_string s;
        while(true){
            u_int8_t num=*c;
            if(num==0x00)
                break;
            ++c;
            for(int i=0;i<num;++i){
              s.add(*c);
                ++c;
            }
            s.add('.');
        }
        s.display();
    }
    if(mark){
        pcap_breakloop(t);
    }

}
void udp_callback(u_char *argument,const struct pcap_pkthdr*pkthdr_head,const u_char *packet_content)
{
    udp_head * udp=(udp_head*)packet_content;
    udp->src_port=ntohs(udp->src_port);
  //  printf("src port is :%d\n",udp->src_port);
    udp->dst_port=ntohs(udp->dst_port);
  //  printf("dst port is :%d\n",udp->dst_port);
    udp->len=ntohs(udp->len);
  //  printf("len is %d\n",udp->len);
    switch(udp->dst_port)
    {
      /*  case 138:printf("this is data-netbios \n");break;
        case 137:printf("this is netbios \n");break;
        case 139:printf("this is netbios-meeting\n");break;
        */
        case 53 :
            //printf("this is DNS server \n");
            dns_callback(argument,pkthdr_head,packet_content+8);
            break;
        default:break;
    }
}
void ip_callback(u_char *argument,const struct pcap_pkthdr*pkthdr_head,const u_char *packet_content)
{
    ip_header*ip=(ip_header*)packet_content;
    /*
    printf("%d\n",ip->head_length);
    printf("ip 唯一标识是:%04x\n",ntohs(ip->mark));
    printf("src ip is :");
    for(int i=0;i<4;++i)
        if(i!=3)
            printf("%d:",ip->src_address[i]);
        else
            printf("%d\n",ip->src_address[i]);
    printf("dst ip is :");
    for(int i=0;i<4;++i)
        if(i!=3)
            printf("%d:",ip->dst_address[i]);
        else
            printf("%d\n",ip->dst_address[i]);
    */
    if(ip->protocol==17){
        //printf("this is udp protocol\n");
        udp_callback(argument,pkthdr_head,packet_content+(ip->head_length*4));
    }

}
void callback(u_char *argument,const struct pcap_pkthdr*pkthdr_head,const u_char *packet_content)
{
    static int num=1;
    /*
    printf("---------------------------------\n");
    printf("%d packet handle\n",num++);
    */
    ethernet * enet=(ethernet *)packet_content;
    //printf("ethernet src address is:");
    /*
    for(int i=0;i<6;++i)
        if(i!=5)
            printf("%02x:",enet->src_address[i]);
        else
            printf("%02x\n",enet->src_address[i]);
    printf("ethernet dst address is:");
    for(int i=0;i<6;++i)
        if(i!=5)
            printf("%02x:",enet->dst_address[i]);
        else
            printf("%02x\n",enet->dst_address[i]);
    */
    enet->type=ntohs(enet->type);
    if(enet->type==0x0800)
        ip_callback(argument,pkthdr_head,packet_content+14);

}
int main()
{
    char *dev;
    bpf_u_int32 ip,mask;
    char error_content[PCAP_ERRBUF_SIZE];
    dev=pcap_lookupdev(error_content);
    pcap_lookupnet(dev,&ip,&mask,error_content);
    bpf_program programs;
    char *programs_string="dns";
    t=pcap_open_live(dev,BUFSIZ,0,0,error_content);
    pcap_compile(t,&programs,programs_string,0,ip);
    pcap_setfilter(t,&programs);
    pcap_loop(t,-1,callback,NULL);
    pcap_close(t);
    return 0;
}
