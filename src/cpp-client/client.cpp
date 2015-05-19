#include <control.hh>
//#include <controlSK.cc>
#include <darc.h>
//#include <stdio.h>
//#include <stdlib.h>
#include <iostream>

using namespace std;
int main(int argc, char** argv)
{

    try {
        CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);
        CORBA::Object_var obj = orb->resolve_initial_references("RootPOA");
        RTC::Control_var controlref = RTC::Control::_narrow(obj);
    }
    catch(CORBA::COMM_FAILURE& ex) {
        cerr << "Caught system exception COMM_FAILURE -- unable to contact the "
            << "object." << endl;
    }
    catch(CORBA::SystemException&) {
        cerr << "Caught CORBA::SystemException." << endl;
    }
    catch(CORBA::Exception&) {
        cerr << "Caught CORBA::Exception." << endl;
    }
    catch(omniORB::fatalException& fe) {
        cerr << "Caught omniORB::fatalException:" << endl;
        cerr << "  file: " << fe.file() << endl;
        cerr << "  line: " << fe.line() << endl;
        cerr << "  mesg: " << fe.errmsg() << endl;
    }
    catch(...) {
        cerr << "Caught unknown exception." << endl;
    }
    std::cout << "hola\n";
    return 0;
}

