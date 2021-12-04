#include<stdio.h>
#include<stdlib.h>
#include<math.h>
struct words
{
    char alpha;
    struct words* next;
};
 
int main()
{
    struct words *header,*last,*current;
    char method[6];
    char method_next[6];
    char now_alpha;
    for(int i=0;i<6;i++)
    {
        method[i]='\0';
        method_next[i]='\0';
    }
    header=(struct words*)malloc(sizeof(struct words));
    header->alpha='\0';
    last=header;
    while(scanf("%s",method)!=EOF)
    {
        if(method[0]=='i')
        {
            if(last==header)
            {
                scanf("%s",method_next);
                if(header->alpha=='\0')
                {
                    scanf("%c",&now_alpha);
                    scanf("%c",&now_alpha);
                    current=(struct words*)malloc(sizeof(struct words));
                    current->alpha=now_alpha;
                    header=current;
                    last=header;
                }else if(header->alpha!='\0')
                {
                    if(method_next[0]=='l'||method_next[0]=='1')
                    {
                        scanf("%c",&now_alpha);
                        scanf("%c",&now_alpha);
                        current=(struct words*)malloc(sizeof(struct words));
                        current->alpha=now_alpha;
                        header=current;
                        header->next=last;
                    }else if(method_next[0]=='r'||method_next[0]=='2')
                    {
                        scanf("%c",&now_alpha);
                        scanf("%c",&now_alpha);
                        current=(struct words*)malloc(sizeof(struct words));
                        current->alpha=now_alpha;
                        last=current;
                        header->next=last;
                    }
                }
            }else if(header!=last)
            {
                scanf("%s",method_next);
                if(method_next[0]=='l')
                {
                    scanf("%c",&now_alpha);
                    scanf("%c",&now_alpha);
                    current=(struct words*)malloc(sizeof(struct words));
                    current->alpha=now_alpha;
                    struct words *temp=header;
                    header=current;
                    header->next=temp;
                }else if(method_next[0]=='r')
                {
                    scanf("%c",&now_alpha);
                    scanf("%c",&now_alpha);
                    current=(struct words*)malloc(sizeof(struct words));
                    current->alpha=now_alpha;
                    last->next=current;
                    last=current;
                }else if(method_next[0]!='l'&&method_next[0]!='r')
                {
                    scanf("%c",&now_alpha);
                    scanf("%c",&now_alpha);
                    int insert_number=0;
                    int now=0;
                    while(method_next[now]!='\0')
                    {
                        insert_number=insert_number*10+method_next[now]-'0';
                        now++;
                    }
                    current=(struct words*)malloc(sizeof(struct words));
                    current->alpha=now_alpha;
                    int count=1;
                    struct words *temp=header;
                    if(insert_number==1)
                    {
                        struct words *temp=header;
                        header=current;
                        header->next=temp;
                    }else
                    {
                        while(1)
                        {
                            count++;
                            if(count>=insert_number||temp==last)
                            {
                                break;
                            }
                            temp=temp->next;
                        }
                        if(temp==last)
                        {
                            current->alpha=now_alpha;
                            last->next=current;
                            last=current;
                        }else
                        {
                            struct words *temp2=temp->next;
                            temp->next=current;
                            current->next=temp2;
 
                        }
                    }
                }
            }
        }else if(method[0]=='d')
        {
            if(header==last)
            {
                scanf("%s",method_next);
                header=(struct words*)malloc(sizeof(struct words));
                last=header;
                header->alpha='\0';
            }else if(header!=last)
            {
                scanf("%s",method_next);
                if(method_next[0]=='l')
                {
                    header=header->next;
                }else if(method_next[0]=='r')
                {
                    struct words *temp=header;
                    while(1)
                    {
                        if(temp->next==last)
                        {
                            break;
                        }
                        temp=temp->next;
                    }
                    temp->next=NULL;
                    last=temp;
                }else if(method_next[0]!='l'&&method_next[0]!='r')
                {
                    int now=0;
                    int delete_number=0;
                    while(method_next[now]!='\0')
                    {
                        delete_number=delete_number*10+method_next[now]-'0';
                        now++;
                    }
                    if(delete_number==1)
                    {
                        header=header->next;
                    }else
                    {
                        struct words *temp=header;
                        int count=1;
                        while(1)
                        {
                            count++;
                            if(count==delete_number||temp->next==last)
                            {
                                break;
                            }
                            temp=temp->next;
                        }
                        if(temp->next==last)
                        {
                            temp->next=NULL;
                            last=temp;
                        }else
                        {
                            struct words *temp2=temp->next;
                            temp->next=temp2->next;
                        }
                    }
                }
            }
        }
        for(int i=0;i<6;i++)
        {
            method[i]='\0';
            method_next[i]='\0';
        }
    }
    struct words *numbers_count=header;
    int count=1;
    if(header==last&&header->alpha=='\0')
    {
        printf("0");
        return 0;
    }else if(header==last&&header->alpha!='\0')
    {
        printf("%c 1",header->alpha);
    }else
    {
        while(1)
        {
            count++;
            if(numbers_count->next==last)
            {
                break;
            }
            numbers_count=numbers_count->next;
        }
        char answer[count];
        int answer_count[count];
        numbers_count=header;
        for(int i=0;i<count;i++)
        {
            answer_count[i]=0;
            answer[i]=numbers_count->alpha;
            if(i!=count-1)
            {
                numbers_count=numbers_count->next;
            }
        }
        for(int i=0;i<count;i++)
        {
            for(int ii=i;ii<count;ii++)
            {
                if(answer[i]==answer[ii])
                {
                    answer_count[i]++;
                }else
                {
                    break;
                }
            }
        }
        int max=0;
        for(int i=0;i<count;i++)
        {
            if(answer_count[i]>max)
            {
                max=answer_count[i];
            }
        }
        for(int i=0;i<count;i++)
        {
            if(answer_count[i]==max)
            {
                printf("%c ",answer[i]);
            }
        }
        printf("%d",max);
    }
    /*struct words* test=header;
    while(1)
    {
        printf("%c ",test->alpha);
        if(test==last)
        {
            break;
        }
        test=test->next;
    }*/
    return 0;
}
