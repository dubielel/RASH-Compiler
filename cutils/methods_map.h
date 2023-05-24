typedef void* (*func)(void** args);
typedef struct methods_map_element METHODS_MAP_ELEMENT;
typedef struct methods_map METHODS_MAP;

struct methods_map_element
{
    char* key;
    func function;
};

struct methods_map
{
    METHODS_MAP_ELEMENT* methods;
    int count;
    int size;
};


METHODS_MAP* init_methods_map(int size); 
void delete_methods_map(METHODS_MAP* methods_map);
func call_method_methods_map(METHODS_MAP* methods_map, char* element_key);
void insert_methods_map(METHODS_MAP* methods_map, char* element_key, func element_function);
