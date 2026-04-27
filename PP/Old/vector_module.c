#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "vector_dot.h"

static PyObject* py_dot_product(PyObject* self, PyObject* args) {
    PyObject *list_a, *list_b;
    double a[VEC_LEN], b[VEC_LEN];

    if (!PyArg_ParseTuple(args, "OO", &list_a, &list_b)) return NULL;

    for (int i = 0; i < VEC_LEN; i++) {
        a[i] = PyFloat_AsDouble(PyList_GetItem(list_a, i));
        b[i] = PyFloat_AsDouble(PyList_GetItem(list_b, i));
    }

    DotResult res = dot_product(a, b);

    if (res.error) {
        PyErr_SetString(PyExc_ValueError, "Null pointer error in C");
        return NULL;
    }

    return PyFloat_FromDouble(res.result);
}

static PyMethodDef VectorMethods[] = {
    {"dot_product", py_dot_product, METH_VARARGS, "Вычисляет скалярное произведение"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef vectormodule = {
    PyModuleDef_HEAD_INIT,
    "vector_lib",
    NULL,
    -1,
    VectorMethods
};

PyMODINIT_FUNC PyInit_vector_lib(void) {
    return PyModule_Create(&vectormodule);
}
