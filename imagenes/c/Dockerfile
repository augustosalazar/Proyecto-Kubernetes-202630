FROM gcc:14 AS build
WORKDIR /app
COPY tareas.c .
RUN gcc -O2 -o tareas tareas.c

FROM alpine:3.21
COPY --from=build /app/tareas /usr/local/bin/tareas
ENTRYPOINT ["/usr/local/bin/tareas"]
