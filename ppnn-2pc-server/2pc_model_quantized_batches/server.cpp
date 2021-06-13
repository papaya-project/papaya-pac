/*********************************************
Author: Mohamad Mansouri
Email: Mohamad.Mansouri@eurecom.fr
Date: 11/09/2018
**********************************************/

#include <ENCRYPTO_utils/crypto/crypto.h>
#include <ENCRYPTO_utils/parse_options.h>
#include <abycore/aby/abyparty.h>
#include <abycore/circuit/share.h>
#include <abycore/circuit/booleancircuits.h>
#include <abycore/circuit/arithmeticcircuits.h>

#include <abycore/sharing/sharing.h>
#include <cassert>
#include <iomanip>
#include <iostream>
#include <chrono>
#include "common/predict.h"
#include "common/utils.h"

using namespace std;

void read_test_options(int32_t* argcp, char*** argvp,
	uint32_t* secparam, string* address, uint16_t* port ,
	string* circuit, uint32_t* n_signal) {

	uint32_t int_port = 0;

	parsing_ctx options[] =
	{
	{(void*) n_signal, T_NUM, "i", "Input Size", true, false },
	{(void*) secparam, T_NUM, "s", "Symmetric Security Bits, default: 128", false, false },
	{(void*) address, T_STR, "a", "IP-address, default: localhost", false, false },
	{(void*) circuit, T_STR, "c", "circuit file name", false, false },
	{(void*) &int_port, T_NUM, "p", "Port, default: 7766", false, false }

	};

	if (!parse_options(argcp, argvp, options,
		sizeof(options) / sizeof(parsing_ctx))) {
		print_usage(*argvp[0], options, sizeof(options) / sizeof(parsing_ctx));
	cout << "Exiting" << endl;
	exit(0);
	}

	

	if (int_port != 0) {
		assert(int_port < 1 << (sizeof(uint16_t) * 8));
		*port = (uint16_t) int_port;
	}

}




int main(int argc, char** argv) {
	uint32_t  secparam = 128, nthreads = 1;

	uint16_t port = 7766;
	uint32_t n_sig = 1;
	string address = "127.0.0.1";
	string circuit = "none.aby";
	e_mt_gen_alg mt_alg = MT_OT;



	vector<vector<double>> weight[2];
	vector<double> bias[2];
	vector<vector<double>> dummy_input;
	
#ifdef PCA	
	vector<double> mean;
	vector<vector<double>> pca;
#endif

	read_test_options(&argc, &argv, &secparam, &address,
		&port, &circuit, &n_sig);

	weight[0] = extract_weight("./parameters/hidden_weight");
	weight[1] = extract_weight("./parameters/output_weight");
	bias[0] = extract_bias("./parameters/hidden_bias");
	bias[1] = extract_bias("./parameters/output_bias");

	seclvl seclvl = get_sec_lvl(secparam);

#ifdef PCA 
	pca = extract_weight("./parameters/pca");
	mean = extract_bias("./parameters/mean");
#endif
std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
while( true )
{
	predict(SERVER, address, port, seclvl, nthreads, mt_alg, dummy_input, weight, bias , n_sig
#ifdef PCA
		, pca, mean
#endif
		);
	std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
	if (std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() > 10000)
		break;

}


	return 0;
}
