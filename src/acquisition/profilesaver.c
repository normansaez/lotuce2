#include "Python.h"
#include "numpy/arrayobject.h"
#include <aio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

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
    int file_ptr;
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
    file_ptr = open(filename, O_CREAT,S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH); 
    if (file_ptr != -1) 
    {
        struct aiocb asyncwr;
            asyncwr.aio_fildes = file_ptr;     /* File descriptor */
            asyncwr.aio_offset = 0;     /* File offset */
            asyncwr.aio_buf = c_array;        /* Location of buffer */
            asyncwr.aio_nbytes = size*sizeof(double);     /* Length of transfer */
            asyncwr.aio_reqprio = 0;    /* Request priority */
            asyncwr.aio_sigevent.sigev_notify = SIGEV_NONE;   /* Notification method */
            asyncwr.aio_lio_opcode = LIO_NOP; /* Operation to be performed; */

//        fwrite(c_array, sizeof(double *), size, file_ptr);
        aio_write(&asyncwr);
        close(file_ptr);
    }
    else
        printf("failed to create the file!\n");

    Py_DECREF(array);
    Py_INCREF(Py_None);
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
