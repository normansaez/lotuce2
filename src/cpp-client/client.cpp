//#include <iostream.h>
#include <control.hh>

int main(int argc, char** argv)
{

printf("test\n");
//  try {
//    // Initialise the ORB.
//    CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);
//
//    // Obtain a reference to the root POA.
//    CORBA::Object_var obj = orb->resolve_initial_references("RootPOA");
//    PortableServer::POA_var poa = PortableServer::POA::_narrow(obj);
//
//      // We allocate the object on the heap.  Since this is a reference
//      // counted object, it will be deleted by the POA when it is no
//      // longer needed.
//    Echo_i* myecho = new Echo_i();
//
//    // Activate the object.  This tells the POA that this object is
//    // ready to accept requests.
//    PortableServer::ObjectId_var myechoid = poa->activate_object(myecho);
//
//      // Obtain a reference to the object.
//    Echo_var myechoref = myecho->_this();
//
//    // Decrement the reference count of the object implementation, so
//    // that it will be properly cleaned up when the POA has determined
//    // that it is no longer needed.
//    myecho->_remove_ref();
//
//    // Obtain a POAManager, and tell the POA to start accepting
//    // requests on its objects.
//    PortableServer::POAManager_var pman = poa->the_POAManager();
//    pman->activate();
//
//    // Do the client-side call.
//    hello(myechoref);
//
//    // Clean up all the resources.
//    orb->destroy();
//  }
//  catch(CORBA::COMM_FAILURE& ex) {
//    cerr << "Caught system exception COMM_FAILURE -- unable to contact the "
//         << "object." << endl;
//  }
//  catch(CORBA::SystemException&) {
//    cerr << "Caught CORBA::SystemException." << endl;
//  }
//  catch(CORBA::Exception&) {
//    cerr << "Caught CORBA::Exception." << endl;
//  }
//  catch(omniORB::fatalException& fe) {
//    cerr << "Caught omniORB::fatalException:" << endl;
//    cerr << "  file: " << fe.file() << endl;
//    cerr << "  line: " << fe.line() << endl;
//    cerr << "  mesg: " << fe.errmsg() << endl;
//  }
//  catch(...) {
//    cerr << "Caught unknown exception." << endl;
//  }

  return 0;
}

