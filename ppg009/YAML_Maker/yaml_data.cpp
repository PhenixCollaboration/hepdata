/*
YAML maker
Tom Krobatsch
tkrobats@vols.utk.edu
*/

#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <algorithm>

//serialize_encaps strips out any non-printable characters
//and encloses '' around the string for latex equations
std::string serialize_encaps(std::string input) {
	std::string serialize;
	serialize += "'";
	for (int i = 0; i < input.length(); i++) {
		if (!((input[i] < 0) || (input[i] > 255))) {
			serialize += input[i];
		}
	}
	//clear any spaces at end
	serialize.erase(std::find_if(serialize.rbegin(), serialize.rend(),
		std::not1(std::ptr_fun<int, int>(std::isspace))).base(), serialize.end());
	serialize += "'";
	return serialize;
}

//serialize strips out any non-printable characters
std::string serialize(std::string input) {
	std::string serialize;
	for (int i = 0; i < input.length(); i++) {
		if (!((input[i] < 0) || (input[i] > 255))) {
			serialize += input[i];
		}
	}
	//clear any spaces at end
	serialize.erase(std::find_if(serialize.rbegin(), serialize.rend(),
		std::not1(std::ptr_fun<int, int>(std::isspace))).base(), serialize.end());
	return serialize;
}

int main(int argc, char** argv) {
	//per line data
	std::vector<std::string> x, y, x_low, x_high;
	std::vector<std::string> x_stat, x_sys;
	std::vector<std::string> y_error_each;
	std::vector<std::vector<std::string> > y_error_int;
	std::vector<std::vector<std::vector<std::string> > > y_error_line;
	std::vector<char> y_error_flags;
	//total data
	std::vector<std::vector<std::string> > x_ttl, y_ttl, x_low_ttl, x_high_ttl;
	std::vector<std::vector<std::vector<std::vector<std::string> > > > y_error_ttl;
	std::vector<std::vector<std::string> > x_stat_ttl, x_sys_ttl;
	//titles
	std::string x_title;
	std::vector<std::string> y_titles, y_error_titles, qualifiers;
	//loop and conditional varibles 
	size_t found;
	char bin_flag, x_stat_flag, x_sys_flag;
	int y_count, y_error_count, data_counter, print_test;
	//file and string handling
	std::ifstream fin;
	std::ofstream fout;
	std::string out_file_name;
	std::string input, serialized_string, temp;
	std::stringstream ss;

	//error check argument
	if (argc != 3) { std::cerr << "usage: yaml_data debug data_filename" << std::endl; return 1; }

	//print test = 1 for printing all data to the terminal
	print_test = std::atoi(argv[1]);

	//open file
	fin.open(argv[2]);
	if (fin.bad()) { std::cerr << "Problem opening file. Check that it exists" << std::endl; return 1; }

	//make yaml file name
	out_file_name = argv[2];
	std::string::size_type i = out_file_name.rfind('.', out_file_name.length());
	if (i != std::string::npos) { out_file_name.replace(i + 1, 4, "yaml"); }
	else { out_file_name.append(".yaml"); }

	//get x title
	std::getline(fin, input);
	x_title = serialize_encaps(input);
	if (print_test) { std::cout << "x title " << x_title << std::endl; }

	//get y count
	std::getline(fin, input);
	serialized_string = serialize(input);
	y_count = atoi(serialized_string.c_str());
	if (print_test) { std::cout << "y count " << y_count << std::endl; }

	//get y titles
	for (i = 0; i < y_count; i++) {
		std::getline(fin, input);
		serialized_string = serialize_encaps(input);
		y_titles.push_back(serialized_string);
		if (print_test) { std::cout << "y title " << i << ": " << y_titles[i] << std::endl; }
	}

	//get y qualifiers
	for (i = 0; i < y_count; i++) {
		std::getline(fin, input);
		serialized_string = serialize_encaps(input);
		qualifiers.push_back(serialized_string);
		if (print_test) { std::cout << "qualifiers " << i << ": " << qualifiers[i] << std::endl; }
	}

	//get bin style
	std::getline(fin, input);
	serialized_string = serialize(input);
	bin_flag = toupper(serialized_string[0]);
	if (print_test) { std::cout << "bin " << bin_flag << std::endl; }

	//x error
	std::getline(fin, input);
	serialized_string = serialize(input);
	x_stat_flag = toupper(serialized_string[0]);
	std::getline(fin, input);
	serialized_string = serialize(input);
	x_sys_flag = toupper(serialized_string[0]);
	if (print_test) { std::cout << "x stat " << x_stat_flag << std::endl; }
	if (print_test) { std::cout << "x sys " << x_sys_flag << std::endl; }

	//get y error count
	std::getline(fin, input);
	serialized_string = serialize(input);
	y_error_count = atoi(serialized_string.c_str());
	if (print_test) { std::cout << "y error count " << y_error_count << std::endl; }


	//y error titles and types
	for (i = 0; i < y_error_count; i++) {
		std::getline(fin, input);
		serialized_string = serialize_encaps(input);
		y_error_titles.push_back(serialized_string);
		std::getline(fin, input);
		serialized_string = serialize(input);
		y_error_flags.push_back(toupper(serialized_string[0]));
		if (print_test) { std::cout << "y error title " << i << ": " << y_error_titles[i] << std::endl; }
		if (print_test) { std::cout << "y error type " << i << ": " << y_error_flags[i] << std::endl; }
	}

	//process data
	data_counter = 0;
	while (std::getline(fin, input)) {
		serialized_string = serialize(input);
		std::stringstream ss(serialized_string);

		if (input[0] == '*') {
			//add to main array
			x_ttl.push_back(x);
			y_ttl.push_back(y);
			x_low_ttl.push_back(x_low);
			x_high_ttl.push_back(x_high);
			y_error_ttl.push_back(y_error_line);
			x_stat_ttl.push_back(x_stat);
			x_sys_ttl.push_back(x_sys);
			//clear existing for use
			x.clear();
			y.clear();
			x_low.clear();
			x_high.clear();
			y_error_line.clear();
			x_stat.clear();
			x_sys.clear();
			data_counter++;
		}
		else {
			//get x's depending on bin style
			switch (bin_flag) {
			case 'Y':
				ss >> temp;
				x_low.push_back(temp);
				ss >> temp;
				x_high.push_back(temp);
				/*				found = temp.find("-");
				if (found != std::string::npos) {
					x_low.push_back(temp.substr(0, found));
					x_high.push_back(temp.substr(found + 1));
					}*/
				break;
			case 'N':
				ss >> temp;
				x.push_back(temp);
				break;
			default:
				std::cerr << "Specify yes or no for Bin style" << std::endl;
				return 1;
				break;
			}

			//get y's
			ss >> temp;
			y.push_back(temp);
			//get x stat errors depending on style
			switch (x_stat_flag) {
			case 'S':
				ss >> temp;
				x_stat.push_back(temp);
				break;
			case 'N':
				break;
			case 'A':
				ss >> temp;
				x_stat.push_back(temp);
				ss >> temp;
				x_stat.push_back(temp);
				break;
			default:
				std::cerr << "Specify symmetric, asymmetric, or none for X stat style" << std::endl;
				return 1;
				break;
			}

			//get x sys errors depending on style
			switch (x_sys_flag) {
			case 'S':
				ss >> temp;
				x_sys.push_back(temp);
				break;
			case 'N':
				break;
			case 'A':
				ss >> temp;
				x_sys.push_back(temp);
				ss >> temp;
				x_sys.push_back(temp);
				break;
			default:
				std::cerr << "Specify symmetric, asymmetric, or none for X sys style" << std::endl;
				return 1;
				break;
			}

			//get y errors depending on style and count
			for (int i = 0; i < y_error_count; i++) {
				switch (y_error_flags[i]) {
				case 'S':
					ss >> temp;
					y_error_each.push_back(temp);
					break;
				case 'A':
					ss >> temp;
					y_error_each.push_back(temp);
					ss >> temp;
					y_error_each.push_back(temp);
					break;
				default:
					std::cerr << "Specify symmetric or asymmetric for Y error style" << std::endl;
					return 1;
					break;
				}
				y_error_int.push_back(y_error_each);
				y_error_each.clear();
			}
			y_error_line.push_back(y_error_int);
			y_error_int.clear();
		}
	}

	//check to see if *** was added
	if (x_ttl.size() != y_count) {
		std::cout << "Check to see if *** was added after each data set:   " << x.size() << "/" << y_count << std::endl;
		return 1;
	}

	//printing for error check
	if (print_test) {
		for (int i = 0; i < y_count; i++) {
			std::cout << std::endl << "print loop: " << i << std::endl;
			for (int j = 0; j < y_ttl[i].size(); j++) { std::cout << "y: " << y_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < x_ttl[i].size(); j++) { std::cout << "x: " << x_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < x_low_ttl[i].size(); j++) { std::cout << "x low: " << x_low_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < x_high_ttl[i].size(); j++) { std::cout << "x high: " << x_high_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < x_stat_ttl[i].size(); j++) { std::cout << "x stat: " << x_stat_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < x_sys_ttl[i].size(); j++) { std::cout << "x sys: " << x_sys_ttl[i][j] << std::endl; }
			std::cout << std::endl;
			for (int j = 0; j < y_error_ttl[i].size(); j++) {
				for (int k = 0; k < y_error_ttl[i][j].size(); k++) {
					for (int l = 0; l < y_error_ttl[i][j][k].size(); l++) {
						std::cout << "y error i/j/k/l " << i << j << k << l << " " << y_error_ttl[i][j][k][l] << std::endl;
					}
				}
			}
		}
		std::cout << std::endl;
	}

	//file handling
	fin.close();
	fout.open(out_file_name.c_str());
	if (fout.bad()) { std::cerr << "Problem opening file. Check that you have write permission" << std::endl; return 1; }

	if (fout.is_open()) {
		//main loop
		for (int i = 0; i < y_count; i++) {
			//print independent values
			if (!x_ttl[i].empty() && i == 0) {
				fout << "independent_variables:" << std::endl;
				fout << "- header: {name: " << x_title << "}" << std::endl;
				fout << "  values:" << std::endl;
				for (int j = 0; j < x_ttl[i].size(); j++) {
					fout << "  - {value: " << x_ttl[i][j] << "}" << std::endl;
					switch (x_stat_flag) {
					case 'S':
						fout << "    errors:" << std::endl;
						fout << "    - {symerror: " << x_stat_ttl[i][j] << ", label: stat}" << std::endl;
						break;
					case 'A':
						fout << "    errors:" << std::endl;
						fout << "    - {asymerror: {plus: " << x_sys_ttl[i][(2 * j) + 1] << ", minus: " << x_sys_ttl[i][2 * j] << "}, label: stat}" << std::endl;
						break;
					case 'N':
						break;
					default:
						std::cerr << "Specify symmetric or asymmetric for X stat error style" << std::endl;
						return 1;
						break;
					}
					switch (x_sys_flag) {
					case 'S':
						fout << "    errors:" << std::endl;
						fout << "    - {symerror: " << x_sys_ttl[i][j] << ", label: sys}" << std::endl;
						break;
					case 'A':
						fout << "    errors:" << std::endl;
						fout << "    - {asymerror: {plus: " << x_sys_ttl[i][(2 * j) + 1] << ", minus: " << x_sys_ttl[i][2 * j] << "}, label: stat}" << std::endl;
						fout << "    - label: sys}" << std::endl;
						break;
					case 'N':
						break;
					default:
						std::cerr << "Specify symmetric or asymmetric for X sys error style" << std::endl;
						return 1;
						break;
					}
				}
			}

			if ((!x_low_ttl[i].empty()) && (!x_high_ttl[i].empty()) && i == 0) {
				if (i == 0) fout << "independent_variables:" << std::endl;
				fout << "- header: {name: " << x_title << "}" << std::endl;
				fout << "  values:" << std::endl;
				for (int j = 0; j < x_low_ttl[i].size(); j++) {
					fout << "  - {low: " << x_low_ttl[i][j] << ", high: " << x_high_ttl[i][j] << "}" << std::endl;
					switch (x_stat_flag) {
					case 'S':
						fout << "    errors:" << std::endl;
						fout << "    - {symerror: " << x_stat_ttl[i][j] << ", label: stat}" << std::endl;
						break;
					case 'A':
						fout << "    errors:" << std::endl;
						fout << "    - {asymerror: {plus: " << x_sys_ttl[i][(2 * j) + 1] << ", minus: " << x_sys_ttl[i][2 * j] << "}, label: stat}" << std::endl;
						break;
					case 'N':
						break;
					default:
						std::cerr << "Specify symmetric or asymmetric for binned X stat error style" << std::endl;
						return 1;
						break;
					}
					switch (x_sys_flag) {
					case 'S':
						fout << "    errors:" << std::endl;
						fout << "    - {symerror: " << x_sys_ttl[i][j] << ", label: sys}" << std::endl;
						break;
					case 'A':
						fout << "    errors:" << std::endl;
						fout << "    - {asymerror: {plus: " << x_sys_ttl[i][(2 * j) + 1] << ", minus: " << x_sys_ttl[i][2 * j] << "}, label: stat}" << std::endl;
						break;
					case 'N':
						break;
					default:
						std::cerr << "Specify symmetric or asymmetric for binned X sys error style" << std::endl;
						return 1;
						break;
					}
				}
			}
			//print dependent values
			if (!y_ttl[i].empty()) {
				if (i == 0) fout << "dependent_variables:" << std::endl;
				fout << "- header: {name: " << y_titles[i] << "}" << std::endl;
				fout << "  qualifiers:" << std::endl;
				fout << "  - {name: " << x_title << ", value: " << qualifiers[i] << "}" << std::endl;
				fout << "  values:" << std::endl;

				for (int j = 0; j < y_ttl[i].size(); j++) {
					fout << "  - value: " << y_ttl[i][j] << std::endl;
					for (int k = 0; k < y_error_ttl[i][j].size(); k++) {
						switch (y_error_flags[k]) {
						case 'S':
							if (k == 0) fout << "    errors:" << std::endl;
							fout << "    - {symerror: " << y_error_ttl[i][j][k][0] << ", label: " << y_error_titles[k] << "}" << std::endl;
							break;
						case 'A':
							if (k == 0) fout << "    errors:" << std::endl;
							fout << "    - {asymerror: {plus: " << y_error_ttl[i][j][k][0] << ", minus: " << y_error_ttl[i][j][k][1] << "}, label: " << y_error_titles[k] << "}" << std::endl;
							break;
						case 'N':
							break;
						default:
							std::cerr << "Specify symmetric or asymmetric for Y error style" << std::endl;
							return 1;
							break;
						}
					}
				}
			}
		}
		fout.close();
	}
	return 0;
}
