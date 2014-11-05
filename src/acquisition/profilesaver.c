#include "Python.h"
#include "numpy/arrayobject.h"

static PyObject* hydrate (PyObject *dummy, PyObject *args)
{
    char *filename;
    FILE *file_ptr;
    int size;
    int ret;
    double *c_array = NULL;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;

    file_ptr=fopen(filename,"rb");
    if (!file_ptr)
    {
        printf("Unable to open file!");
        return Py_None;
    }
    fseek(file_ptr, 0L, SEEK_END);
    size = ftell(file_ptr)/sizeof(double *);
    fseek(file_ptr, 0L, SEEK_SET);
    c_array = (double *)malloc(sizeof(double *)*size+1);
    ret = fread(c_array, sizeof(double *), size, file_ptr);
    fclose(file_ptr);
    if (ret == 0)
        return NULL;
//    int j=0;
//    for (j=0;j<size;j++){
//        printf("c_array[%d] = %f\n",j,c_array[j]);
//    }

    npy_intp dim[1] = {size};
    PyArrayObject *array = (PyArrayObject *) PyArray_SimpleNew(1, dim, PyArray_INT);

    // fill the data
    int    *buffer = (int*)array->data;
    int    i;
    for (i =0; i<size; i++){
        buffer[i] = c_array[i];
    }
    return PyArray_Return(array);
}

static PyObject* saver (PyObject *dummy, PyObject *args)
{
    PyObject *arg1=NULL;
    PyObject *array=NULL;
    FILE * file_ptr;
    char *filename;

    if (!PyArg_ParseTuple(args, "Os", &arg1, &filename))
        return NULL;

    array = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
    if (array == NULL)
        return NULL;

    int size = PyArray_SIZE(array);
    double *c_array = (double*)PyArray_DATA(array);
//    int i =0;    
//    for (i=0; i < 15; i++){
//        printf("c_array[%d] =  %f\n",i,c_array[i]);
//    }
    file_ptr = fopen(filename, "wb"); 
    if (file_ptr != NULL) 
    {
        fwrite(c_array, sizeof(double *), size, file_ptr);
        fclose(file_ptr);
    }
    else
        printf("failed to create the file!\n");

    Py_DECREF(array);
    return Py_None;
}

static struct PyMethodDef methods[] = {
    {"saver", saver, METH_VARARGS, "saver(numpy.array,string)\nsaves numpy.array into a file, give its filename"},
    {"hydrate", hydrate, METH_VARARGS, "hydrate(string)\nreturns a numpy.array from a file, the file should be created with profilesaver.saver\nhydrate receive as parameter a filename"},
    {NULL, NULL, 0, NULL}
};

    PyMODINIT_FUNC
initprofilesaver (void)
{
    (void)Py_InitModule("profilesaver", methods);
    import_array();
}
