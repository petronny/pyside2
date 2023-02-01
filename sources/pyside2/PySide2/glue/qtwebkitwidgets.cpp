/****************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of Qt for Python.
**
** $QT_BEGIN_LICENSE:COMM$
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** $QT_END_LICENSE$
**
****************************************************************************/

// @snippet qwebview-page
auto _pyReturn = reinterpret_cast<SbkObject *>(%PYARG_0);
if (!Shiboken::Object::hasParentInfo(_pyReturn))
    Shiboken::Object::setParent(%PYSELF, %PYARG_0);
// @snippet qwebview-page

// @snippet qwebelementcollection-len
return %CPPSELF.count();
// @snippet qwebelementcollection-len

// @snippet qwebelementcollection-getitem
if (_i < 0 || _i >= %CPPSELF.count()) {
    PyErr_SetString(PyExc_IndexError, "index out of bounds");
    return 0;
}
QWebElement element = %CPPSELF.at(_i);
return %CONVERTTOPYTHON[QWebElement](element);
// @snippet qwebelementcollection-getitem

// @snippet qwebpage-qt-metacall
static int _signalIndex = -1;
static QMetaMethod _m;

if (_signalIndex == -1) {
    _signalIndex = QWebPage::staticMetaObject.indexOfSlot("shouldInterruptJavaScript()")
    _m = QWebPage::staticMetaObject.method(_signalIndex);
}

if (_signalIndex == id) {
    Shiboken::GilState gil;
    auto self = reinterpret_cast<PyObject *>(Shiboken::BindingManager::instance().retrieveWrapper(this));

    if (self) {
        Shiboken::AutoDecRef _pyMethod(PyObject_GetAttrString(self, "shouldInterruptJavaScript"));
        return PySide::SignalManager::callPythonMetaMethod(_m, args, _pyMethod, false);
    }
}
// @snippet qwebpage-qt-metacall

// @snippet qwebframe-metadata
%PYARG_0 = PyDict_New();
const auto &keys = %0.keys();
for (const auto &_key : keys) {
    Shiboken::AutoDecRef _pyValueList(PyList_New(0));
    for (auto it = %0.lowerBound(key), end = %0.upperBound(key); it ! = end; ++it) {
        Shiboken::AutoDecRef _pyValue(%CONVERTTOPYTHON[QString](it.value));
        PyList_Append(_pyValueList, _pyValue);
    }

    Shiboken::AutoDecRef _pyKey(%CONVERTTOPYTHON[QString](_key));
    PyDict_SetItem(%PYARG_0, _pyKey, _pyValueList);
}
// @snippet qwebframe-metadata
