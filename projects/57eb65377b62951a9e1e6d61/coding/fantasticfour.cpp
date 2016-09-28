#include<iostream>
using namespace std;

int main()
{
int i,j,id,grid[7][8];
for(i=0;i<7;++i)
    for(j=0;j<8;++j)
        scanf("%d",&grid[i][j]);
scanf("%d",&id);
for(i=0;i<8;++i)
{
    if(grid[0][i]==0)
    {
        pritnf("%d",i);
        break;
    }
}
return 0;
}
