/****************************************************************************
**
** Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt-project.org/legal
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
**     of its contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include <QtWidgets>

#include "window.h"

//! [0]
Window::Window(QWidget *parent)
    : QWidget(parent)
{
    confBrowseButton = createButton(tr("&Browse..."), SLOT(browse()));
    startButton = createButton(tr("&Start"), SLOT(goDarc()));
    startButton->setEnabled(false);
    cancelButton = createButton(tr("&Cancel"), SLOT(cancel()));

    homePath = QDir::homePath()+tr("/lotuce2/conf/");
    configFileComboBox = createComboBox(homePath);

    configFileLabel = new QLabel(tr("Darc Config File:"));

//! [0]

//! [1]
    QGridLayout *mainLayout = new QGridLayout;

    mainLayout->addWidget(configFileLabel, 0, 0);
    mainLayout->addWidget(configFileComboBox, 0, 1);
    mainLayout->addWidget(confBrowseButton, 0, 2);

    mainLayout->addWidget(cancelButton, 1, 2);
    mainLayout->addWidget(startButton, 1, 3);
    setLayout(mainLayout);

    setWindowTitle(tr("Lotuce2"));
    resize(700, 300);
}
//! [1]

//! [2]
void Window::browse()
{
    QString filename = QFileDialog::getOpenFileName(this,tr("config file"),QDir::homePath()+tr("/lotuce2/conf/"),tr("*.py (*.py)"));
    if (!filename.isEmpty()) {
        if (configFileComboBox->findText(filename) == -1)
            configFileComboBox->addItem(filename);
        configFileComboBox->setCurrentIndex(configFileComboBox->findText(filename));
        startButton->setEnabled(true);
    }
}


//! [3]
void Window::goDarc()
{
    QProcess process;
    process.startDetached("ls .");
}

QPushButton *Window::createButton(const QString &text, const char *member)
{
    QPushButton *button = new QPushButton(text);
    connect(button, SIGNAL(clicked()), this, member);
    return button;
}

QComboBox *Window::createComboBox(const QString &text)
{
    QComboBox *comboBox = new QComboBox;
    comboBox->setEditable(true);
    comboBox->addItem(text);
    comboBox->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
    return comboBox;
}

void Window::cancel(){
    Window::close();
}

