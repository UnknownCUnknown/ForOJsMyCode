#include <iostream>
#include<cstdio>
#include<algorithm>

using namespace std;

int main()
{
    int N,a[10005],i,head,tail;
    while(scanf("%d",&N) != EOF )
    {
        for(i = 0;i < N;i++)
            scanf("%d",&a[i]);
        head = 0;
        tail = N - 1;
        sort(a,a + N);
        int k = 0;
        while(tail >= head)
        {
            if(N - k == 2)
            {
            printf("%d ",a[head]);
            printf("%d\n",a[tail]);
            tail--;
            head++;
            }
            else
            {
                if(N - k == 1)
                {
                    printf("%d\n",a[head]);
                    head++;
                }
                else
                {
                    printf("%d ",a[tail]);
                    printf("%d ",a[head]);
                    tail--;
                    head++;
                    k += 2;
                }

            }

        }
    }

    return 0;
}
