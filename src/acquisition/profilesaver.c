#include "Python.h"
#include "numpy/arrayobject.h"

    static PyObject*
hydrate (PyObject *dummy, PyObject *args)
{
    char *filename;
    npy_intp dim[2] = {10,10};
    PyArrayObject *array = (PyArrayObject *) PyArray_SimpleNew(2, dim, PyArray_INT);
    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;
    // fill the data
    int    *buffer = (int*)array->data;
    int    i;
    for (i =0; i<10*10; i++){
        buffer[i] = i;
    }
    return PyArray_Return(array);
}

    static PyObject*
saver (PyObject *dummy, PyObject *args)
{
    PyObject *arg1=NULL;
    PyObject *arr1=NULL;
    FILE * f;
    char *filename;

    if (!PyArg_ParseTuple(args, "Os", &arg1, &filename))
        return NULL;

    arr1 = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
    if (arr1 == NULL)
        return NULL;

    //nd = PyArray_NDIM(arr1);   //number of dimensions
    //double *da = (double *)PyArray_DATA(arr1);
    int nn = PyArray_SIZE(arr1);
    //printf("elem: %d\n", nn);
    //for (int i=0; i < nn; i++){
    //    printf("%f\n",da[i]);
    //}
    //printf("%s\n",filename);

    f = fopen(filename, "wb"); // wb -write binary
    if (f != NULL) 
    {
        //   printf("size: %lu\n",sizeof(arr1));
        fwrite(arr1, sizeof(arr1), nn, f);
        fclose(f);
    }
    else
    {
        //failed to create the file
        printf("failed!\n");
    }

    //    f = fopen("profile.dat","rb");
    //    while (!feof(f)) {
    //        printf("1:ok here!");
    //        fread(arr2, sizeof(arr2), 1, f);
    //        printf("2:ok here!");
    //        double *da = (double *)PyArray_DATA(arr2);
    //        int nn = PyArray_SIZE(arr2);
    //        for (int i=0; i < nn; i++){
    //            printf("%f\n",da[i]);
    //        }
    //    }


    Py_DECREF(arr1);
    return Py_None;//PyInt_FromLong(nd);
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
