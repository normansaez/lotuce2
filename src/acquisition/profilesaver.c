#include "Python.h"
#include "numpy/arrayobject.h"

    static PyObject*
saver (PyObject *dummy, PyObject *args)
{
    PyObject *arg1=NULL;
    PyObject *arr1=NULL;
    int nd;
    FILE * f;

    if (!PyArg_ParseTuple(args, "O", &arg1))
        return NULL;

    arr1 = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
    if (arr1 == NULL)
        return NULL;

    nd = PyArray_NDIM(arr1);   //number of dimensions
    //double *da = (double *)PyArray_DATA(arr1);
    //int nn = PyArray_SIZE(arr1);
    //for (int i=0; i < nn; i++){
    //    printf("%f\n",da[i]);
    //}

    f = fopen("profile.dat", "wb"); // wb -write binary
    if (f != NULL) 
    {
        fwrite(arr1, sizeof(arr1), 1, f);
        fclose(f);
    }
    else
    {
        //failed to create the file
        printf("failed!\n");
    }

    Py_DECREF(arr1);
    return PyInt_FromLong(nd);
}

static struct PyMethodDef methods[] = {
    {"saver", saver, METH_VARARGS, "descript of saver"},
    {NULL, NULL, 0, NULL}
};

    PyMODINIT_FUNC
initopee (void)
{
    (void)Py_InitModule("opee", methods);
    import_array();
}
