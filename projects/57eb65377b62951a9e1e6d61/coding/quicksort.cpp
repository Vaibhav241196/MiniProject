#include<stdio.h>
using namespace std;

void quicksort(int[],long,long);

int main()
{
    long n;
    scanf("%ld",&n);
    int *mat = new int[n];
    for(long i=0;i<n;++i)
        scanf("%d",&mat[i]);
    quicksort(mat,0,n);
    for(long i=0;i<n;++i)
        printf("%d",mat[i]);
    
    return 0;
}

void quicksort(int t[],long a,long b)		//the matrix is from a to b-1
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
		//total = total+t[j]*j-(b-j-1)*t[j];
		quicksort(t,a,j);
		quicksort(t,j+1,b);
	}
	if(i==j&&t[a]>t[i])
	{
		temp=t[i];
		t[i]=t[a];
		t[a]=temp;
	}
}
