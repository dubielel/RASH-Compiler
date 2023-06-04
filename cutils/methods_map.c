#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "methods_map.h"

METHODS_MAP* init_methods_map(int size) {
    METHODS_MAP* m_map = (METHODS_MAP*) malloc(sizeof(METHODS_MAP));
    m_map->size = size;
    m_map->count = 0;
    m_map->methods = (METHODS_MAP_ELEMENT*) malloc(sizeof(METHODS_MAP_ELEMENT));

    return m_map;
}

void delete_methods_map(METHODS_MAP* methods_map) {
    free(methods_map->methods);
    free(methods_map);
}

func call_method_methods_map(METHODS_MAP* methods_map, char* element_key) {
    int i;
    for (i = 0; i < methods_map->count; i++) {
        if (strcmp(element_key, methods_map->methods[i].key) == 0)
            return methods_map->methods[i].function;
    }

    return NULL;
}

void insert_methods_map(METHODS_MAP* methods_map, char* element_key, func element_function) {
    if (methods_map->size == methods_map->count) {
        printf("Methods map full");
        return;
    }

    methods_map->methods[methods_map->count].key = strdup(element_key);
    methods_map->methods[methods_map->count].function = element_function;
    methods_map->count++;
}



