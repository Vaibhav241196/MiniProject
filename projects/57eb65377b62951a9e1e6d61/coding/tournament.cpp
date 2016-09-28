#include<stdio.h>
#include<algorithm>
using namespace std;
//void quicksort(int[],long,long);
int main()
{
    long long n,total = 0;
    scanf("%lld",&n);
    long long *strength = new long long[n];
    for(long i=0;i<n;++i)
        scanf("%lld",&strength[i]);
    //quicksort(strength,0,n-1);
    sort(strength,strength+n);
    for(long long i = 0;i<n;++i)
    {
        total = total+(n-1-2*i)*(strength[n-i-1]);
        //total = total+strength[i]*i-(n-i-1)*strength[i];
        //total = total+strength[n-i-1]*(n-i-1)-i*strength[n-i-1];
    }

    printf("%lld",total);
    delete[] strength;
    return 0;
}
/*void quicksort(int a[],long s,long b)
{
    //static long total;
	long pivot=s,i=s+1,j=b;
	int temp;
	if(i<=j)
	{
		while(i<=j)
		{
			while(a[pivot]>a[i])
				++i;
			while(a[pivot]<a[j])
				--j;
			if(i<j)
			{
				temp=a[i];
				a[i]=a[j];
				a[j]=temp;
			}
		}
			temp=a[pivot];
			a[pivot]=a[j];
			a[j]=temp;
			total = total+a[j]*j-(b-j)*a[j];
			quicksort(a,s,j-1);
			quicksort(a,j+1,b);
		}

}*/
//total = total+(strength[n-i-1]-strength[i])*(n-2*i-1);
/*void quicksort(int t[],long a,long b)		//the matrix is from a to b-1
{
	long i=a+1,j=b-1;
	int temp;
	while(i<j)
	{
		while(t[a]>t[i])			//equal to sign should come
			++i;
		while(t[a]<t[j])
			--j;
		if(i<j)
		{
			temp=t[i];
			t[i]=t[j];
			t[j]=temp;
			++i;
			--j;
		}
	}
	if(i>=j)
	{
		temp=t[j];
		t[j]=t[a];
		t[a]=temp;
		total = total+t[j]*j-(b-j-1)*t[j];
		quicksort(t,a,j);
		quicksort(t,j+1,b);
	}
	/*if(i==j&&t[a].id>t[i].id)
	{
		temp=t[i];
		t[i]=t[a];
		t[a]=temp;
	}*/

