#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define N  8//修改缓冲区
#define PRODUCT_NUM 15
int buffer[N], readpos = 0, writepos = 0;
sem_t full, empty,pmutex,cmutex;//增加信号量
void sleep_random(int t) {
  sleep((int)(t * (rand() / (RAND_MAX *1.0))));
}

void *produce(void *id){
  int i;
  for (i = 0; i < PRODUCT_NUM; i++){
    sleep_random(2);
    sem_wait(&empty);// 等待缓冲区有空闲位置
    sem_wait(&pmutex);// 保证在product时不会有其他线程访问缓冲区
    int myid = *(int *)id * 1000 + i + 1;
    buffer[writepos++] = myid;// 将新资源放到buffer[writepos]位置 
    if (writepos >= N)
      writepos = 0;
    printf("produce:    %d\n", myid);// 唤醒的顺序可以不同
    sem_post(&pmutex);// 通知consumer缓冲区有资源可以取走
    sem_post(&full);
  }
}

void *consume(){
  int i;
  for (i = 0; i < PRODUCT_NUM; i++){
    sleep_random(2);
    sem_wait(&full);// 等待缓冲区有资源可以使用
    sem_wait(&cmutex);// 保证在consume时不会有其他线程访问缓冲区
    printf("consume: %d\n", buffer[readpos]);// 将buffer[readpos]位置的资源取出
    buffer[readpos++] = - 1;// 重置buffer[out]位置的资源
    if (readpos >= N)
      readpos = 0;
    sem_post(&cmutex);// 唤醒的顺序可以不同
    sem_post(&empty);// 通知缓冲区有空闲位置
  }
}

int main(){
  int res, i,id[5];
  pthread_t t1[5];
  pthread_t t2[5];
  for (i = 0; i < N; i++)
    buffer[i] = i - 1;
  srand((int)time(0));
  sem_init(&full, 0, 0);
  sem_init(&empty, 0, N);
  sem_init(&pmutex, 0, 1);
  sem_init(&cmutex, 0, 1);

  //**********
  for(i = 0;i < 5;i++)
  {
    id[i]=i;
    pthread_create(&t1[i], NULL, produce, &id[i]);
  }
  for(i = 0; i < 5; i++)
    pthread_create(&t2[i],NULL,consume, &id[i]);
  for(i = 0;i < 5; i++)
  {
    pthread_join(t1[i],NULL);
    pthread_join(t2[i],NULL);
  }
//**********
  return 0;
}
