#include <Python.h>
#include <cstring>
#include <iostream>
#include <math.h> 
//#include "/usr/local/Cellar/python3/3.6.3/Frameworks/Python.framework/Versions/3.6/include/python3.6m/Python.h"
#include <vector>

using namespace std;

#ifdef __cplusplus
extern "C" double logarithm(unsigned a)
#else
double logarithm(unsigned a)
#endif
{
	if (a != 0)
	{
		return log2(a);
	}
	else
	{
		return 0;
	}
}

#ifdef __cplusplus
extern "C" double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
#else
double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
#endif
{
	long double N11 = 0;
	long double N10 = 0;
	long double N01 = 0;
	long double N00 = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(classes[j], class_) != NULL)
		{
//			cout << "class+" << endl;
			if(strstr(news[j], word) != NULL) 
			{
//				cout << "word+" << endl;
				N11 ++;
			}
			else 
			{
//				cout << "word-" << endl;
				N01 ++;
			}
		}
		else 
		{
//			cout << "class-" << endl;
			if(strstr(news[j], word) != NULL) 
			{
//				cout << "word+" << endl;
				N10 ++;
			}
			else 
			{
//				cout << "word-" << endl;
				N00 ++;
			}
		}
//		cout<< "N11 " << N11<<endl;
//		cout<< "N10 " << N10<<endl;
//		cout<< "N01 " << N01<<endl;
//		cout<< "N00 " << N00<<endl;
	}
	if((N11*N10*N00*N01) != 0)
	{
		long double N = N11+N10+N00+N01;
		long double N1x = N11+N10;
		long double Nx1 = N11 + N01;
		long double N0x = N01+N00;
		long double Nx0 = N10 + N00;
//		cout<< "N " << N<<endl;
//		cout<< "N1x " << N1x<<endl;
//		cout<< "Nx1 " << Nx1<<endl;
//		cout<< "N0x " << N0x<<endl;
//		cout<< "Nx0 " << Nx0<<endl;
//		cout << (N11/N) * log2((N*N11)/(N1x*Nx1)) << endl;
//		cout << (N01/N) * log2((N*N01)/(N0x*Nx1))<< endl;
//		cout << (N10/N) * log2((N*N10)/(N1x*Nx0)) << endl;
//		cout << (N00/N) * log2((N*N00)/(N0x*Nx0)) << endl;
//		cout << (((N11/N)*log2((N*N11)/(N1x*Nx1))) + ((N01/N) * log2((N*N01)/(N0x*Nx1))) + ((N10/N) * log2((N*N10)/(N1x*Nx0))) + ((N00/N) * log2((N*N00)/(N0x*Nx0))))<< endl << endl;
		return (((N11/N)*logarithm((N*N11)/(N1x*Nx1))) + ((N01/N) * logarithm((N*N01)/(N0x*Nx1))) + ((N10/N) * logarithm((N*N10)/(N1x*Nx0))) + ((N00/N) * logarithm((N*N00)/(N0x*Nx0))));
	}
	else
	{
	    if (N11 == 0)
		    return -1;
		else
		{
		    
		}
	}
//		PyList_Append(out, PyInt_FromLong(i));
}

#ifdef __cplusplus
extern "C" double mi_slow(unsigned long long* news, unsigned n2, char* class_, char** classes, unsigned long long word)
#else
double mi(unsigned long long* news, unsigned n2, char* class_, char** classes, unsigned long long word)
#endif
{
	long double N11 = 0;
	long double N10 = 0;
	long double N01 = 0;
	long double N00 = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(classes[j], class_) != NULL)
		{
//			cout << "class+" << endl;
			if(news[j] % word == 0) 
			{
				cout << "word+" << endl;
				N11 ++;
			}
			else 
			{
				cout << "word-" << endl;
				N01 ++;
			}
		}
		else 
		{
//			cout << "class-" << endl;
			if(news[j] % word == 0)  
			{
				cout << "word+" << endl;
				N10 ++;
			}
			else 
			{
				cout << "word-" << endl;
				N00 ++;
			}
		}
//		cout<< "N11 " << N11<<endl;
//		cout<< "N10 " << N10<<endl;
//		cout<< "N01 " << N01<<endl;
//		cout<< "N00 " << N00<<endl;
	}
	if((N11*N10*N00*N01) != 0)
	{
		long double N = N11+N10+N00+N01;
		long double N1x = N11+N10;
		long double Nx1 = N11 + N01;
		long double N0x = N01+N00;
		long double Nx0 = N10 + N00;
//		cout<< "N " << N<<endl;
//		cout<< "N1x " << N1x<<endl;
//		cout<< "Nx1 " << Nx1<<endl;
//		cout<< "N0x " << N0x<<endl;
//		cout<< "Nx0 " << Nx0<<endl;
//		cout << (N11/N) * log2((N*N11)/(N1x*Nx1)) << endl;
//		cout << (N01/N) * log2((N*N01)/(N0x*Nx1))<< endl;
//		cout << (N10/N) * log2((N*N10)/(N1x*Nx0)) << endl;
//		cout << (N00/N) * log2((N*N00)/(N0x*Nx0)) << endl;
//		cout << (((N11/N)*log2((N*N11)/(N1x*Nx1))) + ((N01/N) * log2((N*N01)/(N0x*Nx1))) + ((N10/N) * log2((N*N10)/(N1x*Nx0))) + ((N00/N) * log2((N*N00)/(N0x*Nx0))))<< endl << endl;
		return (((N11/N)*logarithm((N*N11)/(N1x*Nx1))) + ((N01/N) * logarithm((N*N01)/(N0x*Nx1))) + ((N10/N) * logarithm((N*N10)/(N1x*Nx0))) + ((N00/N) * logarithm((N*N00)/(N0x*Nx0))));
	}
	else
	{
	    if (N11 == 0)
		    return -1;
		else
		{
		    
		}
	}
//		PyList_Append(out, PyInt_FromLong(i));
}

int main()
{
	return 1;
}
#ifdef __cplusplus
extern "C" int count(char** arr, unsigned n2, char* word)
#else
int count(char** arr, unsigned n2, char* word)
#endif
{
//	cout << word << endl<<"-----------"<<endl;
	int out = 0;
	for(unsigned j = 0; j < n2; j++)
	{
//		cout << arr[j] << endl;
		if(strstr(arr[j], word) != NULL) {out ++;}
	}
	return out;
}

#ifdef __cplusplus
extern "C" PyObject* count_arr(char** arr, unsigned n2, char* word)
#else
PyObject* count_arr(char** arr, unsigned n2, char* word)
#endif
//extern "C" __declspec(dllexport) PyObject* _stdcall count_arr(char** arr, unsigned n2, char* word);
//PyObject* _stdcall count_arr(char** arr, unsigned n2, char* word)
{
	PyObject * PList = PyList_New(0);
	vector <int> intVector;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(arr[j], word) != NULL) {intVector.push_back(j);}
	}
	vector<int>::const_iterator it;
	for(it = intVector.begin(); it != intVector.end() ; it++ )
	{
		PyList_Append(PList, Py_BuildValue("i", *it));
	}
	return PList;
}