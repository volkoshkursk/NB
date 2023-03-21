#include <Python.h>
#include <cstring>
#include <iostream>
#include <math.h> 
#include <vector>
#include <stdexcept>

using namespace std;

#ifdef __cplusplus
extern "C" double logarithm(double a)
#else
double logarithm(double a)
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
extern "C" long double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
#else
long double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
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
			if(strstr(news[j], word) != NULL) 
			{
				N11 ++;
			}
			else 
			{
				N01 ++;
			}
		}
		else 
		{
			if(strstr(news[j], word) != NULL) 
			{
				N10 ++;
			}
			else 
			{
				N00 ++;
			}
		}
	}
	if((N11*N10*N00*N01) != 0)
	{
		long double N = N11+N10+N00+N01;
		long double N1x = N11+N10;
		long double Nx1 = N11 + N01;
		long double N0x = N01+N00;
		long double Nx0 = N10 + N00;
		return (((N11/N)*logarithm((N*N11)/(N1x*Nx1))) + ((N01/N) * logarithm((N*N01)/(N0x*Nx1))) + ((N10/N) * logarithm((N*N10)/(N1x*Nx0))) + ((N00/N) * logarithm((N*N00)/(N0x*Nx0))));
	}
	else
	{
	    if (N11 == 0)
		    return -1;
		else
		{
		    throw logic_error( "received negative value" );
		}
	}
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
	int out = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(arr[j], word) != NULL) {out ++;}
	}
	return out;
}

#ifdef __cplusplus
extern "C" PyObject* count_arr(char** arr, unsigned n2, char* word)
#else
PyObject* count_arr(char** arr, unsigned n2, char* word)
#endif
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