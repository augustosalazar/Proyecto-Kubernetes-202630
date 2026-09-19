#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc == 3 && strcmp(argv[1], "tabla") == 0) {
    int n = atoi(argv[2]);
    for (int i = 1; i <= 10; i++) printf("%d x %d = %d\n", n, i, n * i);
    return 0;
  }
  fprintf(stderr, "Uso: tabla <entero>\n");
  return 2;
}
